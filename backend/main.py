from contextlib import asynccontextmanager
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine, get_db
from .escalation import escalate_breached_tickets
from .models import Agent, Customer, Ticket
from .queue import (
    get_ordered_tickets,
    get_sla_state,
    get_time_remaining,
)
from .seed import seed_database


scheduler = BackgroundScheduler()


def run_escalation_job():

    db = SessionLocal()

    try:

        count = escalate_breached_tickets(db)

        if count > 0:
            print(
                f"[SLA AUTOMATION] "
                f"Escalated {count} ticket(s)"
            )

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create tables
    Base.metadata.create_all(
        bind=engine
    )

    # Seed fake data
    seed_database()

    # Run escalation every minute
    scheduler.add_job(
        run_escalation_job,
        "interval",
        minutes=1,
        id="sla_escalation",
        replace_existing=True,
    )

    scheduler.start()

    print(
        "SLA escalation automation started."
    )

    yield

    scheduler.shutdown()


app = FastAPI(
    title="HelpDesk Emergency Queue API",
    version="1.0.0",
    lifespan=lifespan,
)


# ------------------------------------------------
# CORS
# ------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ------------------------------------------------
# Health
# ------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "HelpDesk API is running",
        "status": "ok",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ------------------------------------------------
# Ticket converter
# ------------------------------------------------

def ticket_to_response(
    ticket: Ticket,
    customer: Customer,
    agent: Agent,
    now: datetime,
):

    time_left = get_time_remaining(
        ticket,
        now
    )

    return {
        "id": ticket.id,

        "customer": customer.name,

        "title": ticket.title,

        "description": ticket.description,

        "priority": ticket.priority,

        "originalPriority": (
            ticket.original_priority
        ),

        "assignee": agent.name,

        "timeLeft": time_left,

        "status": ticket.status,

        "escalated": ticket.escalated,

        "slaStatus": get_sla_state(
            ticket,
            now
        ),

        "slaDeadline": ticket.sla_deadline,
    }


# ------------------------------------------------
# Emergency Queue
# ------------------------------------------------

@app.get("/api/tickets")
def get_tickets(

    priority: str | None = Query(
        default=None
    ),

    status: str | None = Query(
        default=None
    ),

    time_filter: str | None = Query(
        default=None
    ),

    search: str | None = Query(
        default=None
    ),

    db: Session = Depends(get_db),
):

    now = datetime.utcnow()

    tickets = get_ordered_tickets(
        db,
        now
    )

    results = []

    for ticket in tickets:

        customer = db.query(Customer).filter(
            Customer.id == ticket.customer_id
        ).first()

        agent = db.query(Agent).filter(
            Agent.id == ticket.assignee_id
        ).first()

        if not customer or not agent:
            continue

        # -----------------------------------------
        # Priority filter
        # -----------------------------------------

        if (
            priority
            and priority != "All"
            and ticket.priority != priority
        ):
            continue

        # -----------------------------------------
        # Status filter
        # -----------------------------------------

        if (
            status
            and status != "All"
            and ticket.status != status
        ):
            continue

        # -----------------------------------------
        # Search
        # -----------------------------------------

        if search:

            search_text = search.lower()

            searchable = (
                f"{customer.name} "
                f"{ticket.title} "
                f"{ticket.description}"
            ).lower()

            if search_text not in searchable:
                continue

        # -----------------------------------------
        # Time filter
        # -----------------------------------------

        time_left = get_time_remaining(
            ticket,
            now
        )

        if time_filter:

            valid = True

            if time_filter == "Overdue":
                valid = time_left <= 0

            elif time_filter == "<15 min":
                valid = 0 < time_left < 15

            elif time_filter == "15–30 min":
                valid = 15 <= time_left <= 30

            elif time_filter == "30–60 min":
                valid = 30 < time_left <= 60

            elif time_filter == "1–2 hrs":
                valid = 60 < time_left <= 120

            elif time_filter == ">2 hrs":
                valid = time_left > 120

            if not valid:
                continue

        results.append(
            ticket_to_response(
                ticket,
                customer,
                agent,
                now
            )
        )

    return {
        "tickets": results,
        "total": len(results),
    }


# ------------------------------------------------
# Single ticket
# ------------------------------------------------

@app.get("/api/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if not ticket:

        return {
            "error": "Ticket not found"
        }

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == ticket.customer_id
        )
        .first()
    )

    agent = (
        db.query(Agent)
        .filter(
            Agent.id == ticket.assignee_id
        )
        .first()
    )

    now = datetime.utcnow()

    return ticket_to_response(
        ticket,
        customer,
        agent,
        now
    )


# ------------------------------------------------
# Dashboard
# ------------------------------------------------

@app.get("/api/dashboard")
def dashboard(
    db: Session = Depends(get_db),
):

    now = datetime.utcnow()

    tickets = (
        db.query(Ticket)
        .filter(
            Ticket.status != "Resolved"
        )
        .all()
    )

    urgent = 0
    overdue = 0
    at_risk = 0
    in_progress = 0

    for ticket in tickets:

        if ticket.priority == "Urgent":
            urgent += 1

        time_left = get_time_remaining(
            ticket,
            now
        )

        if time_left <= 0:
            overdue += 1

        elif time_left <= 30:
            at_risk += 1

        if ticket.status == "In Progress":
            in_progress += 1

    return {
        "urgent": urgent,
        "overdue": overdue,
        "at_risk": at_risk,
        "in_progress": in_progress,
        "total": len(tickets),
    }


# ------------------------------------------------
# Manual trigger for testing
# ------------------------------------------------

@app.post("/api/admin/run-escalation")
def manual_escalation_run():

    db = SessionLocal()

    try:

        count = escalate_breached_tickets(
            db
        )

        return {
            "message": "Escalation job completed",
            "escalated": count,
        }

    finally:
        db.close()