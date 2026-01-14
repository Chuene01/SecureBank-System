# OpenBank – Cloud-Native Banking System

A cloud-native banking application built as part of a FullStack and DevOps-focused Agile simulation. The project combines frontend banking functionality, a FastAPI backend, MongoDB, and modern DevOps practices including CI/CD, containerization, and monitoring.

---

##  Project Vision

This project simulates the build of a real-world banking platform while applying:

- Agile sprint planning & execution
- Frontend–backend integration
- Secure authentication & transactions
- DevOps automation (CI/CD, Docker, Kubernetes)
- Monitoring & observability 

**The goal is learning-by-building, not just delivering features.**

---

##  Team

| Name | Role |
|------|------|
| Ntando | DevOps Lead / Project Manager |
| Kagiso | Frontend Lead |
| Chuene | Backend Lead / Frontend Developer |
| Elona | Frontend / Backend Developer |
| Zwavhudi | Frontend Developer |
| Jaden | UI/UX Designer |
| Florence | QA & Documentation |
| Elihle | Agile Project Manager |
| Tumi | Database & Backend Support |

---

## Tech Stack

### Frontend
- HTML5
- CSS3 (Flexbox & Grid)
- JavaScript (ES6+)
- Fetch API
- Deployed with Vercel

### Backend
- Python 3.9+
- FastAPI
- Uvicorn
- PyMongo
- JWT-based authentication
- Argon2 password hashing (Passlib)

### Database
- MongoDB Atlas (Cloud)

### DevOps & Cloud
- Git & GitHub
- GitHub Actions (CI/CD)
- Docker & Docker Compose
- Kubernetes (Week 3)
- Prometheus & Grafana (Week 4)

---

##  Core Features

### Banking Functionality
- User registration and login
- JWT-based authentication
- Account dashboard with live balance display
- Deposit funds with server-side balance updates
- Withdraw funds with balance validation
- Transaction history (deposits & withdrawals)
- Responsive, mobile-friendly user interface

### Security
- Password hashing using Argon2
- JWT-based authentication with protected API routes
- Secure token handling via Authorization Bearer headers
- Input validation using Pydantic schemas
- CORS configuration for frontend–backend communication

---

##  Sprint Timeline

### Week 1 – Planning & Core Build 
- Agile board & user stories
- Frontend pages
- Backend API
- Authentication & transactions
- Local state persistence

### Week 2 – Testing & Containerization (Current)
- Docker & Docker Compose
- API testing (Postman)
- CI pipeline setup
- Code quality improvements

### Week 3 – CI/CD & Deployment
- GitHub Actions pipelines
- Kubernetes deployment
- Infrastructure as Code

### Week 4 – Monitoring & SRE
- Prometheus & Grafana
- SLO definitions
- Final demo & documentation

---

##  Project Structure

```text
BANKING-SYSTEM-FRONT-END/
│
├── backend/                         # FastAPI backend
│   ├── __pycache__/
│   ├── venv/                        # Local Python virtual environment
│   ├── auth_utils.py                # JWT auth helpers
│   ├── auth.py                      # Authentication logic
│   ├── crud.py                      # Database CRUD operations
│   ├── database.py                  # MongoDB Atlas connection
│   ├── main.py                      # FastAPI entry point
│   ├── models.py                   # Database models
│   ├── schemas.py                  # Pydantic schemas
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend Docker image
│   ├── start.sh                    # Backend startup script
│   ├── package.json                # Backend scripts/config (if used)
│   └── README.md                   # Backend documentation
│
├── frontend/                        # Frontend (HTML/CSS/JS)
│   ├── css/                         # Stylesheets
│   ├── js/
│   │   ├── config.js                # API base URL & config
│   │   └── index.js                 # Shared frontend logic
│   ├── pages/
│   │   ├── login.html               # Login page
│   │   ├── register.html            # Registration page
│   │   ├── dashboard.html           # User dashboard
│   │   ├── deposit.html             # Deposit page
│   │   ├── withdraw.html            # Withdrawal page
│   │   └── history.html             # Transaction history
│   └── README.md                   # Frontend documentation
│
├── UI Screenshots/                  # UI evidence for deliverables
│   ├── Dashboard 1.PNG
│   ├── Dashboard 2.PNG
│   ├── Deposit money.PNG
│   ├── Withdraw money.PNG
│   ├── Sign in page.PNG
│   ├── Registration Page.PNG
│   └── Transaction history.PNG
│
├── devops/
│   ├── docker/                      # DevOps Docker resources
│   └── .gitignore
│
├── kubernetes/                      # Kubernetes manifests (Week 3)
├── terraform/                       # Infrastructure as Code (optional)
│
├── nginx.conf                       # Nginx config for frontend
├── Dockerfile                       # Frontend Docker image
├── docker-compose.yml               # Local multi-container setup
├── vercel.json                      # Vercel routing configuration
├── index.html                       # Landing / home page
├── README.md                        # Main project documentation
└── .env.example                     # Environment variable template
```

---

##  Running the Application (Local)

### Prerequisites
- Python 3.9+
- MongoDB Atlas (cloud database)
- Git
- VS Code
- VS Code Live Server extension

### 1. Start the Backend

 **Important:** Backend must be run from inside the `backend/` folder.

```bash
cd backend
uvicorn main:app --reload
```

 **Backend will run at:**
- API root: http://127.0.0.1:8000
- Interactive API Docs (Swagger UI): http://127.0.0.1:8000/docs

### 2. Start the Frontend

**Option 1 — VS Code Live Server**
- Right-click `login.html` → Open with Live Server

 **Frontend runs at:** http://127.0.0.1:5500/

---

##  Key Fixes & Improvements Implemented

- Corrected login authentication flow with secure password verification
- Ensured dashboard displays the authenticated user’s username and email
- Implemented dynamic account number generation based on user identity
- Synced deposit and withdrawal balances across dashboard and transaction pages
- Enforced overdraft protection with server-side balance validation
- Logged deposits and withdrawals reliably in MongoDB
- Fully synchronized transaction history with backend data
- Improved email-based login validation and error handling

---

##  State Persistence

- User authentication state is maintained using a JWT stored in localStorage
- Account balance and transactions are persisted in MongoDB Atlas and retrieved via secured API endpoints
- Frontend state (e.g. balance display) is refreshed from the backend on page load to ensure consistency

 **Note:** Clearing the browser storage logs the user out but does not reset account data
MongoDB serves as the single source of truth for balances and transaction history

---

##  Docker

```bash
docker-compose up --build
```

## Services

### Local Development
- Backend API → http://localhost:8000 (FastAPI)
- Frontend → Static HTML/CSS/JS served locally or via Nginx
- Database → MongoDB Atlas (cloud-hosted)

### Production
- Frontend → Vercel
- Backend → Render
- Database → MongoDB Atlas

---

## API Overview

### Auth

| Method | Endpoint |
|--------|----------|
| POST | `/register` |
| POST | `/login` |

### Account

| Method | Endpoint |
|--------|----------|
| GET | `/profile` |
| GET | `/balance` |

### Transactions

| Method | Endpoint |
|--------|----------|
| POST | `/deposit` |
| POST | `/withdraw` |
| GET | `/transactions` |

---

##  Development Workflow

1. Branch from `develop`
2. Commit clearly (`feat: add login validation`)
3. Push to GitHub
4. Open Pull Request
5. Team review
6. Merge after approval

---

##  Learning Outcomes

This project demonstrates:

- Full-stack integration
- Secure API development
- Frontend state management
- Agile team collaboration
- CI/CD automation
- Cloud-native thinking

---

##  License

This project was developed for educational purposes as part of a DevOps & Cloud Engineering simulation.
It is not intended for commercial use.

---

##  Backlogs
<img width="1600" height="704" alt="image" src="https://github.com/user-attachments/assets/7ac1ef1f-c46f-4249-b2c3-5472c55ca7a5" />

Backlog was originally managed in a separate repository and is referenced for traceability.

Done by Thubelihle Titi

---

**Last Updated:** January 2026


