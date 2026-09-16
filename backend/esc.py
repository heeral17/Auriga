from datetime import datetime

from sqlalchemy.orm import Session

from .models import Ticket, TicketEvent


ESCALATION_LEVEL = {
    "Normal": "High",
    "High": "Urgent",
    "Urgent": "Urgent",
}


def escalate_breached_tickets(
    db: Session
):

    now = datetime.utcnow()

    breached_tickets = (
        db.query(Ticket)
        .filter(
            Ticket.status != "Resolved",
            Ticket.sla_deadline <= now,
            Ticket.priority != "Urgent"
        )
        .all()
    )

    escalated_count = 0

    for ticket in breached_tickets:

        old_priority = ticket.priority

        new_priority = ESCALATION_LEVEL[
            old_priority
        ]

        # Safety check:
        # never move more than one level.

        if old_priority == "Normal":
            expected = "High"

        elif old_priority == "High":
            expected = "Urgent"

        else:
            continue

        if new_priority != expected:
            continue

        ticket.priority = new_priority
        ticket.escalated = True
        ticket.last_escalated_at = now
        ticket.updated_at = now

        event = TicketEvent(
            ticket_id=ticket.id,
            event_type="AUTO_ESCALATION",
            old_priority=old_priority,
            new_priority=new_priority,
            message=(
                f"Ticket breached SLA. "
                f"Priority automatically increased "
                f"from {old_priority} to {new_priority}."
            ),
            created_at=now,
        )

        db.add(event)

        escalated_count += 1

    db.commit()

    return escalated_count