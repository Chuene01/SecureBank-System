# Banking App Infrastructure as Code (Terraform)

This directory contains Terraform configuration files to deploy the Banking App to Kubernetes.

## Prerequisites

- Terraform >= 1.0
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- kubectl configured
- Docker

## File Structure

```
terraform/
├── main.tf           # Main infrastructure configuration
├── variables.tf      # Variable definitions
├── outputs.tf        # Output values
├── terraform.tfvars  # Variable values (create this)
└── README.md         # This file
```

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Create terraform.tfvars

Create a `terraform.tfvars` file with your configuration:

```hcl
namespace          = "banking-app"
environment        = "production"
backend_replicas   = 3
frontend_replicas  = 2
mongodb_storage_size = "5Gi"
```

### 3. Plan the deployment

```bash
terraform plan
```

### 4. Apply the infrastructure

```bash
terraform apply
```

Type `yes` when prompted.

### 5. View outputs

```bash
terraform output
```

## What Gets Deployed

- **Kubernetes Namespace**: `banking-app`
- **MongoDB**:
  - 1 replica
  - 5Gi persistent storage
  - ClusterIP service on port 27017
- **Backend**:
  - 3 replicas (configurable)
  - LoadBalancer service on port 8000 (NodePort 30800)
  - Auto-scaling ready
- **Frontend**:
  - 2 replicas (configurable)
  - LoadBalancer service on port 80 (NodePort 30080)
  - Auto-scaling ready
- **ConfigMap**: Application configuration

## Accessing the Application

After deployment:

- **Frontend**: http://localhost:30080
- **Backend**: http://localhost:30800
- **MongoDB**: mongodb://localhost:27017 (from within cluster)

## Scaling

To change the number of replicas:

```bash
terraform apply -var="backend_replicas=5" -var="frontend_replicas=3"
```

## Destroying Infrastructure

```bash
terraform destroy
```

## Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `namespace` | Kubernetes namespace | `banking-app` |
| `environment` | Environment name | `production` |
| `backend_replicas` | Number of backend pods | `3` |
| `frontend_replicas` | Number of frontend pods | `2` |
| `mongodb_storage_size` | MongoDB PVC size | `5Gi` |
| `backend_image` | Backend Docker image | `ghcr.io/...` |
| `frontend_image` | Frontend Docker image | `ghcr.io/...` |

## Troubleshooting

### Check deployment status

```bash
terraform show
```

### View state

```bash
terraform state list
```

### Refresh state

```bash
terraform refresh
```

## CI/CD Integration

This Terraform configuration can be integrated with GitHub Actions:

```yaml
- name: Terraform Apply
  run: |
    cd terraform
    terraform init
    terraform apply -auto-approve
```

## Notes

- Persistent volumes are created for MongoDB data
- Services are configured with LoadBalancer type (use NodePort for Minikube)
- Health checks and resource limits are configured
- All resources are labeled for easy identification