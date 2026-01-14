# Terraform Outputs for Banking App Infrastructure

output "namespace" {
  description = "Kubernetes namespace where application is deployed"
  value       = kubernetes_namespace.banking_app.metadata[0].name
}

output "backend_service_name" {
  description = "Backend service name"
  value       = kubernetes_service.backend.metadata[0].name
}

output "frontend_service_name" {
  description = "Frontend service name"
  value       = kubernetes_service.frontend.metadata[0].name
}

output "mongodb_service_name" {
  description = "MongoDB service name"
  value       = kubernetes_service.mongodb.metadata[0].name
}

output "backend_endpoint" {
  description = "Backend service endpoint"
  value       = "http://localhost:30800"
}

output "frontend_endpoint" {
  description = "Frontend service endpoint"
  value       = "http://localhost:30080"
}

output "deployment_summary" {
  description = "Deployment summary"
  value = {
    namespace         = kubernetes_namespace.banking_app.metadata[0].name
    backend_replicas  = kubernetes_deployment.backend.spec[0].replicas
    frontend_replicas = kubernetes_deployment.frontend.spec[0].replicas
    mongodb_replicas  = kubernetes_deployment.mongodb.spec[0].replicas
    environment       = var.environment
  }
}