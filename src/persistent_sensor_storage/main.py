from fastapi import FastAPI
from .database import engine, Base
from .routers import nodes, sensors
from .config import SENTRY_DSN
import sentry_sdk
import logging
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from .kafka.consumers import node_consumer, sensor_consumer, readings_consumer
import asyncio

from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,         # Capture info and above as breadcrumbs
    event_level=logging.INFO,  # Send errors as events
)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        integrations=[sentry_logging],
        traces_sample_rate=1.0,
        _experiments={
            # Set continuous_profiling_auto_start to True
            # to automatically start the profiler on when
            # possible.
            "continuous_profiling_auto_start": True,
        },
    )
    sentry_sdk.profiler.start_profiler()    
else:
    logging.warning("SENTRY_DSN not set, Sentry will not be initialized")


# Create all database tables (for SQLite or initial setup)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aclima Nodes & Sensors API")

logging.info("Logging is working: FastAPI app initialized")

# Include routers for nodes and sensors
app.include_router(nodes.router)
app.include_router(sensors.router)

# Kafka consumer tasks
consumer_tasks = []

@app.on_event("startup")
async def startup_event():
    """Start Kafka consumers on application startup."""
    loop = asyncio.get_event_loop()
    consumer_tasks.extend([
        loop.create_task(node_consumer.start()),
        loop.create_task(sensor_consumer.start()),
        loop.create_task(readings_consumer.start())
    ])

@app.on_event("shutdown")
async def shutdown_event():
    """Stop Kafka consumers on application shutdown."""
    for task in consumer_tasks:
        task.cancel()
    await asyncio.gather(*consumer_tasks, return_exceptions=True)
    await node_consumer.stop()
    await sensor_consumer.stop()
    await readings_consumer.stop()

# Simple health check endpoint for connectivity testing


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "OK"}


logging.info("Logging is working: Starting application")
asgi_app = SentryAsgiMiddleware(app)
sentry_sdk.profiler.stop_profiler()
