Today 2:45 PM

ROUND 2  ·  BUILD ROUND
The helpdesk is drowning
Priya runs a two-person IT helpdesk and the queue never stops. Some tickets are ‘my laptop won’t boot before a client demo’ emergencies; others are ‘can I get a bigger monitor.’ Each ticket has a priority and an agreed response time — urgent within 2 hours, normal within a day — and Priya wants to always pick the most pressing ticket next, with anything past its promised time jumping to the front. She’s forever answering ‘what’s overdue?’ and ‘what’s assigned to me?’, and looking up a specific customer’s ticket by name. The list is huge, so she pages through it.
Build Priya something so the right ticket is always on top.
(The way Priya talks about her queue tells you what it needs — the ordering rule is the heart of it. Build it for any helpdesk, not just Priya’s. Get tickets and the queue order right first, then filters and assignment.)

This is a build-round product challenge. The key is not making a generic helpdesk CRUD app—the evaluator is explicitly telling you that queue ordering is the core logic.

I’d build a small but polished Helpdesk Ticket Queue with this behavior:

1. Core ticket model

Each ticket should have:

id
title
customer
description
priority — urgent / normal
created_at
due_at
status — open, in_progress, resolved
assignee
updated_at

The important field is due_at, because overdue status should be calculated from the current time, not manually entered.

2. Queue ordering — the heart of the app

Use this ordering:

1. Overdue tickets first
2. Within overdue:
      earliest due_at first
3. Then non-overdue urgent tickets
4. Then normal tickets
5. Within the same priority:
      earliest due_at first
6. Use created_at / id as a deterministic tie-breaker

Conceptually:

def queue_key(ticket, now):
    overdue = ticket.due_at < now

    return (
        not overdue,                         # overdue first
        0 if ticket.priority == "urgent" else 1,
        ticket.due_at,
        ticket.created_at
    )

But there is one subtlety: an overdue normal ticket must jump ahead of a non-overdue urgent ticket, because the prompt explicitly says anything past its promised time jumping to the front.

So I'd make the logic explicit:

def queue_key(ticket, now):
    if ticket.due_at <= now:
        bucket = 0
    elif ticket.priority == "urgent":
        bucket = 1
    else:
        bucket = 2

    return (
        bucket,
        ticket.due_at,
        ticket.created_at
    )

That gives:

OVERDUE
 ├── oldest overdue urgent
 ├── oldest overdue normal
 └── ...

URGENT
 ├── earliest deadline
 └── ...

NORMAL
 ├── earliest deadline
 └── ...

This is the behavior I'd demonstrate first in the demo.

3. UI

Keep it simple:

┌─────────────────────────────────────────────────────┐
│ Helpdesk Queue                         + New Ticket │
├─────────────────────────────────────────────────────┤
│ 🔴 7 Overdue   🟠 4 Urgent   🟢 18 Normal           │
├─────────────────────────────────────────────────────┤
│ Search customer/ticket...                            │
│ [All] [Overdue] [My Tickets] [Urgent] [Normal]      │
├─────────────────────────────────────────────────────┤
│ 🔴 #1042  Laptop won't boot                         │
│     Acme Corp • URGENT • Overdue 1h 24m             │
│     Assigned: Priya                                  │
├─────────────────────────────────────────────────────┤
│ 🔴 #1038  VPN unavailable                           │
│     Globex • NORMAL • Overdue 42m                   │
│     Assigned: Rahul                                  │
├─────────────────────────────────────────────────────┤
│ 🟠 #1045  Client demo laptop                        │
│     Stark Industries • URGENT • Due in 38m          │
│     Unassigned                                       │
└─────────────────────────────────────────────────────┘

                  1  2  3  4  5  →
4. Required interactions

I'd make these work before adding anything fancy:

Create ticket

Customer
Title
Description
Priority
Assignee
Response SLA

Automatically calculate:

urgent → created_at + 2 hours
normal → created_at + 24 hours

Filters

All tickets
Overdue
Assigned to me
Urgent
Normal
Status

Customer search

Searching:

"Acme"

should return Acme's tickets.

Pagination

Don't fetch the entire queue and paginate in the browser if the challenge expects a real scalable implementation.

Use:

GET /tickets?page=2&limit=20

and ideally perform the ordering in the database.

5. Backend API

Something like:

POST   /tickets
GET    /tickets
GET    /tickets/:id
PATCH  /tickets/:id
GET    /tickets?overdue=true
GET    /tickets?assignee=Priya
GET    /tickets?customer=Acme

The important endpoint is:

GET /tickets

because it should return the queue already correctly ordered.

For example:

{
  "tickets": [...],
  "page": 1,
  "page_size": 20,
  "total": 127
}
6. Database

A simple relational DB is enough.

tickets
-------
id
title
description
customer_id
priority
status
assignee_id
created_at
due_at
updated_at

Plus:

customers
---------
id
name
email

and:

users
-----
id
name
email

Useful indexes:

INDEX(priority)
INDEX(due_at)
INDEX(assignee_id)
INDEX(customer_id)
INDEX(status)

If the dataset becomes large, these matter much more than fancy UI features.

7. The demo scenario

This is what I'd actually show the evaluator.

Create five tickets:

Ticket	Priority	Due	Result
Laptop won't boot	Urgent	1h ago	🔴 #1
VPN broken	Normal	30m ago	🔴 #2
Client demo	Urgent	20m	🟠 #3
Monitor request	Normal	5h	🟢 #4
Keyboard request	Normal	20h	🟢 #5

Then let time pass / modify the clock or create an already-overdue ticket.

The queue should automatically reorder.

That demonstrates the central requirement much more convincingly than showing 15 CRUD screens.

8. Build priority

If you have limited time, I'd allocate it like this:

40%  Queue ordering + SLA logic
20%  Ticket CRUD
15%  Filters/search
10%  Assignment
10%  Pagination
 5%  UI polish

Don't spend half the round building authentication, dashboards, charts, email notifications, etc.

The challenge literally tells you:

“Get tickets and the queue order right first, then filters and assignment.”

So I'd treat that as the implementation roadmap.

If you're building this for an actual coding/build round, I can also give you a 
complete project structure + database schema + backend + frontend implementation that you can run locally and submit.
lets build this project a simple website  into parts first part is  designing UI/UX tech stack react tailwind css it should have a simple look , a basic front page which will be containg all details of the customers 

```
Customer name 
Title
Description/Problem 
Priority
Assignee
Response Time urgency level  then a filtering option acc to urgency time remaining )
```
Yes. Let’s build this UI-first, and keep the first version deliberately simple.

The key design decision is: this is an action queue, not a traditional ticket-management table. When Priya opens the site, the first thing she should see is who needs attention next and how much time is left.

Part 1 — Front Page / Emergency Queue
Proposed screen
┌─────────────────────────────────────────────────────────────────────┐
│  HelpDesk                                      🔔  Priya ▼          │
│  Emergency Queue                                                   │
│  Resolve the most pressing customer issue first.                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🚨 8 Urgent Tickets        3 Overdue        12 In Progress       │
│                                                                     │
│  Filter: [ All Urgency ▼ ] [ All Assignees ▼ ]   🔍 Search         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ CUSTOMER       PROBLEM              PRIORITY   ASSIGNEE   TIME LEFT │
├─────────────────────────────────────────────────────────────────────┤
│ 🔴 Acme Corp   Laptop won't boot    URGENT     Priya       18 min   │
│               Client demo today                                      │
│                                                                     │
│ 🟠 TechNova    VPN connection       URGENT     Rahul       42 min   │
│               Unable to access server                               │
│                                                                     │
│ 🟡 John Smith  Bigger monitor       NORMAL     Priya       18 hrs   │
│               Request for workspace                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

But I would make one important UX change:

Don't make it look like a boring spreadsheet

Each ticket should be a compact card/row, with the most important information visually emphasized:

┌────────────────────────────────────────────────────────────────────┐
│ 🔴  ACME CORPORATION                              18 MIN LEFT      │
│                                                                    │
│     Laptop won't boot before client demo                            │
│     Device completely fails to start                               │
│                                                                    │
│     URGENT       👤 Priya       ⚠ SLA AT RISK                      │
└────────────────────────────────────────────────────────────────────┘

The time remaining should be the strongest visual element because that's what actually determines what Priya needs to look at.

UI structure

I'd make the first page have only 4 major sections.

1. Header
HelpDesk
Emergency Queue                         Priya Jain ▾

Simple white header, small logo/icon, no unnecessary navigation yet.

2. Queue statistics

Small cards:

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 🚨 Urgent    │ │ 🔴 Overdue   │ │ ⚡ At Risk   │ │ ✓ Resolved   │
│      8       │ │      2       │ │      3       │ │     24       │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

These are useful because Priya can understand the state of the helpdesk in 2 seconds.

3. Filters

This is where your "filter according to urgency/time remaining" comes in.

I'd use:

[ All Tickets ▼ ]

[ Time Remaining ▼ ]

[ Priority ▼ ]

[ Assignee ▼ ]

[ Status ▼ ]

                 🔍 Search customer or problem
Time Remaining options
All
Overdue
< 15 minutes
15–30 minutes
30–60 minutes
1–2 hours
> 2 hours

This is better than simply "urgent/normal" because the actual operational question is:

Who is closest to missing their response deadline?

4. Emergency Queue

The queue itself should be automatically ordered.

For example:

🚨 EMERGENCY QUEUE

1
┌──────────────────────────────────────────────────────────────┐
│ 🔴  Sarah Williams                          12 MIN LEFT      │
│     Laptop won't boot                                         │
│     Critical issue before client presentation                 │
│                                                              │
│     URGENT   •   Hardware   •   👤 Priya   •   SLA AT RISK  │
└──────────────────────────────────────────────────────────────┘

2
┌──────────────────────────────────────────────────────────────┐
│ 🔴  Acme Corporation                         31 MIN LEFT      │
│     VPN unavailable                                           │
│     Cannot access production environment                      │
│                                                              │
│     URGENT   •   Network    •   👤 Rahul   •   SLA SAFE     │
└──────────────────────────────────────────────────────────────┘

3
┌──────────────────────────────────────────────────────────────┐
│ 🟠  John Smith                              1 HR 14 MIN       │
│     Software installation                                    │
│                                                              │
│     URGENT   •   Software   •   👤 Priya                      │
└──────────────────────────────────────────────────────────────┘
Most important part: queue behavior

The frontend should not decide urgency.

We'll eventually have the backend return something like:

{
  "id": 1024,
  "customer": "Sarah Williams",
  "title": "Laptop won't boot",
  "description": "Laptop fails to start before client presentation",
  "priority": "urgent",
  "assignee": "Priya",
  "due_at": "2026-09-16T16:20:00",
  "time_remaining_seconds": 720,
  "urgency": "critical",
  "sla_status": "at_risk"
}

React simply displays it.

The backend queue engine determines:

OVERDUE
   ↓
< 15 min
   ↓
15–30 min
   ↓
30–60 min
   ↓
1–2 hours
   ↓
> 2 hours

That means if there are 100 tickets, Priya doesn't need to mentally process all 100.

She sees:

Sarah Williams — 12 minutes left

and knows immediately what she should deal with.

Tech stack for Part 1

Since we're only building the UI first:

Frontend

React + TypeScript + Tailwind CSS

I'd also use:

Vite — project/build tool
Lucide React — clean icons
React Router — later, when we add ticket details/dashboard
TanStack Query — later, when connecting APIs

So:

React
  │
  ├── TypeScript
  ├── Tailwind CSS
  ├── Lucide Icons
  └── Vite

Don't add Redux yet. We don't need it.

Component architecture

Let's keep the code clean from the beginning:

src/
│
├── components/
│   ├── Header.tsx
│   ├── StatsCard.tsx
│   ├── FilterBar.tsx
│   ├── TicketCard.tsx
│   ├── UrgencyBadge.tsx
│   └── TimeRemaining.tsx
│
├── pages/
│   └── Dashboard.tsx
│
├── data/
│   └── mockTickets.ts
│
├── types/
│   └── ticket.ts
│
├── App.tsx
├── main.tsx
└── index.css

This is enough for the first version.

Visual style

I'd avoid the typical flashy AI dashboard.

Use:

Background: very light gray
Cards: white
Text: dark gray/black
Borders: subtle
Urgency: red/orange/yellow only where meaningful
Buttons: simple
Font: Inter/system font

The overall feeling should be:

Calm interface + strong urgency signals

rather than "AI startup dashboard with 20 glowing widgets."

One more UX feature I'd add

Every ticket should have a small "Why?" indicator.

For example:

🔴 12 MIN LEFT
⚠ SLA AT RISK

Why is this urgent?
• 12 minutes remaining
• Critical issue
• Client-facing

This becomes especially useful later when we introduce AI.

The AI can help determine:

Severity: Critical
Business impact: Client-facing
Estimated resolution: 45 min
SLA risk: High

But the actual deadline remains deterministic.

Our build sequence

I suggest we build this in exactly this order:

PART 1
Frontend UI
       ↓
Mock ticket data
       ↓
Queue sorting
       ↓
Urgency/time filters
       ↓
Responsive design
       ↓
        DONE

PART 2
FastAPI
       ↓
PostgreSQL
       ↓
Ticket API
       ↓
Real queue engine
       ↓
        DONE

PART 3
AI Triage
       ↓
Severity/category/complexity
       ↓
SLA risk estimation
       ↓
        DONE

PART 4
RAG + Helpdesk Copilot
       ↓
Knowledge base
       ↓
Troubleshooting suggestions
       ↓
        DONE

PART 5
Daily 24-hour dashboard
       ↓
Resolved / Remaining / SLA breaches
       ↓
Historical analytics

For now, we should not touch AI/backend. Let's make the frontend feel like a real product first.

Next, I can give you the 
complete React + Tailwind Part 1 code, including mock tickets, the emergency queue, countdown-style time remaining, filters, search, and a clean responsive UI.