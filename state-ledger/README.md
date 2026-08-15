# State Ledger Backend Service

[![Java 21](https://img.shields.io/badge/Java-21-orange?style=flat-square&logo=openjdk)](https://openjdk.org/projects/jdk/21/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-brightgreen?style=flat-square&logo=springboot)](https://spring.io/projects/spring-boot)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
[![Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?style=flat-square&logo=googlecloud)](https://cloud.google.com/run)

An immutable, append-only backend ledger designed to maintain reliable state storage and eliminate context drift for autonomous AI agents. 
---

## Tech Stack

* **Language & Framework:** Java 21, Spring Boot 3
* **Database & ORM:** PostgreSQL (Neon), Spring Data JPA / Hibernate
* **Containerization:** Docker (Eclipse Temurin JDK 21 Alpine)
* **Cloud & Deployment:** Google Cloud Run, Google Artifact Registry, Google Cloud Build
---

## Local Development & Setup

### 1. Prerequisites
Make sure you have the following installed on your machine:
* **Java 21** (JDK 21)
* **Maven** (or you can use the included `./mvnw` wrapper)
* **PostgreSQL** (or a remote Neon database instance)

### 2. Configure Environment Variables
You can configure your local database connection by setting the following environment variables, or rely on the local defaults in your `src/main/resources/application.properties`:

```properties
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/state_ledger_db
SPRING_DATASOURCE_USERNAME=postgres
SPRING_DATASOURCE_PASSWORD=your_password
```

### 3. Run the Application Locally
Clone the repository, navigate to the `state-ledger` directory, and run:

```bash
./mvnw clean spring-boot:run
```
---

## Dockerization

You can containerize and run the backend service locally using Docker.

### 1. Build the Docker Image
From the root of your `state-ledger` directory (where the `Dockerfile` is located), run:

```bash
docker build -t state-ledger:latest .
```
### 2. Run the Container Locally
Run the container and pass your database environment variables:

```bash
docker run -p 8080:8080 `
  -e SPRING_DATASOURCE_URL="jdbc:postgresql://your-db-host:5432/neondb?sslmode=require" `
  -e SPRING_DATASOURCE_USERNAME="neondb_owner" `
  -e SPRING_DATASOURCE_PASSWORD="your_password" `
  state-ledger:latest
```
---

## Google Cloud Deployment (Cloud Run)

The application is containerized and deployed to Google Cloud Run, utilizing Google Cloud Build for CI and Google Artifact Registry for image storage.

### 1. Build and Push via Cloud Build
Run the following command from your project root to trigger a cloud build:

```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/api-ledger-backend/ledger-repo/state-ledger:latest
```

### 2. Deploy to Cloud Run
Deploy the built image to Cloud Run with your production database environment variables:

```bash
gcloud run deploy state-ledger-service \
    --image us-central1-docker.pkg.dev/api-ledger-backend/ledger-repo/state-ledger:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars "SPRING_DATASOURCE_URL=jdbc:postgresql://your-db-host/neondb?sslmode=require,SPRING_DATASOURCE_USERNAME=neondb_owner,SPRING_DATASOURCE_PASSWORD=your_password"
```
