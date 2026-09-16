from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    email = Column(
        String(255),
        nullable=False
    )


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=False
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    assignee_id = Column(
        Integer,
        ForeignKey("agents.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    priority = Column(
        String(20),
        nullable=False,
        index=True
    )

    original_priority = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="Open",
        index=True
    )

    created_at = Column(
        DateTime,
        nullable=False
    )

    sla_deadline = Column(
        DateTime,
        nullable=False,
        index=True
    )

    escalated = Column(
        Boolean,
        default=False,
        nullable=False
    )

    last_escalated_at = Column(
        DateTime,
        nullable=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class TicketEvent(Base):
    """
    Audit trail.

    This lets us know WHY a ticket changed.
    """

    __tablename__ = "ticket_events"

    id = Column(
        Integer,
        primary_key=True
    )

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False,
        index=True
    )

    event_type = Column(
        String(50),
        nullable=False
    )

    old_priority = Column(
        String(20),
        nullable=True
    )

    new_priority = Column(
        String(20),
        nullable=True
    )

    message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )