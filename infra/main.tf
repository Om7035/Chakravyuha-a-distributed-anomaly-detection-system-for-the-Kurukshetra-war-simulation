terraform {
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# 1. Deploy Redpanda (Kafka) - Low Resource Mode
resource "helm_release" "redpanda" {
  name       = "redpanda"
  repository = "https://charts.redpanda.com"
  chart      = "redpanda"
  namespace  = "redpanda"
  create_namespace = true

  # External Access
  set {
    name  = "external.enabled"
    value = "true"
  }
  set {
    name  = "external.type"
    value = "NodePort"
  }
  set {
    name  = "external.domain"
    value = "localhost" 
  }
  
  # CRITICAL: Strict Resource Limits for 8GB Laptop
  set {
    name  = "resources.cpu.cores"
    value = "0.5" 
  }
  set {
    name  = "resources.memory.container.max"
    value = "1.5Gi" # Cap memory at 1.5GB
  }
  set {
    name  = "statefulset.replicas"
    value = "1"
  }
}

# 2. Deploy MinIO (S3 Storage) - Low Resource Mode
resource "helm_release" "minio" {
  name       = "minio"
  repository = "https://charts.min.io/"
  chart      = "minio"
  namespace  = "minio"
  create_namespace = true

  set {
    name  = "rootUser"
    value = "admin"
  }
  set {
    name  = "rootPassword"
    value = "password123"
  }
  set {
    name  = "persistence.size"
    value = "2Gi"
  }
  set {
    name  = "resources.requests.memory"
    value = "256Mi" # Reduce to 256MB
  }
}

# 3. Deploy Redis (Feature Store)
resource "helm_release" "redis" {
  name       = "redis"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "redis"
  namespace  = "feast"
  create_namespace = true
  
  set {
    name  = "architecture"
    value = "standalone"
  }
  set {
    name  = "auth.enabled"
    value = "false"
  }
}
