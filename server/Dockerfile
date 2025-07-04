FROM python:3.9-slim

WORKDIR /app

# Copy server code into container
COPY app.py .

# Install Python dependencies
RUN pip install flask

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

EXPOSE 5000

CMD ["python", "app.py"]
