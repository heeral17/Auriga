from datetime import datetime

from sqlalchemy.orm import Session

from .models import Ticket


PRIORITY_RANK = {
    "Urgent": 0,
    "High": 1,
    "Normal": 2,
}


def get_sla_state(ticket: Ticket, now: datetime) -> str:

    seconds_remaining = (
        ticket.sla_deadline - now
    ).total_seconds()

    if seconds_remaining <= 0:
        return "Breached"

    if seconds_remaining <= 30 * 60:
        return "At risk"

    return "On track"


def get_time_remaining(ticket: Ticket, now: datetime) -> int:

    seconds = (
        ticket.sla_deadline - now
    ).total_seconds()

    return round(seconds / 60)


def queue_sort_key(ticket: Ticket, now: datetime):

    time_remaining = get_time_remaining(
        ticket,
        now
    )

    # Rule 1:
    # breached tickets ALWAYS come first.

    breached_bucket = (
        0 if time_remaining <= 0 else 1
    )

    # Rule 2:
    # among active tickets, nearest deadline first.

    return (
        breached_bucket,
        ticket.sla_deadline,
        PRIORITY_RANK.get(ticket.priority, 99),
        ticket.created_at,
        ticket.id,
    )


def get_ordered_tickets(
    db: Session,
    now: datetime | None = None
):

    if now is None:
        now = datetime.utcnow()

    tickets = (
        db.query(Ticket)
        .filter(Ticket.status != "Resolved")
        .all()
    )

    tickets.sort(
        key=lambda ticket:
        queue_sort_key(ticket, now)
    )

    return tickets