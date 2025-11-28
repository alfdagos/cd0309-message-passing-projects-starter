# UdaConnect Business Requirements

## 🎯 Primary Goal
* **Refactor POC to MVP**: Transform the existing Proof of Concept (UdaTracker) application into a **Minimum Viable Product (MVP)**.
* **Microservices Architecture**: The refactoring must adopt a microservices architecture to improve scalability and maintainability.

## ⚙️ Functional & Technical Requirements
1. **High Volume Data Ingestion**: The system must be capable of handling the ingestion of a **large volume of location data** from mobile devices.
2. **Message Passing**: The architecture must utilize **message passing techniques** for inter-service communication to decouple components.
3. **Core Functionalities**:
   * **Location Ingestion**: Receive and store location data from users.
   * **Proximity Detection**: Identify individuals who have shared a close geographic proximity (attended the same booths/presentations).

## 🏗️ Infrastructure & Deployment
* **Kubernetes**: The application is designed to run on a Kubernetes cluster (K3s is used for local development).
* **Containerization**: All services must be containerized using **Docker** and images stored in a registry (e.g., DockerHub).

## 🛠️ Technology Stack Constraints
* **Backend Framework**: Python with **Flask**.
* **Database**: **PostgreSQL** with **PostGIS** extension for handling spatial data and geographic queries.
* **ORM**: SQLAlchemy for database interactions.
