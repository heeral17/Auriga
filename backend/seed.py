import random
from datetime import datetime, timedelta

from faker import Faker

from .database import Base, SessionLocal, engine
from .models import Agent, Customer, Ticket


fake = Faker()


PRIORITIES = [
    "Normal",
    "High",
    "Urgent",
]

STATUSES = [
    "Open",
    "In Progress",
]


TITLES = [
    "Laptop won't boot",
    "VPN connection unavailable",
    "Email service is not syncing",
    "Cannot access shared drive",
    "Request for larger monitor",
    "Keyboard replacement",
    "Password reset request",
    "Install analytics software",
    "Printer is not responding",
    "Wi-Fi connection unavailable",
    "Software installation request",
    "Cannot access company portal",
]


DESCRIPTIONS = [
    "User is unable to access an important company resource.",
    "Employee reported an issue before an important client meeting.",
    "The service stopped working unexpectedly.",
    "User needs help restoring normal workstation functionality.",
    "Employee cannot complete their normal work because of this issue.",
]


def get_sla_minutes(priority: str):

    if priority == "Urgent":
        return 120

    if priority == "High":
        return 480

    return 1440


def seed_database():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        existing_tickets = db.query(Ticket).count()

        if existing_tickets > 0:
            print("Database already contains tickets.")
            return

        # -------------------------
        # Create agents
        # -------------------------

        agents = [
            Agent(
                name="Priya",
                email="priya@helpdesk.local"
            ),
            Agent(
                name="Rahul",
                email="rahul@helpdesk.local"
            ),
        ]

        db.add_all(agents)
        db.flush()

        # -------------------------
        # Customers
        # -------------------------

        customers = []

        for _ in range(30):

            customer = Customer(
                name=fake.company(),
                email=fake.company_email()
            )

            customers.append(customer)

        db.add_all(customers)
        db.flush()

        # -------------------------
        # Tickets
        # -------------------------

        now = datetime.utcnow()

        for i in range(100):

            priority = random.choices(
                PRIORITIES,
                weights=[55, 25, 20],
                k=1
            )[0]

            sla_minutes = get_sla_minutes(
                priority
            )

            # Create some realistic tickets:
            #
            # 20% overdue
            # 20% at risk
            # remaining on track

            situation = random.random()

            if situation < 0.20:

                minutes_before_now = random.randint(
                    5,
                    180
                )

                created_at = (
                    now
                    - timedelta(
                        minutes=sla_minutes
                        + minutes_before_now
                    )
                )

            elif situation < 0.40:

                minutes_remaining = random.randint(
                    5,
                    30
                )

                created_at = (
                    now
                    - timedelta(
                        minutes=sla_minutes
                        - minutes_remaining
                    )
                )

            else:

                minutes_remaining = random.randint(
                    60,
                    sla_minutes
                )

                created_at = (
                    now
                    - timedelta(
                        minutes=sla_minutes
                        - minutes_remaining
                    )
                )

            sla_deadline = (
                created_at
                + timedelta(
                    minutes=sla_minutes
                )
            )

            ticket = Ticket(
                customer_id=random.choice(
                    customers
                ).id,

                assignee_id=random.choice(
                    agents
                ).id,

                title=random.choice(
                    TITLES
                ),

                description=random.choice(
                    DESCRIPTIONS
                ),

                priority=priority,

                original_priority=priority,

                status=random.choice(
                    STATUSES
                ),

                created_at=created_at,

                sla_deadline=sla_deadline,

                escalated=False,

                updated_at=now,
            )

            db.add(ticket)

        db.commit()

        print("Database seeded successfully.")
        print("Created 30 customers.")
        print("Created 2 helpdesk agents.")
        print("Created 100 fake tickets.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()