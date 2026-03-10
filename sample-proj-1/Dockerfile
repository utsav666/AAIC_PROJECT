# Use a lightweight Python 3.10 image
FROM python:3.10-slim

# Set the working directory inside the container (root of the project)
WORKDIR /app

# Copy only the requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "document_processing.endpoint_api_swagger:app", "--host", "0.0.0.0", "--port", "8000"]
