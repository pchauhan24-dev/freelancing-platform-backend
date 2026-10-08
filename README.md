# Freelancing Platform Backend API

A secure backend API for a freelancing marketplace where clients can post projects and freelancers can submit proposals.

## Features

### Authentication

- User signup and login
- Client and Freelancer roles
- JWT authentication
- Password hashing using bcrypt
- Role-based access control

### Client Features

Clients can:

- Create projects
- View projects
- Search and filter projects
- Update their own projects
- Delete their own projects
- View received proposals
- Accept proposals
- Reject proposals
- Start projects
- Complete projects
- Cancel projects
- Access the client dashboard

### Freelancer Features

Freelancers can:

- Browse available projects
- Search and filter projects
- Submit proposals
- View submitted proposals
- Withdraw pending proposals
- Access the freelancer dashboard

### Proposal System

Freelancers can submit proposals containing:

- Bid amount
- Cover letter
- Estimated delivery time
- Proposal status

Clients can:

- View received proposals
- Accept proposals
- Reject proposals

## Project Status

Projects can have the following statuses:

- Open
- In Progress
- Completed
- Cancelled

### Project Status Flow

```text
Open
  ↓
In Progress
  ↓
Completed
```

A project can also be cancelled:

```text
Open
  ↓
Cancelled
```

## Tech Stack

- Python
- FastAPI
- MongoDB
- PyMongo
- JWT
- Passlib
- Bcrypt
- Pydantic
- Uvicorn

## Project Structure

```text
freelancing-platform-backend/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

Clone the repository and open the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd freelancing-platform-backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_secret_key
```

> **Security:** Never commit the `.env` file to GitHub or share sensitive credentials publicly.

It is recommended to include the following entries in `.gitignore`:

```gitignore
venv/
.env
__pycache__/
*.pyc
```

## Run the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive Swagger API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to test the API endpoints, authentication, project management, proposals, and dashboards.

---

# Main API Endpoints

## Authentication

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/auth/signup` | Register a new user | Public |
| `POST` | `/auth/login` | Login and receive JWT token | Public |

## Projects

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/projects/` | Create a new project | Client |
| `GET` | `/projects/` | View available projects | Public |
| `GET` | `/projects/{project_id}` | View project details | Public |
| `PUT` | `/projects/{project_id}` | Update own project | Project Owner |
| `DELETE` | `/projects/{project_id}` | Delete own project | Project Owner |

## Proposals

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/projects/{project_id}/proposal` | Submit a proposal | Freelancer |
| `GET` | `/projects/my-proposals` | View submitted proposals | Freelancer |
| `GET` | `/projects/{project_id}/proposals` | View proposals for a project | Client |
| `PUT` | `/projects/proposal/{proposal_id}/accept` | Accept a proposal | Client |
| `PUT` | `/projects/proposal/{proposal_id}/reject` | Reject a proposal | Client |
| `DELETE` | `/projects/proposal/{proposal_id}` | Withdraw a proposal | Freelancer |

## Project Status

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `PUT` | `/projects/{project_id}/start` | Start a project | Client |
| `PUT` | `/projects/{project_id}/complete` | Complete a project | Client |
| `PUT` | `/projects/{project_id}/cancel` | Cancel a project | Client |

## Dashboards

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/dashboard/client` | Access client dashboard | Client |
| `GET` | `/dashboard/freelancer` | Access freelancer dashboard | Freelancer |

---

# User Roles

## Client

Clients can:

- Create projects
- View their projects
- Search and filter projects
- Update their own projects
- Delete their own projects
- View proposals received for their projects
- Accept proposals
- Reject proposals
- Start projects
- Complete projects
- Cancel projects
- Access the client dashboard

## Freelancer

Freelancers can:

- Browse available projects
- Search and filter projects
- View project details
- Submit proposals
- View submitted proposals
- Withdraw pending proposals
- Access the freelancer dashboard

---

# Proposal Workflow

The basic proposal workflow is:

```text
Freelancer
    ↓
Browse Projects
    ↓
Select Project
    ↓
Submit Proposal
    ↓
Client Reviews Proposal
    ↓
┌───────────────┐
│               │
Accept        Reject
│               │
↓               ↓
Project       Proposal
Starts        Rejected
```

A freelancer can withdraw a proposal while it is still eligible for withdrawal.

---

# Project Workflow

The basic project workflow is:

```text
Client Creates Project
        ↓
       Open
        ↓
Freelancers Submit Proposals
        ↓
Client Reviews Proposals
        ↓
Client Accepts Proposal
        ↓
Client Starts Project
        ↓
   In Progress
        ↓
    Completed
```

A project may also be cancelled:

```text
Open
  ↓
Cancelled
```

---

# Authentication

The API uses **JWT-based authentication**.

After successful login, the API returns a JWT access token.

The token should be included when accessing protected endpoints.

In Swagger UI, use the **Authorize** button and provide the token in the required format:

```text
Bearer YOUR_JWT_TOKEN
```

Protected endpoints require a valid JWT token.

> **Security:** Never share your JWT access token publicly.

---

# Security

The project implements the following security mechanisms:

- JWT-based authentication
- Password hashing using bcrypt
- Role-based authorization
- Ownership validation
- Input validation using Pydantic
- Protected API endpoints
- Environment variables for sensitive configuration
- `.env` excluded from Git
- Access control based on user roles

### Ownership Validation

Clients can modify or delete only their own projects.

Freelancers can manage only their own submitted proposals.

This prevents users from modifying resources that belong to other users.

---

# API Access Control

The platform uses role-based access control.

| Feature | Client | Freelancer |
|---|:---:|:---:|
| Register/Login | Yes | Yes |
| Browse Projects | Yes | Yes |
| Create Projects | Yes | No |
| Update Own Projects | Yes | No |
| Delete Own Projects | Yes | No |
| Submit Proposals | No | Yes |
| View Own Proposals | No | Yes |
| View Received Proposals | Yes | No |
| Accept Proposals | Yes | No |
| Reject Proposals | Yes | No |
| Withdraw Proposals | No | Yes |
| Start Projects | Yes | No |
| Complete Projects | Yes | No |
| Cancel Projects | Yes | No |
| Client Dashboard | Yes | No |
| Freelancer Dashboard | No | Yes |

---

# API Workflow

The overall platform workflow is:

```text
User Signup
     ↓
Choose Role
     ↓
Client / Freelancer
     ↓
Login
     ↓
JWT Access Token
     ↓
┌───────────────────────┐
│                       │
Client              Freelancer
│                       │
↓                       ↓
Create Project      Browse Projects
│                       │
↓                       ↓
Receive Proposals   Submit Proposal
│                       │
↓                       ↓
Review Proposals    View Proposal Status
│                       │
↓                       │
Accept Proposal ←───────┘
     ↓
Project Starts
     ↓
In Progress
     ↓
Project Completed
```

---

# Internship Project

This project was developed as part of the **Backend Development Internship at Sqrock IT Solutions**.

The project demonstrates the development of a secure RESTful freelancing marketplace backend using modern backend technologies.

The main objectives were to implement:

- User authentication
- JWT authorization
- Role-based access control
- Client and freelancer workflows
- Project management
- Proposal management
- Project status management
- Dashboard APIs
- Database integration
- Secure API design

---

# Future Improvements

Possible future improvements include:

- Online payment integration
- Escrow payment system
- Freelancer profile management
- Client profile management
- Ratings and reviews
- Messaging between clients and freelancers
- Email notifications
- Real-time notifications
- File and document attachments
- Advanced project search
- Skill-based freelancer matching
- AI-powered freelancer recommendations
- AI-powered proposal assistance
- Admin dashboard
- Payment history
- Dispute management
- Automated testing
- Rate limiting
- Production logging
- Docker deployment
- Cloud deployment

---

# License

This project was developed for **educational and internship purposes** as part of the Backend Development Internship at **Sqrock IT Solutions**.

---

# Author

Developed as part of a **Backend Development Internship at Sqrock IT Solutions**.
```