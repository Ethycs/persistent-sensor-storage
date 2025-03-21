from fastapi import FastAPI
from .database import engine, Base
from .routers import nodes, sensors
from .config import SENTRY_DSN
import sentry_sdk
import logging
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,         # Capture info and above as breadcrumbs
    event_level=logging.INFO,  # Send regukar as events
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
else:
    logging.warning("SENTRY_DSN not set, Sentry will not be initialized")


# Create all database tables (for SQLite or initial setup)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aclima Nodes & Sensors API")

logging.info("Logging is working: FastAPI app initialized")

# Include routers for nodes and sensors
app.include_router(nodes.router)
app.include_router(sensors.router)

# Simple health check endpoint for connectivity testing


@app.get("/health")
def health_check():
    return {"status": "OK"}


logging.info("Logging is working: Starting application")
asgi_app = SentryAsgiMiddleware(app)
