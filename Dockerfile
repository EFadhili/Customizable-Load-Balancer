FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y docker.io curl && \
    apt-get clean

# Copy load balancer code into container
COPY app.py .
COPY consistent_hashing.py .

# Install Python dependencies
RUN pip install flask docker

EXPOSE 5000

CMD ["python", "app.py"]
