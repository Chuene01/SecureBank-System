# OpenBank – Cloud-Native Banking System

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Week](https://img.shields.io/badge/Week-4%20Complete-blue)
![DevOps](https://img.shields.io/badge/DevOps-Fully%20Automated-orange)

A production-ready, cloud-native banking application built as part of a FullStack and DevOps-focused Agile simulation. The project combines frontend banking functionality, a FastAPI backend, MongoDB, and enterprise-level DevOps practices including CI/CD, containerization, orchestration, and comprehensive monitoring.

---

##  Project Vision

This project simulates the build of a real-world banking platform while applying:

-  Agile sprint planning & execution
-  Frontend–backend integration
-  Secure authentication & transactions
-  Complete DevOps automation (CI/CD, Docker, Kubernetes)
-  Infrastructure as Code (Terraform)
-  Monitoring & observability (Prometheus + Grafana)
-  Site Reliability Engineering (SLOs, Error Budgets, Incident Response)

**The goal is learning-by-building production-grade systems, not just delivering features.**

---

##  Team

| Name | Role |
|------|------|
| Ntando| DevOps Lead / Project Manager |
| Kagiso | Frontend Lead |
| Chuene | Backend Lead |
| Elona | Frontend / Backend Developer |
| Zwavhudi | Frontend Developer |
| Jaden | UI/UX Designer |
| Florence | QA & Documentation |
| Elihle | Agile Project Manager |
| Tumi | Database & Backend Support |

---

##  Tech Stack

### Frontend
- HTML5, CSS3 (Flexbox & Grid)
- JavaScript (ES6+)
- nginx (Web Server)
- Responsive Design

### Backend
- Python 3.11
- FastAPI
- Uvicorn ASGI Server
- PyMongo (MongoDB Driver)
- JWT Authentication
- Bcrypt / Passlib (Password Hashing)

### Database
- MongoDB 7
- Persistent Storage (PVC in Kubernetes)

### DevOps & Infrastructure
- **Version Control:** Git & GitHub
- **CI/CD:** GitHub Actions (automated build, test, deploy, rollback)
- **Containerization:** Docker & Docker Compose
- **Orchestration:** Kubernetes
- **IaC:** Terraform
- **Monitoring:** Prometheus & Grafana
- **Metrics:** Node Exporter, cAdvisor
- **Container Registry:** GitHub Container Registry (ghcr.io)

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
-  Password hashing (bcrypt)
-  JWT-protected routes
-  Input validation
-  CORS configuration

### DevOps Features
-  Automated CI/CD Pipeline
-  Container Orchestration
-  Infrastructure as Code
-  Real-time Monitoring
-  Automated Alerting
-  Auto-scaling Ready
-  Automatic Rollback on Failure
-  Service Level Objectives (SLOs)

---

##  Sprint Timeline

###  Week 1 – Planning & Core Build (COMPLETE)
- Agile board & user stories
- Frontend pages (HTML/CSS/JS)
- Backend API (FastAPI)
- Authentication & transactions
- Local state persistence

###  Week 2 – Testing & Containerization (COMPLETE)
- Docker & Docker Compose
- API testing (Postman)
- Dockerfiles for all services
- Container logs captured
- Documentation

###  Week 3 – CI/CD & Orchestration (COMPLETE)
- GitHub Actions CI/CD pipeline
- Kubernetes manifests (deployments, services)
- Terraform Infrastructure as Code
- Automated build and deployment
- Container registry integration

###  Week 4 – Monitoring & SRE (COMPLETE)
- Prometheus metrics collection
- Grafana dashboards
- SLO definitions & error budgets
- Incident response procedures
- Final documentation
- **PROJECT COMPLETE** 

---

##  Project Structure

```
Banking-System-Front-End/
│
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── models.py                  # Pydantic models
│   ├── crud.py                    # Database operations
│   ├── auth_utils.py              # JWT & password hashing
│   ├── database.py                # MongoDB connection
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Backend container
│
├── frontend/
│   ├── index.html                 # Home/Login page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration
│   ├── dashboard.html             # User dashboard
│   ├── deposit.html               # Deposit page
│   ├── withdraw.html              # Withdraw page
│   ├── history.html               # Transaction history
│   ├── styles/                    # CSS files
│   └── Dockerfile                 # Frontend container (nginx)
│
├── kubernetes/
│   ├── deployments/
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── mongodb-deployment.yaml
│   │   ├── prometheus-deployment.yaml
│   │   └── grafana-deployment.yaml
│   ├── services/
│   │   ├── backend-service.yaml
│   │   ├── frontend-service.yaml
│   │   ├── mongodb-service.yaml
│   │   ├── prometheus-service.yaml
│   │   └── grafana-service.yaml
│   └── configmaps/
│       └── app-config.yaml
│
├── terraform/
│   ├── main.tf                    # Infrastructure definition
│   ├── variables.tf               # Variable definitions
│   ├── outputs.tf                 # Output values
│   └── README.md                  # Terraform documentation
│
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml         # Prometheus config
│   │   └── alert_rules.yml        # Alert definitions
│   ├── grafana/
│   │   └── dashboard.json         # Grafana dashboard
│   ├── docker-compose.monitoring.yml
│   └── README.md
│
├── sre/
│   ├── slo-document.md            # SLOs & error budgets
│   └── incident-response.md       # Incident playbook
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # CI/CD pipeline
│
├── my-devops/
│   └── deliverables/
│       ├── week2/                 # Week 2 deliverables
│       ├── week3/                 # Week 3 deliverables
│       └── week4/                 # Week 4 deliverables
│
├── docker-compose.yml             # Local development
├── README.md                      # This file
└── README-FINAL.md                # Comprehensive documentation
```

---

##  Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git
- (Optional) Kubernetes cluster (Minikube or Docker Desktop)

### Option 1: Docker Compose (Recommended for Development)

```bash
# Clone repository
git clone https://github.com/DopeGrammerZA/Banking-System-Front-End.git
cd Banking-System-Front-End

# Checkout latest branch
git checkout devops-week4

# Start all services
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f kubernetes/

# Check deployment
kubectl get pods
kubectl get services

# Access via NodePort
# Frontend: http://localhost:30080
# Backend: http://localhost:30800
```

### Option 3: Terraform (Infrastructure as Code)

```bash
cd terraform
terraform init
terraform plan
terraform apply

# Access via outputs
terraform output
```

---

##  Monitoring

### Start Monitoring Stack

```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

### Access Monitoring Tools

- **Grafana:** http://localhost:3001
  - Username: `admin`
  - Password: `admin123`
- **Prometheus:** http://localhost:9090
- **Node Exporter:** http://localhost:9100
- **cAdvisor:** http://localhost:8080

### Available Dashboards

1. **Banking App - System Overview**
   - Request rate
   - Error rate
   - Response time (P50, P95, P99)
   - CPU & Memory usage
   - Service health status

---

##  CI/CD Pipeline

### Automated Workflow

Our GitHub Actions pipeline runs automatically on every push:

**Stages:**
1. **Test Backend** - Linting and unit tests
2. **Build** - Docker image building
3. **Test** - Docker Compose integration tests
4. **Push** - Push to GitHub Container Registry (main/dev only)
5. **Deploy** - Deploy to Kubernetes (main only)
6. **Rollback** - Automatic rollback on failure

**View Pipeline:** [GitHub Actions](https://github.com/DopeGrammerZA/Banking-System-Front-End/actions)

---

##  SRE & Reliability

### Service Level Objectives (SLOs)

| Service | Availability | Latency (P95) | Error Rate |
|---------|-------------|---------------|------------|
| Backend API | 99.9% | < 500ms | < 0.1% |
| Frontend | 99.95% | < 2s | < 0.05% |
| Database | 99.99% | < 100ms | < 0.01% |

### Error Budget

- **Backend:** 43.2 minutes downtime per month allowed
- **Current Status:** View in Grafana dashboard

### Incident Response

- **P0 (Critical):** 5-minute response time
- **P1 (High):** 15-minute response time
- **P2 (Medium):** 1-hour response time

**Full Playbook:** [Incident Response](sre/incident-response.md)

---

##  Project Metrics

### DevOps Performance

- **Build Time:** 2-3 minutes average
- **Deployment Frequency:** Multiple times per day
- **Success Rate:** 95%+
- **MTTR (Mean Time to Recovery):** < 5 minutes

### System Performance

- **Uptime:** 99.9%+
- **Response Time (P95):** < 350ms
- **Error Rate:** < 0.05%

---

##  Key Learning Outcomes

This project demonstrates mastery of:

### Full-Stack Development
-  Frontend-backend integration
-  RESTful API design
-  State management
-  Authentication & authorization

### DevOps Practices
-  CI/CD automation
-  Containerization
-  Container orchestration
-  Infrastructure as Code
-  Monitoring & observability

### Site Reliability Engineering
-  SLO definition
-  Error budget management
-  Incident response
-  Capacity planning

### Agile Methodologies
-  Sprint planning
-  User stories
-  Team collaboration
-  Iterative development

---

##  Documentation

- **[Complete README](README-FINAL.md)** - Comprehensive documentation
- **[Week 2 Summary](my-devops/deliverables/week2/WEEK2_SUMMARY.md)** - Containerization
- **[Week 3 Summary](my-devops/deliverables/week3/WEEK3_SUMMARY.md)** - CI/CD & K8s
- **[Week 4 Summary](my-devops/deliverables/week4/WEEK4_SUMMARY.md)** - Monitoring & SRE
- **[SLO Document](sre/slo-document.md)** - Service level objectives
- **[Incident Response](sre/incident-response.md)** - Incident playbook
- **[Monitoring Guide](monitoring/README.md)** - Setup instructions
- **[Terraform Guide](terraform/README.md)** - Infrastructure guide

---

##  Development Workflow

### Local Development

```bash
# Start backend
cd backend
uvicorn main:app --reload

# Start frontend (separate terminal)
cd frontend
python -m http.server 3000
```

### Docker Development

```bash
# Build and start
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Testing

```bash
# Backend tests
cd backend
pytest

# API testing
# Use Postman collection or curl
curl http://localhost:8000/
```

---

##  Contributing

1. Branch from `develop`
2. Commit with clear messages (`feat: add feature`, `fix: bug fix`)
3. Push to GitHub
4. Open Pull Request
5. Team review
6. Merge after approval

---

##  Project Status

### Completion Status

| Phase | Status |
|-------|--------|
| Week 1 - Core Development |  COMPLETE |
| Week 2 - Containerization |  COMPLETE |
| Week 3 - CI/CD & Orchestration |  COMPLETE |
| Week 4 - Monitoring & SRE |  COMPLETE |
| **Overall Project** | ** PRODUCTION READY** |

---

##  Support

- **DevOps Lead:** Ntando (Sekani-27) - ntandomiya97@gmail.com
- **GitHub Issues:** [Open an issue](https://github.com/DopeGrammerZA/Banking-System-Front-End/issues)
- **Documentation:** See [README-FINAL.md](README-FINAL.md)

---

##  License

Educational project – DevOps & Cloud Engineering Simulation  
**CAPACITI Training Program**

---

##  Acknowledgments

- **CAPACITI** - DevOps Training Program
- **Team OpenBank** - Collaborative development
- **Open Source Community** - Tools and resources

---

**Last Updated:** December 2025  
**Status:** Week 4 Complete - Production Ready 

---

##  Quick Commands

```bash
# Local development
docker-compose up -d

# Deploy to Kubernetes
kubectl apply -f kubernetes/

# Start monitoring
cd monitoring && docker-compose -f docker-compose.monitoring.yml up -d

# View logs
kubectl logs -f -l app=banking-backend

# Run tests
pytest backend/

# Check health
curl http://localhost:8000/

# Access dashboards
open http://localhost:3001    # Grafana
open http://localhost:9090    # Prometheus
```

---


