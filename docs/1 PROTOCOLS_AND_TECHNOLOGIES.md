# UdaConnect Protocols and Technologies

## Module Design Justifications

### 1. API Gateway (HTTP REST)
**Choice:** HTTP REST with Python/Flask.
**Justification:** Leveraging the existing Flask skillset minimizes development time to meet the 2-week launch deadline. REST provides a standard, cost-effective interface for the frontend without requiring complex client generation.

### 2. Location Ingestion API (HTTP REST)
**Choice:** HTTP REST with Python/Flask.
**Justification:** A lightweight REST endpoint allows mobile devices to easily push large volumes of data using standard protocols. It acts as a producer for the message broker, decoupling ingestion from processing to handle high-throughput ingress.

### 3. Apache Kafka (Message Broker)
**Choice:** Kafka.
**Justification:** Kafka is chosen to handle the ingress of large volumes of location data reliably and asynchronously. It allows the system to buffer high-throughput traffic, preventing data loss and ensuring the system scales within a limited budget.

### 4. Location Consumer (Kafka Consumer)
**Choice:** Python Consumer.
**Justification:** Running as a containerized service, the consumer processes data from Kafka in batches to optimize database writes. This design allows for independent scaling of workers to manage variable data loads efficiently.

### 5. Person Service (gRPC)
**Choice:** gRPC.
**Justification:** gRPC provides strictly typed, efficient internal communication that reduces network overhead and latency. Auto-generated client code accelerates development, helping to meet the strict 2-week delivery timeline.

### 6. Connection Service (HTTP REST)
**Choice:** HTTP REST with Python/Flask.
**Justification:** Isolating the complex PostGIS logic into a separate containerized service ensures modularity for the MVP. REST is sufficient for these read-heavy, less frequent query patterns, keeping development complexity and costs low.

### 7. PostgreSQL + PostGIS (Database)
**Choice:** PostgreSQL with PostGIS.
**Justification:** This open-source solution meets the budget constraints while providing the necessary spatial features for proximity detection. Reusing the existing database technology minimizes the learning curve and development time.
