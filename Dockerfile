FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8080

# Command to run the application
CMD ["sh", "-c", "uvicorn app.main:app --host $HOST --port $PORT"]
