
# Reasoning Behind the Solution

## 1. Problem Understanding

The objective was to build a Helpdesk Queue Management System that allows support requests to be created, stored, viewed, and managed through their lifecycle.

The application needed both a frontend interface and a backend capable of handling business logic and persistent data.

The main requirements were therefore divided into:

1. Ticket creation
2. Ticket storage
3. Ticket retrieval
4. Ticket status management
5. Priority management
6. Search/filter functionality
7. Backend API communication
8. Error handling
9. Simple and understandable project structure

---

## 2. Architecture

The application follows a simple client-server architecture:

```text
┌──────────────────────┐
│      Frontend        │
│ HTML / CSS / JS      │
└──────────┬───────────┘
           │
           │ HTTP / REST API
           ▼
┌──────────────────────┐
│       Backend        │
│       Python         │
│       Flask          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       SQLite         │
│      Database        │
└──────────────────────┘
```

This separation keeps the user interface independent from the business logic and database operations.

---

## 3. Frontend Decision

HTML, CSS, and JavaScript were selected for the frontend because the project primarily requires a dashboard-style interface rather than a complex frontend framework.

This provides several advantages:

* Easy to run
* No frontend build process
* Easy for evaluators to inspect
* Minimal dependencies
* Direct interaction with REST APIs

JavaScript is responsible for:

* Sending API requests
* Receiving API responses
* Updating the ticket list
* Handling forms
* Applying filters
* Updating the interface without requiring a complete page reload

---

## 4. Backend Decision

Python with Flask was selected for the backend.

Flask provides a lightweight way to expose REST API endpoints while keeping the implementation simple.

The backend is responsible for:

* Receiving client requests
* Validating input
* Applying ticket-related logic
* Reading and writing database records
* Returning JSON responses
* Handling errors

The backend therefore acts as the central layer between the frontend and database.

---

## 5. Database Decision

SQLite was selected as the database for this implementation.

The project is designed as an evaluation/demo application, so a lightweight local database avoids unnecessary infrastructure.

SQLite provides:

* Persistent storage
* No separate database server
* Simple setup
* SQL-based data management
* Easy portability

For a production-scale deployment, the database could later be replaced with PostgreSQL or another managed relational database.

---

## 6. Ticket Data Model

Each ticket contains information such as:

```text
Ticket
├── id
├── title
├── description
├── priority
├── status
├── created_at
└── updated_at
```

The ID uniquely identifies each ticket.

The status represents the ticket lifecycle, while priority helps support staff determine which requests require greater attention.

---

## 7. Ticket Lifecycle

The ticket workflow is represented as:

```text
New
 ↓
Open
 ↓
In Progress
 ↓
Resolved
 ↓
Closed
```

Keeping the lifecycle explicit makes the system easier to understand and allows additional workflow rules to be added later.

---

## 8. API Design

The backend exposes REST-style endpoints.

The primary operations are:

```text
GET     /api/tickets
POST    /api/tickets
PUT     /api/tickets/<id>
DELETE  /api/tickets/<id>
```

This follows the basic CRUD pattern:

```text
Create  → POST
Read    → GET
Update  → PUT
Delete  → DELETE
```

Using REST APIs also keeps the frontend and backend loosely coupled.

---

## 9. Validation and Error Handling

User input should not be assumed to be valid.

The backend validates important fields before inserting or updating records.

Examples include:

* Required title
* Required description
* Valid priority values
* Valid status values
* Valid ticket IDs

Invalid requests should return an appropriate HTTP status and a useful JSON error message.

This prevents the frontend from being the only layer responsible for validation.

---

## 10. Search and Filtering

Filtering is useful because a helpdesk queue can contain many tickets.

The interface can filter tickets based on attributes such as:

* Status
* Priority
* Search text

This allows support staff to quickly locate relevant tickets without manually scanning the entire queue.

---

## 11. Maintainability

The project is intentionally divided into separate responsibilities.

```text
Frontend
   ↓
API
   ↓
Backend logic
   ↓
Database
```

This makes debugging easier because a problem can be isolated to a particular layer.

For example:

* UI problem → inspect browser/JavaScript
* API problem → inspect Flask routes
* Database problem → inspect SQL/database layer
* Dependency problem → inspect Python environment

---

## 12. Debugging Strategy

The debugging process follows the request path:

```text
User Action
    ↓
Browser
    ↓
JavaScript API Request
    ↓
Flask Route
    ↓
Database Operation
    ↓
API Response
    ↓
Frontend Update
```

If a feature fails, each stage can be checked independently.

Browser Developer Tools can be used to inspect:

* Console errors
* HTTP status codes
* API requests
* API responses

The Flask terminal can be used to inspect backend exceptions and request logs.

---

## 13. Security Considerations

Although this is an evaluation application, several basic practices are followed:

* User input is validated.
* SQL operations should use parameterized queries.
* Sensitive credentials should not be stored in source code.
* Development configuration should not be treated as production configuration.
* `.gitignore` should prevent unnecessary local files such as virtual environments from being committed.

For production, additional controls would be required, including authentication, authorization, HTTPS, rate limiting, stronger validation, secure configuration management, and a production database.

---

## 14. Testing Approach

Testing focuses on the major user flows:

### Ticket Creation

```text
Open application
      ↓
Enter ticket information
      ↓
Submit
      ↓
Verify ticket appears in queue
```

### Ticket Update

```text
Select ticket
      ↓
Change status/priority
      ↓
Submit
      ↓
Verify updated information
```

### Ticket Deletion

```text
Select ticket
      ↓
Delete
      ↓
Verify ticket is removed
```

### API Testing

Each REST endpoint can also be tested independently using the browser, development tools, or an API client.

---

## 15. Tradeoffs

### Flask instead of a larger backend framework

Flask keeps the backend lightweight and makes the API easy to understand.

A larger framework could provide more built-in functionality but would add complexity that is unnecessary for this evaluation project.

### SQLite instead of PostgreSQL

SQLite simplifies local setup and is sufficient for the project's expected scale.

PostgreSQL would be more appropriate for a production system with concurrent users and larger workloads.

### Vanilla JavaScript instead of React

The interface does not require the component architecture or build ecosystem of a large frontend framework.

Using vanilla JavaScript reduces setup complexity and makes the project easier to run during evaluation.

---

## 16. Scalability Path

The current architecture can be extended without completely redesigning the application.

A production version could introduce:

```text
Frontend
    ↓
API Gateway / Load Balancer
    ↓
Multiple Backend Instances
    ↓
PostgreSQL
    ↓
Caching / Queue / Background Workers
```

Potential additions include:

* PostgreSQL
* Redis
* Authentication
* Role-based permissions
* Docker
* CI/CD
* Cloud deployment
* Automated tests
* Logging and monitoring
* Email notifications
* SLA tracking

---

## 17. Final Design Rationale

The solution prioritizes simplicity, clear separation of responsibilities, persistent data, and ease of evaluation.

The architecture provides the core functionality required by a helpdesk system while keeping the implementation understandable and extensible.

The main design principle is:

> Keep the frontend responsible for presentation, the backend responsible for application logic, and the database responsible for persistent storage.

This separation makes the application easier to test, debug, maintain, and extend.
