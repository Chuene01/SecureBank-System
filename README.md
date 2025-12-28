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
| Chuene | Backend Lead |
| Elona | Frontend / Backend Developer |
| Zwavhudi | Frontend Developer |
| Mthobisi | Frontend Developer |
| Jaden | UI/UX Designer |
| Florence | QA & Documentation |
| Elihle | Agile Project Manager |
| Tumi | Database & Backend Support |

---

##  Tech Stack

### Frontend
- HTML5
- CSS3 (Flexbox & Grid)
- JavaScript (ES6+)
- Fetch API
- Optional React (DevOps phase extension)

### Backend
- Python 3.9+
- FastAPI
- Uvicorn
- PyMongo
- JWT (Authentication)
- Bcrypt / Passlib

### Database
- MongoDB

### DevOps & Cloud
- Git & GitHub
- GitHub Actions (CI/CD)
- Docker & Docker Compose
- Kubernetes (Week 3)
- Prometheus & Grafana (Week 4)

---

##  Core Features

### Banking Functionality
-  User Registration & Login
-  JWT Authentication
-  Account Dashboard
-  Deposit Money
-  Withdraw Money (with balance validation)
-  Transaction History
-  Responsive UI

### Security
- Password hashing
- JWT-protected routes
- Input validation
- CORS configuration

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

```
project-folder/
│
├── backend/
│   ├── main.py                # FastAPI entry point
│   ├── app/
│   │   ├── routes/            # API routes
│   │   ├── models/            # Database models
│   │   ├── middleware/        # JWT verification
│   │   └── config/            # MongoDB config
│   └── requirements.txt
│
├── frontend/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── deposit.html
│   ├── withdraw.html
│   ├── history.html
│   ├── styles.css
│   └── js/
│       ├── api.js
│       ├── auth.js
│       └── utils.js
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── docs/
│   ├── architecture/
│   ├── guides/
│   └── screenshots/
│
├── .github/workflows/
│   └── ci.yml
│
├── README.md
└── .env.example
```

---

##  Running the Application (Local)

### Prerequisites
- Python 3.9+
- MongoDB
- Git
- VS Code (recommended)

### 1. Start the Backend

 **Important:** Backend must be run from inside the `backend/` folder.

```bash
cd backend
uvicorn main:app --reload
```

 **Backend will run at:**
- Application: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

### 2. Start the Frontend

**Option 1 — VS Code Live Server**
- Right-click `login.html` → Open with Live Server

**Option 2 — Python server**
```bash
cd frontend
python -m http.server 3000
```

 **Frontend runs at:** http://localhost:3000

---

##  Key Fixes & Improvements Implemented

-  Login now verifies passwords correctly
-  Dashboard shows logged-in username & email
-  Dynamic account number generation
-  Deposit & withdraw pages sync balances
-  Overdraft prevention enforced
-  Deposits & withdrawals logged correctly
-  Transaction history fully synced
-  Improved email validation rules

---

##  State Persistence

- User session stored in `localStorage`
- Balance persists during session navigation

 **Note:** Balance resets on browser clear or backend restart  
 MongoDB persistence planned

---

##  Docker (Week 2)

```bash
docker-compose up --build
```

**Services:**
- Frontend → `localhost:3000`
- Backend → `localhost:8000`
- MongoDB → `localhost:27017`

---

##  API Overview

### Auth

| Method | Endpoint |
|--------|----------|
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |

### Transactions

| Method | Endpoint |
|--------|----------|
| POST | `/api/transactions/deposit` |
| POST | `/api/transactions/withdraw` |
| GET | `/api/transactions/history` |

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

##  Support

- Open a GitHub issue
- Contact Ntando (DevOps)
- Contact Elihle (Project Manager)

---

##  License

Educational project – DevOps & Cloud Engineering Simulation

---

**Last Updated:** November 2025

# Week 3 Complete
