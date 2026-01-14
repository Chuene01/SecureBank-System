# Terraform Variables for Banking App Infrastructure

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "docker_host" {
  description = "Docker host URL"
  type        = string
  default     = "unix:///var/run/docker.sock"
}

variable "namespace" {
  description = "Kubernetes namespace for the application"
  type        = string
  default     = "banking-app"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "mongodb_database" {
  description = "MongoDB database name"
  type        = string
  default     = "bankingdb"
}

variable "mongodb_storage_size" {
  description = "Storage size for MongoDB persistent volume"
  type        = string
  default     = "5Gi"
}

variable "backend_image" {
  description = "Docker image for backend"
  type        = string
  default     = "ghcr.io/dopegrammmerza/banking-system-front-end-backend:latest"
}

variable "frontend_image" {
  description = "Docker image for frontend"
  type        = string
  default     = "ghcr.io/dopegrammmerza/banking-system-front-end-frontend:latest"
}

variable "backend_replicas" {
  description = "Number of backend replicas"
  type        = number
  default     = 3
}

variable "frontend_replicas" {
  description = "Number of frontend replicas"
  type        = number
  default     = 2
}