from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: int

    customer: str

    title: str

    description: str

    priority: str

    originalPriority: str

    assignee: str

    timeLeft: int

    status: str

    escalated: bool

    slaStatus: str

    slaDeadline: datetime


class TicketListResponse(BaseModel):
    tickets: list[TicketResponse]

    total: int


class DashboardResponse(BaseModel):
    urgent: int

    overdue: int

    at_risk: int

    in_progress: int

    total: int