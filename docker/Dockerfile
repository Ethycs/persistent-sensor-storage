FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (all files in the project root)
COPY . .

# Expose port 80 (container port 80 mapped to host port 8000)
EXPOSE 80

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "src.persistent_sensor_storage.main:app", "--host", "0.0.0.0", "--port", "80"]
