# Message Passing Implementation Plan

## Objective
Apply message passing techniques to enable asynchronous communication between the Location Ingestion API and the Location Consumer using Apache Kafka, synchronous communication between the API Gateway and Person Service using gRPC, and RESTful communication for other services.

## Kafka Implementation Steps

### 1. Kafka Queue Implementation
**Requirement**: Project implements a Kafka queue in a container in a Dockerfile or Kubernetes deployment file.
**Action**:
-   Created `deployment/kafka.yaml` which defines a Kubernetes Deployment and Service for Kafka.
-   Used the pre-built `bitnami/kafka:latest` Docker image.
-   Configured Kafka in KRaft mode (no Zookeeper required) for simplicity and modern deployment.
-   Exposed port `9092` for internal cluster communication.

### 2. Python Kafka Library
**Requirement**: requirements.txt file installs the kafka-python Kafka library.
**Action**:
-   Updated `modules/location-api/requirements.txt` to include `kafka-python==2.0.2`.
-   Updated `modules/location-consumer/requirements.txt` to include `kafka-python==2.0.2`.
-   This library enables the Producer (API) and Consumer (Worker) to interact with the Kafka broker.

### 3. Kafka Deployment Verification
**Requirement**: kafka deployment runs successfully without errors.
**Action**:
-   Deploy Kafka using `kubectl apply -f deployment/kafka.yaml`.
-   Verify the pod status is `Running` using `kubectl get pods`.
-   Check logs for startup errors using `kubectl logs -l app=kafka`.
-   Ensure other services (`location-api`, `location-consumer`) can successfully connect to the `kafka:9092` service.

## gRPC Implementation Steps

### 1. Protobuf Definition
**Requirement**: Project contains a *.proto file showing that they mapped a message and service into a protobuf format.
**Action**:
-   Created `modules/person-service/app/protos/person.proto`.
-   Defined `PersonService` with RPC methods: `Create`, `Retrieve`, `RetrieveAll`.
-   Defined messages: `PersonMessage`, `PersonId`, `PersonList`, `Empty`.

### 2. Code Generation
**Requirement**: Code should contain a *_pb2 and *_pb2_grpc file generated from the *.proto file.
**Action**:
-   Configured `modules/person-service/Dockerfile` to run `grpc_tools.protoc` during the build process.
-   Configured `modules/api/Dockerfile` to run `grpc_tools.protoc` during the build process.
-   This ensures `person_pb2.py` and `person_pb2_grpc.py` are generated and available in the container at runtime.

### 3. gRPC Client
**Requirement**: Project contains a gRPC client. Code should open a gRPC channel.
**Action**:
-   Implemented in `modules/api/app/udaconnect/services.py`.
-   Uses `grpc.insecure_channel('person-service:5001')` to connect to the Person Service.
-   Calls the defined RPC methods using the generated stub.

### 4. gRPC Host
**Requirement**: Project contains a gRPC host. Code should contain a grpc.server() instantiation.
**Action**:
-   Implemented in `modules/person-service/app/main.py`.
-   Instantiates `server = grpc.server(...)`.
-   Registers the `PersonService` servicer.
-   Starts the server on port `5001`.

### 5. gRPC Dependencies
**Requirement**: requirements.txt file should define the grpcio package.
**Action**:
-   Verified `modules/person-service/requirements.txt` contains `grpcio` and `grpcio-tools`.
-   Verified `modules/api/requirements.txt` contains `grpcio` and `grpcio-tools`.

## REST API Implementation Steps

### 1. New/Modified API Endpoints
**Requirement**: Project either created a new API endpoint(s) or a modification to existing Flask API.
**Action**:
-   **Connection Service**: Created `modules/connection-service/app/routes.py` exposing `GET /persons/<person_id>/connection`.
-   **Location API**: Created `modules/location-api/app/routes.py` exposing `POST /locations`.
-   **API Gateway**: Modified `modules/api/app/udaconnect/controllers.py` to act as a proxy, forwarding requests to the respective microservices.

### 2. Proper HTTP Request Types
**Requirement**: All new API endpoints use proper HTTP request types.
**Action**:
-   `GET` used for retrieving connection data (`ConnectionDataResource`).
-   `POST` used for creating new locations (`LocationResource`).
-   `POST` used for creating new persons (`PersonsResource`).

### 3. No Payload in GET/DELETE
**Requirement**: GET or DELETE request does not contain an HTTP payload.
**Action**:
-   Verified `ConnectionDataResource.get` in `modules/connection-service/app/routes.py` uses `request.args` to retrieve query parameters (`start_date`, `end_date`, `distance`).
-   No JSON body is expected or processed for this GET request.

### 4. Swagger Documentation
**Requirement**: REST API’s have live Swagger documentation in an external library.
**Action**:
-   Used `flask-restx` library in all Flask services (`api`, `connection-service`, `location-api`).
-   `flask-restx` automatically generates Swagger UI documentation.
-   Defined schemas using `marshmallow` and `flask-accepts` to document request/response structures.
