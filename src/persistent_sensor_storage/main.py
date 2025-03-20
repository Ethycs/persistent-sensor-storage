from fastapi import FastAPI
from .database import engine, Base
from .routers import nodes, sensors

# Create all database tables (for SQLite or initial setup)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aclima Nodes & Sensors API")

# Include routers for nodes and sensors
app.include_router(nodes.router)
app.include_router(sensors.router)

# Simple health check endpoint for connectivity testing


@app.get("/health")
def health_check():
    return {"status": "OK"}
