from fastapi import FastAPI
from .database import engine, Base
from .routers import nodes, sensors
from .config import SENTRY_DSN
from .init_db import engine as init_engine
import sentry_sdk
import logging
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.INFO,  # Send errors as events
)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Add data like request headers and IP for users
        # See docs for more info
        send_default_pii=True,
        integrations=[sentry_logging],
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )
    sentry_sdk.profiler.start_profiler()
else:
    logging.warning("SENTRY_DSN not set, Sentry will not be initialized")


app = FastAPI(title="Aclima Nodes & Sensors API")

# Create all database tables (for SQLite or initial setup)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=init_engine)

logging.info("Logging is working: FastAPI app initialized")

# Include routers for nodes and sensors
app.include_router(nodes.router)
app.include_router(sensors.router)


@app.get("/health")
def health_check():
    return {"status": "OK"}


logging.info("Logging is working: Starting application")
asgi_app = SentryAsgiMiddleware(app)
sentry_sdk.profiler.stop_profiler()
