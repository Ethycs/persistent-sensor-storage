# persistent-sensor-storage
Persistent sensor storage of coupled data in database via API

This application is developed with the Pixi package tool, it is recommended to use this tool here: https://pixi.sh/latest/

TODO: 
    1. Setup API
    2. Setup Database
    3. Orchestrate Together

Choices:
    a. Fastapi is a familiar technology that is more than sufficient for this task
    b. Uvicorn is a fast ASGI web server for Python
    c. SqlAlchemy
    d. sqlite and Postgresql as Test and Production databases


From root folder
pixi run uvicorn src.persistent_sensor_storage.main:app --host 0.0.0.0 --port 8000

How to test:
    1. Make sure Uvicorn is running
    2. pixi run pytest

How to standup prod ()
    1. docker compose -f docker/docker-compose.yml up --build

TODO:
1. Reconcile issue between pip on container and pixi
2. Work on the compose file working with a requirements.txt in a root file rather than docker
3. Stress test testing code for database performance
4. Double check on spec 