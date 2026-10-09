# Student API

A simple REST API built with Flask and PostgreSQL for managing student records.

This project was developed as part of the One2N SRE Bootcamp exercises, covering REST API development, database integration, migrations, testing, API documentation, and Dockerisation.

## Features

- REST API for managing students
- API versioning using `/api/v1`
- PostgreSQL database integration
- Database schema migrations
- Environment-based configuration
- Health check endpoint
- OpenAPI specification
- Automated API tests using pytest
- Docker support
- Multi-stage Docker build
- Makefile commands for common development tasks

## Tech Stack

- Python 3.12
- Flask 3.1.3
- PostgreSQL
- Psycopg
- pytest
- Docker
- Make
- OpenAPI

## Project Structure

```text
student-api/
├── app.py
├── migrate.py
├── migrations/
│   └── 001_create_students.sql
├── tests/
│   └── test_students.py
├── openapi.yaml
├── requirements.txt
├── Makefile
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Prerequisites

Make sure the following are installed:

- Python 3.12+
- PostgreSQL
- Docker
- Make

## Local Setup

Clone the repository:

```bash
git clone https://github.com/manojsambana443/student-api.git
cd student-api
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
make install
```

## Environment Configuration

Create a `.env` file in the project root.

Example:

```text
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=student_api
DB_USER=student_api_user
DB_PASSWORD=your_password
```

The `.env` file contains environment-specific configuration and is intentionally excluded from Git.

## Database Migration

Run the database migration:

```bash
make migrate
```

The migration creates the required `students` table.

## Running the API Locally

Start the Flask application:

```bash
make run
```

The API runs on:

```text
http://localhost:5000
```

## API Endpoints

### Health Check

```http
GET /healthcheck
```

Example:

```bash
curl http://localhost:5000/healthcheck
```

### Get All Students

```http
GET /api/v1/students
```

Example:

```bash
curl http://localhost:5000/api/v1/students
```

### Get Student by ID

```http
GET /api/v1/students/<student_id>
```

Example:

```bash
curl http://localhost:5000/api/v1/students/1
```

### Create Student

```http
POST /api/v1/students
```

Example:

```bash
curl -X POST http://localhost:5000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John","course":"DevOps"}'
```

### Update Student

```http
PUT /api/v1/students/<student_id>
```

Example:

```bash
curl -X PUT http://localhost:5000/api/v1/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","course":"Cloud"}'
```

### Delete Student

```http
DELETE /api/v1/students/<student_id>
```

Example:

```bash
curl -X DELETE http://localhost:5000/api/v1/students/1
```

## API Documentation

The API specification is available in:

```text
openapi.yaml
```

The OpenAPI specification documents the available API endpoints, request bodies, and responses.

## Running Tests

Run the test suite using:

```bash
make test
```

The tests verify the API behaviour and database operations.

## Makefile Commands

The project provides a Makefile to simplify common development commands.

### Install dependencies

```bash
make install
```

### Run the application

```bash
make run
```

### Run tests

```bash
make test
```

### Run database migrations

```bash
make migrate
```

### Build Docker image

```bash
make docker-build
```

### Run the application using Docker

```bash
make docker-run
```

## Docker

The Student API can be built and run using Docker.

### Docker Image

The current Docker image is tagged using Semantic Versioning:

```text
student-api:1.1.0
```

The project intentionally avoids using the `latest` tag.

### Build the Docker Image

Build the image using:

```bash
make docker-build
```

This creates the following image:

```text
student-api:1.1.0
```

### Run the Docker Container

Run the API using:

```bash
make docker-run
```

The container exposes the API on port `5000`.

Environment variables are injected at container runtime instead of being stored inside the Docker image.

### Verify the Container

Check the health endpoint:

```bash
curl http://localhost:5000/healthcheck
```

Get all students:

```bash
curl http://localhost:5000/api/v1/students
```

The API should return the student data from PostgreSQL.

## Multi-Stage Docker Build

The Dockerfile uses a multi-stage build.

The first stage installs the Python dependencies in a separate build environment.

The second stage contains the runtime environment, application files, migrations, and required dependencies.

Using multiple stages helps keep the final runtime image smaller by separating build-time and runtime requirements.

## Docker Build Context

The `.dockerignore` file prevents unnecessary files from being sent to the Docker build context.

Examples include:

```text
.git
.venv
__pycache__
.pytest_cache
.env
tests
```

This keeps the Docker build context smaller and prevents sensitive or unnecessary files from being included in the Docker image.

## Docker and Environment Variables

Environment-specific configuration is injected when the container starts.

The `.env` file is not copied into the Docker image and is not committed to the repository.

For local development, the application uses:

```text
DB_HOST=127.0.0.1
```

When running inside Docker, the Makefile provides the appropriate database host configuration to the container at runtime.

## Docker Image Size

The Docker image was reduced using a multi-stage build and pip's `--no-cache-dir` option.

The initial Docker image was approximately:

```text
170 MB
```

The multi-stage Docker image is approximately:

```text
162 MB
```

This reduces unnecessary build artifacts and package cache data from the final runtime image.

## Useful Docker Commands

List Docker images:

```bash
docker images
```

Run the container directly:

```bash
docker run --rm -p 5000:5000 student-api:1.1.0
```

View Docker image history:

```bash
docker history student-api:1.1.0
```

List running containers:

```bash
docker ps
```

Stop a running container:

```bash
docker stop <container_id>
```

## Development Workflow

The typical development workflow is:

```text
1. Install dependencies
        ↓
2. Configure environment variables
        ↓
3. Run database migration
        ↓
4. Start Flask API
        ↓
5. Run tests
        ↓
6. Build Docker image
        ↓
7. Run API using Docker
        ↓
8. Verify API endpoints
```

## Versioning

Docker images are tagged using Semantic Versioning.

Current version:

```text
1.1.0
```

Docker image:

```text
student-api:1.1.0
```

The project does not rely on the `latest` Docker tag.

## License

This project is created for learning and SRE/DevOps practice as part of the One2N SRE Bootcamp.

## One-Click Local Development Setup (Docker Compose)

Docker Compose starts the application stack with a single command, including PostgreSQL, database migrations, and the Flask API.

### Prerequisites
- Docker installed
- Docker Compose v2
- A `.env` file containing the required database configuration

### Start the Application

```bash
make setup
```

This command builds the application image and starts the services in the correct order:

1. **Database (`db`)** — starts PostgreSQL and waits for its health check to pass.
2. **Migration (`migrate`)** — applies pending database migrations and exits successfully.
3. **API (`api`)** — starts the Flask API after migrations complete successfully.

### Verify the Setup

```bash
make status
curl http://localhost:5000/healthcheck
curl http://localhost:5000/api/v1/students
```

The health-check endpoint should return a healthy status.

### View Logs

```bash
make logs
```

### Stop the Application

```bash
make down
```

This removes the Compose containers and network but preserves the named PostgreSQL volume. Database data remains available when the stack is started again with `make setup`.

**Note:** Do not use `docker compose down -v` unless you intentionally want to remove the named volume and its stored database data.
