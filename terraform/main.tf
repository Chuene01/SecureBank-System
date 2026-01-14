# Main Terraform configuration for Banking App Infrastructure

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Kubernetes Provider Configuration
provider "kubernetes" {
  config_path = var.kubeconfig_path
}

# Docker Provider Configuration
provider "docker" {
  host = var.docker_host
}

# Kubernetes Namespace
resource "kubernetes_namespace" "banking_app" {
  metadata {
    name = var.namespace
    labels = {
      app     = "banking-app"
      env     = var.environment
      managed = "terraform"
    }
  }
}

# ConfigMap for application configuration
resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
  }

  data = {
    mongodb_url      = "mongodb://mongodb-service:27017/"
    mongodb_database = var.mongodb_database
    environment      = var.environment
  }
}

# MongoDB Persistent Volume Claim
resource "kubernetes_persistent_volume_claim" "mongodb_pvc" {
  metadata {
    name      = "mongodb-pvc"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
  }

  spec {
    access_modes = ["ReadWriteOnce"]
    
    resources {
      requests = {
        storage = var.mongodb_storage_size
      }
    }
  }
}

# MongoDB Deployment
resource "kubernetes_deployment" "mongodb" {
  metadata {
    name      = "mongodb-deployment"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
    labels = {
      app = "banking-mongodb"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "banking-mongodb"
      }
    }

    template {
      metadata {
        labels = {
          app = "banking-mongodb"
        }
      }

      spec {
        container {
          name  = "mongodb"
          image = "mongo:7"

          port {
            container_port = 27017
          }

          env {
            name  = "MONGO_INITDB_DATABASE"
            value = var.mongodb_database
          }

          volume_mount {
            name       = "mongodb-storage"
            mount_path = "/data/db"
          }

          resources {
            requests = {
              memory = "512Mi"
              cpu    = "250m"
            }
            limits = {
              memory = "1Gi"
              cpu    = "500m"
            }
          }
        }

        volume {
          name = "mongodb-storage"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.mongodb_pvc.metadata[0].name
          }
        }
      }
    }
  }
}

# MongoDB Service
resource "kubernetes_service" "mongodb" {
  metadata {
    name      = "mongodb-service"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
    labels = {
      app = "banking-mongodb"
    }
  }

  spec {
    type = "ClusterIP"

    selector = {
      app = "banking-mongodb"
    }

    port {
      protocol    = "TCP"
      port        = 27017
      target_port = 27017
    }
  }
}

# Backend Deployment
resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "backend-deployment"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
    labels = {
      app = "banking-backend"
    }
  }

  spec {
    replicas = var.backend_replicas

    selector {
      match_labels = {
        app = "banking-backend"
      }
    }

    template {
      metadata {
        labels = {
          app = "banking-backend"
        }
      }

      spec {
        container {
          name  = "backend"
          image = var.backend_image

          port {
            container_port = 8000
          }

          env {
            name  = "PYTHONUNBUFFERED"
            value = "1"
          }

          env {
            name = "MONGODB_URL"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.app_config.metadata[0].name
                key  = "mongodb_url"
              }
            }
          }

          env {
            name = "MONGODB_DATABASE"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.app_config.metadata[0].name
                key  = "mongodb_database"
              }
            }
          }

          resources {
            requests = {
              memory = "256Mi"
              cpu    = "250m"
            }
            limits = {
              memory = "512Mi"
              cpu    = "500m"
            }
          }

          liveness_probe {
            http_get {
              path = "/"
              port = 8000
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
        }
      }
    }
  }

  depends_on = [kubernetes_deployment.mongodb]
}

# Backend Service
resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend-service"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
    labels = {
      app = "banking-backend"
    }
  }

  spec {
    type = "LoadBalancer"

    selector = {
      app = "banking-backend"
    }

    port {
      protocol    = "TCP"
      port        = 8000
      target_port = 8000
      node_port   = 30800
    }
  }
}

# Frontend Deployment
resource "kubernetes_deployment" "frontend" {
  metadata {
    name      = "frontend-deployment"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
    labels = {
      app = "banking-frontend"
    }
  }

  spec {
    replicas = var.frontend_replicas

    selector {
      match_labels = {
        app = "banking-frontend"
      }
    }

    template {
      metadata {
        labels = {
          app = "banking-frontend"
        }
      }

      spec {
        container {
          name  = "frontend"
          image = var.frontend_image

          port {
            container_port = 80
          }

          resources {
            requests = {
              memory = "128Mi"
              cpu    = "100m"
            }
            limits = {
              memory = "256Mi"
              cpu    = "200m"
            }
          }

          liveness_probe {
            http_get {
              path = "/"
              port = 80
            }
            initial_delay_seconds = 10
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/"
              port = 80
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
        }
      }
    }
  }

  depends_on = [kubernetes_deployment.backend]
}

# Frontend Service
resource "kubernetes_service" "frontend" {
  metadata {
    name      = "frontend-service"
    namespace = kubernetes_namespace.banking_app.metadata[0].name
    labels = {
      app = "banking-frontend"
    }
  }

  spec {
    type = "LoadBalancer"

    selector = {
      app = "banking-frontend"
    }

    port {
      protocol    = "TCP"
      port        = 80
      target_port = 80
      node_port   = 30080
    }
  }
}