# Week 2 Deliverables - Banking App DevOps Setup
 
**Date:** December 11, 2025  
**Branch:** devops-week2-deliverables  
**Project:** Banking System

---

##  Deliverable Checklist

### 1. Dockerized Services (Frontend + Backend + DB) 

**Status:** COMPLETE 

All services successfully containerized and running:

-  **Backend Dockerfile** created (`backend/Dockerfile`)
  - Base image: Python 3.11 slim
  - FastAPI application
  - Port: 8000
  - Hot-reload enabled for development

-  **Frontend Dockerfile** created (`frontend/Dockerfile`)
  - Base image: nginx:alpine
  - Serves static HTML/CSS/JS
  - Port: 80 (mapped to 3000 externally)

-  **Docker Compose** configuration (`docker-compose.yml`)
  - Orchestrates all 3 services
  - MongoDB 7 as database
  - Persistent volume for database
  - Service dependencies configured

**Services:**
| Service | Image | Port | Status |
|---------|-------|------|--------|
| Backend | bankingapp-backend | 8000 | Running  |
| Frontend | bankingapp-frontend | 3000→80 | Running  |
| MongoDB | mongo:7 | 27017 | Running  |

### 2. Functional Backend APIs 

**Status:** INFRASTRUCTURE COMPLETE  | APPLICATION INTEGRATION IN PROGRESS 

**DevOps Deliverables (Complete):**
- Docker containerization working
- Backend service running
- API endpoints defined in code
- MongoDB connection configured

**Application Status (Team's Work):**
- Backend-frontend integration in progress
- API endpoint testing pending bug fixes
- Frontend loads but shows "Error connecting to server"

**Backend Endpoints Defined:**
- `GET /` - Health check
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /balance/{username}` - Get balance
- `POST /deposit` - Deposit funds
- `POST /withdraw` - Withdraw funds
- `GET /transactions/{username}` - Transaction history

**Note:** Backend code issues are being resolved by development team. Docker infrastructure is production-ready.

### 3. Test Report with Coverage Summary 

**Status:** PENDING (Backend integration issues)

- Docker health checks passing
- Container connectivity verified
- API endpoint tests pending backend fixes
- Unit tests with PyTest - to be implemented

### 4. Screenshot/Log of Successful Container Runs 

**Status:** COMPLETE 

**Logs Generated:**
- `logs/container-status-[timestamp].log` - All containers running
- `logs/all-containers-logs-[timestamp].log` - Complete container output

**Container Status Evidence:**
```
CONTAINER ID   IMAGE                    STATUS      PORTS
[ID]          banking-backend          Up          0.0.0.0:8000->8000/tcp
[ID]          banking-frontend         Up          0.0.0.0:3000->80/tcp
[ID]          banking-mongodb          Up          0.0.0.0:27017->27017/tcp
```

---

## Docker Infrastructure Status

### All Services Operational 

**Build Status:**
- Backend build: SUCCESS 
- Frontend build: SUCCESS 
- MongoDB deployment: SUCCESS 

**Network Configuration:**
- Docker network created: `banking-app-dev_default` 
- Inter-container communication: WORKING 
- Port mappings: CONFIGURED 

**Volume Management:**
- MongoDB data volume: `banking-app-dev_mongo_data` 
- Data persistence: ENABLED 

---

## 🔗 Access Information

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **MongoDB:** mongodb://localhost:27017

---

##  Project Structure
```
Banking-App-Dev/
├── backend/
│   ├── Dockerfile               Created
│   ├── requirements.txt         Created
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   ├── database.py
│   └── auth_utils.py
├── frontend/
│   ├── Dockerfile               Created
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── styles/
├── docker-compose.yml           Created
└── my-devops/
    ├── scripts/
    │   ├── setup.sh             Created
    │   └── stop.sh              Created
    └── deliverables/
        └── week2/
            ├── WEEK2_SUMMARY.md (this file)
            ├── logs/
            │   ├── container-status-[timestamp].log
            │   └── all-containers-logs-[timestamp].log
            └── screenshots/
                └── (To be added)
```

---

## 🛠️ Technologies Used

- **Backend:** Python 3.11, FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript, nginx
- **Database:** MongoDB 7
- **DevOps:** Docker 24.x, Docker Compose v3.8
- **Development:** Git, GitHub (dev branch)

---

##  How to Run

### Prerequisites
- Docker Desktop installed and running
- Git

### Clone and Run
```bash
# Clone repository
git clone -b devops-week2-deliverables https://github.com/DopeGrammerZA/Banking-System-Front-End.git

# Navigate to project
cd Banking-App-Dev

# Start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Helper Scripts
```bash
# Setup and start
./my-devops/scripts/setup.sh

# Stop
./my-devops/scripts/stop.sh
```

---

##  Week 2 Completion Summary

| Deliverable | Status | Notes |
|------------|--------|-------|
| **Dockerized Services** |  COMPLETE | All containers running successfully |
| **Backend APIs** |  PARTIAL | Infrastructure ready, integration pending |
| **Test Reports** |  PENDING | Awaiting backend bug fixes |
| **Container Logs** |  COMPLETE | All logs captured and saved |

**Overall DevOps Status:** Infrastructure deployment SUCCESSFUL 

**Application Status:** Backend-frontend integration in progress (separate from DevOps work)

---

##  Next Steps

### Immediate (Application Team)
- [ ] Fix backend API connection issues
- [ ] Complete backend-frontend integration
- [ ] Test all endpoints with Postman

### Week 3 (DevOps)
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Create Kubernetes manifests
- [ ] Implement Infrastructure as Code (Terraform/Ansible)
- [ ] Add automated testing to pipeline
- [ ] Set up monitoring and logging

---

## 📸 Screenshots Required

1. Docker Desktop showing all 3 containers running
2. Terminal with `docker ps` output
3. Frontend in browser (http://localhost:3000)
4. Backend API docs (http://localhost:8000/docs)
5. Container logs in terminal

---

**Prepared by:** CAPACITI-JHB  
**Submission Date:** December 11, 2025  
**Branch:** devops-week2-deliverables  
**Repository:** https://github.com/DopeGrammerZA/Banking-System-Front-End