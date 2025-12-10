OpenBank – Cloud-Native Banking System  

A cloud-native banking application built as part of a FullStack and DevOps-focused Agile simulation. 
The project combines frontend banking functionality, a FastAPI backend, MongoDB, and modern DevOps practices including CI/CD, containerization, and monitoring. 

Shape 

Project Vision 

This project simulates the build of a real-world banking platform while applying: 

Agile sprint planning & execution 

Frontend–backend integration 

Secure authentication & transactions 

DevOps automation (CI/CD, Docker, Kubernetes) 

Monitoring & observability 

The goal is learning-by-building, not just delivering features. 

Shape 

Team 

Name 

Role 

Ntando 

DevOps Lead / Project Manager 

Kagiso 

Frontend Lead 

Chuene 

Backend Lead 

Elona 

Frontend / Backend Developer 

Zwavhudi 

Frontend Developer 

Mthobisi 

Frontend Developer 

Jaden 

UI/UX Designer 

Florence 

QA & Documentation 

Elihle 

Agile Project Manager 

Tumi 

Database & Backend Support 

Shape 

Tech Stack 

Frontend 

HTML5 

CSS3 (Flexbox & Grid) 

JavaScript (ES6+) 

Fetch API 

Optional React (DevOps phase extension) 

Backend 

Python 3.9+ 

FastAPI 

Uvicorn 

PyMongo 

JWT (Authentication) 

Bcrypt / Passlib 

Database 

MongoDB 

DevOps & Cloud 

Git & GitHub 

GitHub Actions (CI/CD) 

Docker & Docker Compose 

Kubernetes (Week 3) 

Prometheus & Grafana (Week 4) 

Shape 

Core Features 

Banking Functionality 

✅ User Registration & Login 

✅ JWT Authentication 

✅ Account Dashboard 

✅ Deposit Money 

✅ Withdraw Money (with balance validation) 

✅ Transaction History 

✅ Responsive UI 

Security 

Password hashing 

JWT-protected routes 

Input validation 

CORS configuration 

Shape 

Sprint Timeline 

Week 1 – Planning & Core Build ✅ 

Agile board & user stories 

Frontend pages 

Backend API 

Authentication & transactions 

Local state persistence 

Week 2 – Testing & Containerization (Current) 

Docker & Docker Compose 

API testing (Postman) 

CI pipeline setup 

Code quality improvements 

Week 3 – CI/CD & Deployment 

GitHub Actions pipelines 

Kubernetes deployment 

Infrastructure as Code 

Week 4 – Monitoring & SRE 

Prometheus & Grafana 

SLO definitions 

Final demo & documentation 

Shape 

Project Structure 

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

Shape 

Running the Application (Local) 

Prerequisites 

Python 3.9+ 

MongoDB 

Git 

VS Code (recommended) 

Shape 

1. Start the Backend 

⚠️ Important: Backend must be run from inside the backend/ folder. 

cd backend 

uvicorn main:app --reload 

✅ Backend will run at: 
http://127.0.0.1:8000 

API Docs: 
http://127.0.0.1:8000/docs 

Shape 

2. Start the Frontend 

Option 1 — VS Code Live Server 

Right-click login.html → Open with Live Server 

Option 2 — Python server 

cd frontend 

python -m http.server 3000 

✅ Frontend runs at: 
http://localhost:3000 

Shape 

Key Fixes & Improvements Implemented 

✅ Login now verifies passwords correctly 

✅ Dashboard shows logged-in username & email 

✅ Dynamic account number generation 

✅ Deposit & withdraw pages sync balances 

✅ Overdraft prevention enforced 

✅ Deposits & withdrawals logged correctly 

✅ Transaction history fully synced 

✅ Improved email validation rules 

Shape 

State Persistence 

User session stored in localStorage 

Balance persists during session navigation 

⚠️ Balance resets on browser clear or backend restart 
➡️ MongoDB persistence planned 

Shape 

Docker (Week 2) 

docker-compose up --build 

Services: 

Frontend → localhost:3000 

Backend → localhost:8000 

MongoDB → localhost:27017 

Shape 

API Overview 

Auth 

Method 

Endpoint 

POST 

/api/auth/register 

POST 

/api/auth/login 

Transactions 

| POST | /api/transactions/deposit | 
| POST | /api/transactions/withdraw | 
| GET | /api/transactions/history | 

Shape 

Development Workflow 

Branch from develop 

Commit clearly (feat: add login validation) 

Push to GitHub 

Open Pull Request 

Team review 

Merge after approval 

Shape 

Learning Outcomes 

This project demonstrates: 

Full-stack integration 

Secure API development 

Frontend state management 

Agile team collaboration 

CI/CD automation 

Cloud-native thinking 

Shape 

Support 

Open a GitHub issue 

Contact Ntando (DevOps) 

Contact Elihle (Project Manager) 

Shape 

License 

Educational project – DevOps & Cloud Engineering Simulation 

Shape 

Last Updated: November 2025 

 
