FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port 80 (will be mapped to host's port 8000 via docker-compose)
EXPOSE 80

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "src.persistent_sensor_storage.main:app", "--host", "0.0.0.0", "--port", "80"]
