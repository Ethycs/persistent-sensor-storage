# persistent-sensor-storage
Persistent sensor storage of coupled data in database via API

Choices:
    a. Fastapi is a familiar technology that is more than sufficient for this task
    b. Uvicorn is a fast ASGI web server for Python
    c. SqlAlchemy
    d. sqlite and Postgresql as Test and Production databases

TODO:
1. Reconcile issue between pip on container and pixi
2. Stress test testing code for database performance
3. Rewrite Application Async
4. Double check on spec 
5. Add curl commands to readme for full spec

This project implements a RESTful API using FastAPI to manage project nodes and sensors. The API provides endpoints to create, retrieve, update, and connect nodes and sensors. The project is containerized with Docker for production deployment and uses Pixi for development environment management and dependency resolution.



## Prerequisites
Pixi – A fast, cross-platform package manager built atop the conda ecosystem.
Docker – For containerized deployment.
Git – To clone and manage the source code.

## Docker Deployment
If you prefer a containerized setup, you can use Docker and Docker Compose:

Build and start the containers:

```bash
docker compose -f docker/docker-compose.yml up --build
```
The API will be available at http://localhost:8000.



1. Running the API outside of the container
With your environment set up, you can run the FastAPI application using Pixi. For example:

```bash
pixi run uvicorn src.persistent_sensor_storage.main:app --host 0.0.0.0 --port 8000
```
This command launches Uvicorn to serve your FastAPI app from the Pixi-managed environment. <mark> The API will be available at http://localhost:8000, with interactive documentation at http://localhost:8000/docs.</mark> You can access the curl commands from /docs

2. Running Tests
To run the automated tests (located in the tests/ directory), execute:

```bash
pixi run pytest
```
This will run your test suite using the environment that Pixi has created.


### Project Structure
```bash
persistent_sensor_storage/
├── src/
│   └── persistent_sensor_storage/
│       ├── __init__.py
│       ├── main.py              # FastAPI entry point; sets up routes and creates tables
│       ├── models.py            # SQLAlchemy ORM models for Nodes & Sensors
│       ├── schemas.py           # Pydantic models for request & response validation
│       ├── database.py          # Database engine and session setup
│       ├── crud.py              # CRUD operations for nodes and sensors
│       ├── dependencies.py      # Dependency functions (e.g., DB session)
│       ├── config.py            # Configuration settings (e.g., DATABASE_URL)
│       └── routers/
│           ├── __init__.py
│           ├── nodes.py         # API endpoints for node resource
│           └── sensors.py       # API endpoints for sensor resource
├── tests/
│   ├── test_main.py             # Basic API tests (e.g., health check)
│   ├── test_nodes.py            # Tests for node endpoints
│   └── test_sensors.py          # Tests for sensor endpoints
├── migrations/                  # (Optional) Alembic migrations for database schema changes
├── docker/
│   ├── Dockerfile               # Dockerfile to containerize the FastAPI app
│   └── docker-compose.yml       # Compose file to run the app with a PostgreSQL container
├── .env                       # Environment variables (e.g., DATABASE_URL)
├── requirements.txt           # Python dependencies (for Docker build and manual setup)
├── pyproject.toml             # Project manifest for Pixi (generated by `pixi init`)
├── pixi.lock                  # Lockfile generated by Pixi for reproducible environments
├── README.md                  # Project overview and instructions (this file)
└── .gitignore                 # Files to ignore in Git (e.g., __pycache__, .env, pixi.lock)
```
## API Documentation
FastAPI automatically generates interactive documentation:

OpenAPI UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc


## License
GPL 3.0