# GitOps CI/CD Pipeline - Monorepo Demo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A complete **GitOps implementation** demonstrating automated deployment of a multi-service application using modern DevOps tools and practices.

## 🎯 Project Overview

This project showcases a production-ready CI/CD pipeline that:
- Automatically builds Docker images on every commit
- Pushes images to a private registry (Nexus)
- Updates Kubernetes manifests with new image tags
- Uses Argo CD to sync deployments to a Kubernetes cluster
- Implements GitOps principles (Git as single source of truth)

##  Architecture
```
Developer Push to Git
        ↓
   GitLab CI/CD
        ↓
  Docker Image Build
        ↓
  Push to Nexus Registry
        ↓
  Update K8s Manifests in Git
        ↓
   Argo CD Detects Change
        ↓
  Sync to Kubernetes Cluster
        ↓
   Rolling Update (Zero Downtime)
```

##  Application Components

### Frontend
- **Technology**: Nginx web server
- **Port**: 80
- **Replicas**: 2
- **Service Type**: NodePort (for external access)

### Backend  
- **Technology**: Python Flask REST API
- **Port**: 5000
- **Replicas**: 2
- **Endpoints**:
  - `GET /` - Health check
  - `GET /api/data` - Returns JSON data

### Database
- **Technology**: MySQL 8.0
- **Port**: 3306
- **Replicas**: 1
- **Initialization**: Custom SQL script on startup

##  Technologies & Tools

| Category | Tools |
|----------|-------|
| **CI/CD** | GitLab CI/CD |
| **Container Registry** | Nexus Repository OSS |
| **Orchestration** | Kubernetes (Minikube for local) |
| **GitOps** | Argo CD |
| **Containerization** | Docker |
| **Configuration Management** | Kustomize |
| **Version Control** | Git |

##  Project Structure
```
application-images/
├── .gitlab-ci.yml              # CI/CD pipeline definition
│
├── frontend/                   # Frontend application
│   ├── Dockerfile             # Nginx container image
│   └── index.html             # Static web content
│
├── backend/                    # Backend API
│   ├── Dockerfile             # Flask container image
│   └── app.py                 # REST API application
│
├── database/                   # Database
│   ├── Dockerfile             # MySQL container image
│   └── init.sql               # Database initialization script
│
└── k8s/                        # Kubernetes manifests
    ├── kustomization.yaml     # Root Kustomize configuration
    │
    ├── frontend/
    │   ├── kustomization.yaml
    │   ├── deployment.yaml    # Frontend deployment (2 replicas)
    │   └── service.yaml       # NodePort service
    │
    ├── backend/
    │   ├── kustomization.yaml
    │   ├── deployment.yaml    # Backend deployment (2 replicas)
    │   └── service.yaml       # ClusterIP service
    │
    └── database/
        ├── kustomization.yaml
        ├── deployment.yaml    # Database deployment (1 replica)
        └── service.yaml       # ClusterIP service
```

##  Getting Started

### Prerequisites

Before running this project, ensure you have:

- **Minikube** - Local Kubernetes cluster
- **kubectl** - Kubernetes command-line tool
- **Docker** - Container runtime
- **GitLab** account (or GitLab self-hosted)
- **Nexus Repository** - Container registry
- **Argo CD** - GitOps deployment tool


#### 3. Configure GitLab CI/CD

Set these variables in GitLab (Settings → CI/CD → Variables):

| Variable | Description | Masked |
|----------|-------------|--------|
| `GIT_PUSH_USER` | Your GitLab username | No |
| `GIT_PUSH_TOKEN` | Personal Access Token | Yes |
| `REGISTRY_URL` | Nexus registry address | No |
| `NEXUS_USER` | Nexus username | No |
| `NEXUS_PASSWORD` | Nexus password | Yes |

#### 4. Install Argo CD
```bash
# Create namespace
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

#### 5. Configure Argo CD Application

1. Access Argo CD UI: https://localhost:8080
2. Login with username `admin` and retrieved password
3. Add your Git repository
4. Create application:
   - **Name**: app-monorepo
   - **Project**: default
   - **Repo URL**: Your GitLab repository
   - **Path**: k8s/
   - **Cluster**: https://kubernetes.default.svc
   - **Namespace**: apps
5. Click **SYNC** to deploy

##  CI/CD Pipeline

The pipeline consists of two stages:

### Stage 1: Build and Push
Three parallel jobs build Docker images:
- `backend_build_and_push` - Builds backend image
- `frontend_build_and_push` - Builds frontend image  
- `database_build_and_push` - Builds database image

Each job:
1. Builds Docker image
2. Tags with Git commit SHA
3. Pushes to Nexus registry

### Stage 2: Update Manifests
- Updates Kubernetes deployment YAMLs with new image tags
- Commits changes back to Git repository
- Triggers Argo CD sync

##  GitOps Workflow

1. Developer pushes code to Git
2. GitLab CI/CD pipeline triggers
3. Images built and pushed to Nexus
4. Manifests updated with new image tags
5. Changes committed to Git
6. Argo CD detects drift
7. Argo CD syncs cluster state
8. Kubernetes performs rolling update
9. Application updated with zero downtime 

##  Learning Outcomes

This project demonstrates:

- ✅ **Monorepo structure** for microservices
- ✅ **Continuous Integration/Deployment**
- ✅ **GitOps principles** and methodology
- ✅ **Container orchestration** with Kubernetes
- ✅ **Infrastructure as Code** practices
- ✅ **Automated testing** and deployment
- ✅ **Service mesh** architecture basics
- ✅ **Rolling updates** for zero-downtime deployments

## 🐛 Troubleshooting

### ImagePullBackOff Error

If pods can't pull images:
```bash
# Restart Minikube with insecure registry
minikube stop
minikube delete --purge=true
minikube start --driver=docker --insecure-registry="<NEXUS_IP>:5002"

# Verify configuration
minikube ssh
docker info | grep -A3 'Insecure Registries'
exit

# Delete pods to recreate
kubectl delete pods --all -n apps
```

### Pipeline Fails to Push Images

Check Nexus user has proper permissions:
- Role: nx-admin or custom role with docker push privileges


##  Future Enhancements

Potential improvements:

- [ ] Add automated testing (unit tests, integration tests)
- [ ] Implement health checks and readiness probes
- [ ] Add Horizontal Pod Autoscaling (HPA)
- [ ] Implement service mesh (Istio/Linkerd)
- [ ] Add monitoring and alerting
- [ ] Implement blue-green or canary deployments
- [ ] Add persistent volumes for database
- [ ] Implement backup and disaster recovery
- [ ] Add multi-cluster deployment
- [ ] Implement progressive delivery with Argo Rollouts


##  Author

**Abdulrahman Alharbi**
