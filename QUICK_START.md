# UdaConnect - Quick Start Guide

## 🚀 Deploy dell'Applicazione

### 1. Deploy dei componenti
```bash
# Vai nella directory del progetto
cd /home/alfdagos/Projects/cd0309-message-passing-projects-starter

# Applica tutte le configurazioni
kubectl apply -f deployment/db-configmap.yaml
kubectl apply -f deployment/db-secret.yaml
kubectl apply -f deployment/postgres.yaml
kubectl apply -f deployment/udaconnect-api.yaml
kubectl apply -f deployment/udaconnect-app.yaml

# Attendi che i pod siano pronti
kubectl wait --for=condition=ready pod --all --timeout=120s
```

### 2. Seed del database (solo la prima volta)
```bash
# Ottieni il nome del pod postgres
POD_NAME=$(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}')

# Esegui lo script di seeding
sh scripts/run_db_command.sh $POD_NAME
```

## 🌐 Eseguire e Accedere all'Applicazione

### Avvia i port-forward (richiesto per k3d)
```bash
# Terminal 1: Port-forward per l'API
kubectl port-forward svc/udaconnect-api 30001:5000

# Terminal 2: Port-forward per la Web App
kubectl port-forward svc/udaconnect-app 30000:3000
```

### 🔗 Link per accedere all'applicazione

#### 📱 Applicazione Web (Frontend)
**http://localhost:30000/**

#### 📚 API Documentation (OpenAPI/Swagger)
**http://localhost:30001/**

#### 🔌 API Endpoint Base
**http://localhost:30001/api/**

## ✅ Verifica dello Stato

```bash
# Verifica pod
kubectl get pods

# Verifica servizi
kubectl get services

# Logs dell'API
kubectl logs -f deployment/udaconnect-api

# Logs dell'app
kubectl logs -f deployment/udaconnect-app
```

## 🗑️ Cleanup (per rimuovere tutto)

```bash
kubectl delete -f deployment/
```

## 📋 Note Importanti

- **Cluster richiesto**: k3d, minikube, o k3s
- **Port-forwarding**: Necessario per k3d (i NodePort non sono esposti automaticamente)
- **Database**: PostgreSQL con estensione PostGIS
- **Seeding**: Va eseguito solo la prima volta dopo il deploy

---

**Cluster attuale**: k3d (K3s v1.31.5 in Docker)
