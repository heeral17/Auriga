Problem statement : stack_queue
# Helpdesk Queue Management System

A full-stack Helpdesk Queue Management System that allows users to create support tickets and enables support staff to manage, prioritize, and resolve those tickets.

## Features

* Create support tickets
* View all tickets
* Track ticket status
* Assign ticket priority
* Update ticket status
* Search/filter tickets
* REST API backend
* Web-based frontend
* Persistent database storage
* Input validation and error handling

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask
* SQLite
* REST APIs

### Development Tools

* Git
* GitHub
* Python virtual environment

---

## Project Structure

```text
helpdesk-queue/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   ├── database.py
│   └── requirements.txt
│
├── README.md
├── REASONING.md
└── .gitignore
```

---

# Prerequisites

Install the following:

* Python 3.10 or newer
* Git
* A modern web browser

Check Python:

```bash
python --version
```

On some Windows systems:

```bash
py --version
```

---

# Setup

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd helpdesk-queue
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

If the `python` command does not work:

```bash
py -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

Move into the backend directory:

```bash
cd backend
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Backend

From the `backend` directory:

```bash
python app.py
```

If successful, Flask will start the development server.

The backend will normally be available at:

```text
http://127.0.0.1:5000
```

Keep this terminal running.

---

# Running the Frontend

Open the `frontend/index.html` file in a browser.

Alternatively, use VS Code Live Server if it is installed.

The frontend communicates with the Flask backend through REST API endpoints.

---

# API Endpoints

## Get Tickets

```http
GET /api/tickets
```

Returns the available helpdesk tickets.

## Create Ticket

```http
POST /api/tickets
```

Example request:

```json
{
    "title": "Unable to login",
    "description": "User cannot access the application.",
    "priority": "High"
}
```

## Update Ticket

```http
PUT /api/tickets/<ticket_id>
```

Used to update ticket information such as status or priority.

## Delete Ticket

```http
DELETE /api/tickets/<ticket_id>
```

Deletes a ticket from the system.

---

# Ticket Lifecycle

Tickets follow a simple workflow:

```text
New
 ↓
Open
 ↓
In Progress
 ↓
Resolved
```

A ticket can also be closed after resolution.

---

# Database

The application uses SQLite for local persistent storage.

The database is automatically created by the backend if it does not already exist.

The database stores information such as:

* Ticket ID
* Title
* Description
* Priority
* Status
* Creation timestamp
* Updated timestamp

---

# Debugging

## Backend does not start

Check that Python is installed:

```bash
python --version
```

Check that the virtual environment is active.

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

---

## `ModuleNotFoundError`

If you see an error such as:

```text
ModuleNotFoundError: No module named 'flask'
```

Run:

```bash
pip install -r requirements.txt
```

---

## Frontend cannot connect to backend

Make sure the Flask server is running:

```bash
python app.py
```

Then verify that the API is available at:

```text
http://127.0.0.1:5000
```

Also check the browser Developer Tools:

```text
F12 → Console
F12 → Network
```

Look for failed API requests or CORS errors.

---

## Port already in use

If port `5000` is already being used, stop the process using it or configure Flask to use another port.

For example:

```python
app.run(debug=True, port=5001)
```

Then update the frontend API URL accordingly.

---

# GitHub

After making changes:

```bash
git status
```

Add the files:

```bash
git add .
```

Commit:

```bash
git commit -m "Complete helpdesk queue application"
```

Push:

```bash
git push
```

Make sure `README.md` and `REASONING.md` are located in the repository root so that the evaluator can find them easily.

---

# Troubleshooting Checklist

Before submission, verify:

* [ ] Python is installed
* [ ] Virtual environment works
* [ ] Dependencies install successfully
* [ ] Flask backend starts
* [ ] Database is created
* [ ] Frontend loads
* [ ] Frontend can communicate with backend
* [ ] Ticket creation works
* [ ] Ticket updates work
* [ ] Ticket deletion works
* [ ] Filtering/search works
* [ ] No sensitive information is committed
* [ ] README.md exists
* [ ] REASONING.md exists
* [ ] All files are pushed to GitHub

---

# Future Improvements

Possible improvements include:

* User authentication
* Role-based access control
* PostgreSQL/MySQL production database
* Email notifications
* Ticket assignment to support agents
* SLA monitoring
* Analytics dashboard
* Docker deployment
* Automated testing
* Cloud deployment
