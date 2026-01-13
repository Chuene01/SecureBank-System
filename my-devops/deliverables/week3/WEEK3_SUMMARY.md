# Week 3 Deliverables - CI/CD & Deployment Automation

**Student:** Ntando, Kagiso, Florence & Tumelo 
**Date:** December 11-13, 2025  
**Branch:** devops-week3  
**Project:** Banking System - DevOps Implementation

---

##  Deliverable Checklist

### 1. CI/CD Pipeline YAML File in Repo 

**Status:** COMPLETE 

**File:** `.github/workflows/ci-cd.yml`

**Pipeline Features:**
-  Automated build on push to main, dev, and devops-week3 branches
-  Automated testing for backend (Python linting, unit tests)
-  Docker image building for backend and frontend
-  Docker Compose integration testing
-  Container registry push (GitHub Container Registry)
-  Kubernetes deployment automation
-  Automatic rollback on deployment failure

**Pipeline Jobs:**
1. **test-backend**: Python linting and testing
2. **build**: Docker image building and compose testing
3. **push**: Push images to GitHub Container Registry
4. **deploy**: Deploy to Kubernetes cluster
5. **rollback**: Automatic rollback on failure

### 2. Automated Build + Deploy Logs from GitHub Actions 
**Status:** COMPLETE 

**Pipeline Run:** Workflow #4 - Success  
**Date:** December 15, 2025  
**Commit:** 96113dd  
**Duration:** ~2 minutes  

**Logs Available:**
- Complete workflow logs (downloaded)
- Build job logs (screenshot)
- Test job logs (screenshot)

### 3. Kubernetes Manifests for Services, Pods, and Deployments 

**Status:** COMPLETE 

**Files Created:**

#### Deployments (`kubernetes/deployments/`)
-  `backend-deployment.yaml` - Backend FastAPI application (3 replicas)
-  `frontend-deployment.yaml` - Frontend nginx application (2 replicas)
-  `mongodb-deployment.yaml` - MongoDB database (1 replica + PVC)

#### Services (`kubernetes/services/`)
-  `backend-service.yaml` - LoadBalancer on port 8000 (NodePort 30800)
-  `frontend-service.yaml` - LoadBalancer on port 80 (NodePort 30080)
-  `mongodb-service.yaml` - ClusterIP on port 27017

#### ConfigMaps (`kubernetes/configmaps/`)
-  `app-config.yaml` - Application configuration (MongoDB URL, environment)

**Kubernetes Features:**
- Health checks (liveness & readiness probes)
- Resource limits and requests
- Persistent storage for MongoDB (5Gi)
- Auto-scaling ready
- Service discovery configured
- Environment-specific configurations

### 4. Infrastructure Defined Using IaC Script (Terraform) 

**Status:** COMPLETE 

**Tool:** Terraform

**Files Created:**
-  `terraform/main.tf` - Main infrastructure configuration
-  `terraform/variables.tf` - Variable definitions
-  `terraform/outputs.tf` - Output values
-  `terraform/README.md` - Documentation
-  `terraform/.gitignore` - Git ignore rules

**Infrastructure Components:**
- Kubernetes namespace (`banking-app`)
- MongoDB deployment with persistent volume
- Backend deployment (configurable replicas)
- Frontend deployment (configurable replicas)
- All Kubernetes services
- ConfigMaps for application configuration
- Resource management and scaling policies

**Terraform Features:**
-  Declarative infrastructure definition
-  Variable-driven configuration
-  Reusable and maintainable
-  Version controlled
-  Supports multiple environments
-  Automatic dependency management

---

##  DevOps Architecture

### CI/CD Pipeline Flow

```
Developer Push → GitHub
       ↓
GitHub Actions Triggered
       ↓
1. Run Tests (Backend linting, unit tests)
       ↓
2. Build Docker Images (Backend + Frontend)
       ↓
3. Test Docker Compose Locally
       ↓
4. Push Images to Container Registry
       ↓
5. Deploy to Kubernetes Cluster
       ↓
6. Verify Deployment
       ↓
Success  / Failure → Auto Rollback 
```

### Kubernetes Architecture

```
┌─────────────────────────────────────────┐
│         LoadBalancer Services           │
│  Frontend (30080)  |  Backend (30800)   │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           Kubernetes Cluster            │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  Frontend    │    │   Backend    │  │
│  │  (2 Pods)    │ →  │  (3 Pods)    │  │
│  └──────────────┘    └──────────────┘  │
│                            ↓            │
│                     ┌──────────────┐   │
│                     │   MongoDB    │   │
│                     │   (1 Pod)    │   │
│                     │   + PVC      │   │
│                     └──────────────┘   │
└─────────────────────────────────────────┘
```

---

##  Technologies Used

### CI/CD
- **GitHub Actions** - Automated workflows
- **Docker** - Container runtime
- **Docker Compose** - Multi-container orchestration
- **GitHub Container Registry** - Image storage

### Orchestration
- **Kubernetes** - Container orchestration
- **kubectl** - Kubernetes CLI

### Infrastructure as Code
- **Terraform** - Infrastructure provisioning
- **HCL** - HashiCorp Configuration Language

### Application Stack
- **Backend:** Python 3.11, FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript, nginx
- **Database:** MongoDB 7

---

##  Project Structure

```
Banking-App-Week3/
├── .github/
│   └── workflows/
│       └── ci-cd.yml               CI/CD Pipeline
├── backend/
│   ├── Dockerfile                  Backend container
│   ├── requirements.txt            Python dependencies
│   └── main.py
├── frontend/
│   ├── Dockerfile                  Frontend container
│   └── index.html
├── kubernetes/
│   ├── deployments/
│   │   ├── backend-deployment.yaml    
│   │   ├── frontend-deployment.yaml   
│   │   └── mongodb-deployment.yaml    
│   ├── services/
│   │   ├── backend-service.yaml       
│   │   ├── frontend-service.yaml      
│   │   └── mongodb-service.yaml       
│   └── configmaps/
│       └── app-config.yaml            
├── terraform/
│   ├── main.tf                     Infrastructure code
│   ├── variables.tf                Variables
│   ├── outputs.tf                  Outputs
│   ├── README.md                   Documentation
│   └── .gitignore                 
├── docker-compose.yml              Local development
└── my-devops/
    └── deliverables/
        └── week3/
            ├── WEEK3_SUMMARY.md    This file
            └── logs/              (To be populated)
```

---

##  How to Deploy

### Using Kubernetes Manifests

```bash
# Apply all manifests
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods -n default
kubectl get services -n default

# Access application
# Frontend: http://localhost:30080
# Backend: http://localhost:30800
```

### Using Terraform

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan deployment
terraform plan

# Apply infrastructure
terraform apply

# View outputs
terraform output
```

### Using CI/CD Pipeline

```bash
# Push code to trigger pipeline
git add .
git commit -m "Deploy to production"
git push origin main

# Monitor pipeline
# Go to: https://github.com/DopeGrammerZA/Banking-System-Front-End/actions
```

---

##  Week 3 Completion Status

| Deliverable | Status | Evidence |
|------------|--------|----------|
| **CI/CD Pipeline YAML** |  COMPLETE | `.github/workflows/ci-cd.yml` |
| **Automated Build Logs** |  PENDING | Requires push to GitHub |
| **Kubernetes Manifests** |  COMPLETE | `kubernetes/` directory |
| **IaC Script (Terraform)** |  COMPLETE | `terraform/` directory |

**Overall Status:** Infrastructure code COMPLETE  
**Next Step:** Push to GitHub and capture workflow logs

---

##  Automatic Rollback Implementation

The CI/CD pipeline includes automatic rollback:

```yaml
rollback:
  needs: deploy
  runs-on: ubuntu-latest
  if: failure()
  
  steps:
    - name: Rollback deployment
      run: |
        kubectl rollout undo deployment/backend-deployment
        kubectl rollout undo deployment/frontend-deployment
```

**Rollback Triggers:**
- Deployment failure
- Health check failure
- Kubernetes resource errors

---

##  Deployment Metrics

### Resource Allocation

| Service | Replicas | CPU Request | Memory Request | CPU Limit | Memory Limit |
|---------|----------|-------------|----------------|-----------|--------------|
| Backend | 3 | 250m | 256Mi | 500m | 512Mi |
| Frontend | 2 | 100m | 128Mi | 200m | 256Mi |
| MongoDB | 1 | 250m | 512Mi | 500m | 1Gi |

### Storage
- MongoDB Persistent Volume: 5Gi

---

##  Testing Strategy

### CI Pipeline Tests
- Code linting (flake8)
- Unit tests (pytest)
- Docker build verification
- Docker Compose integration tests
- Kubernetes deployment validation

### Manual Testing
```bash
# Test backend health
curl http://localhost:30800/

# Test frontend
curl http://localhost:30080/

# Check pod status
kubectl get pods

# View logs
kubectl logs -l app=banking-backend
```

---

## Next Steps

### Immediate
1. Push code to GitHub
2. Capture CI/CD workflow logs
3. Test Kubernetes deployment
4. Document deployment results

### Future Enhancements
- Add monitoring (Prometheus + Grafana)
- Implement auto-scaling (HPA)
- Add staging environment
- Set up log aggregation (ELK stack)
- Implement secret management (Vault)
- Add integration tests in CI pipeline

---

##  Resources

- **Repository:** https://github.com/DopeGrammerZA/Banking-System-Front-End
- **Branch:** devops-week3
- **CI/CD:** GitHub Actions
- **Container Registry:** GitHub Container Registry (ghcr.io)
- **Orchestration:** Kubernetes
- **IaC:** Terraform

---

**Prepared by:** Ntando, Tumelo, Kagiso & Florence
**Submission Date:** December 13, 2025  
**Week:** 3 - CI/CD & Deployment Automation  
**Status:** Infrastructure Complete
