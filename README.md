# Customizable Load Balancer Project

This project implements a **customizable load balancer** with consistent hashing and auto-scaling capabilities using **Docker**, **Python Flask**, and **Docker SDK**.

It demonstrates key distributed systems concepts including:

- Consistent hashing
- Dynamic replica management
- Request routing
- Load distribution analysis

---

## 📋 Project Structure
```

├── server/ # Minimal backend server
│ ├── app.py
│ ├── Dockerfile
│
├── load_balancer/ # Load Balancer & Consistent Hashing
│ ├── app.py # Load Balancer Flask App
│ ├── consistent_hashing.py # Consistent Hashing Implementation
│ ├── Dockerfile
│
├── Analysis/ # Load Distribution Testing 
│ ├── analysis.py # Async Request Load Tester with Graph Output
│
├── docker-compose.yml # Multi-Container Setup
├── README.md # Project Documentation

---
```
## ✅ Task 1: Server

The server (`server/app.py`) is a minimal Flask app with:

- `/home` → Returns the server’s ID.
- `/heartbeat` → Health check endpoint.

Each server runs inside a Docker container with its own `SERVER_ID`.

---

## ✅ Task 2: Consistent Hashing

Implemented in `load_balancer/consistent_hashing.py`:

- Uses a hash ring with 512 slots and 9 virtual nodes per server.
- Maps requests to backend servers consistently.
- Minimizes redistribution during server changes.
- Supports adding/removing servers dynamically.

---

## ✅ Task 3: Load Balancer

Implemented in `load_balancer/app.py` using Flask + Docker SDK:

- `/rep` → View current replicas.
- `/add` → Add new server instances dynamically.
- `/rm` → Remove server instances dynamically.
- `/<path>` → Route incoming requests to the correct backend using consistent hashing.

The load balancer automatically controls Docker containers:

- Starts/stops backend servers.
- Uses consistent hashing for stable routing.
- Communicates with servers over Docker’s internal network.

---

## ✅ Task 4: Analysis

Located in `Analysis/analysis.py`:

- Sends 10,000 async requests to `/home` endpoint via load balancer.
- Collects the number of requests served by each backend.
- Generates and saves a **bar chart** (`load_distribution.png`) showing load distribution.

---

## ⚙️ How to Run the Project

### 1. Build and Start All Containers:

```bash
docker-compose build
docker-compose up


```

## Interact with Load Balancer Endpoints

### View Current Replicas

```bash
curl http://127.0.0.1:5000/rep

```

### Add Servers

```bash
curl -X POST http://127.0.0.1:5000/add \
-H "Content-Type: application/json" \
-d '{"n": 2, "hostnames": ["Server 4", "Server 5"]}'


```

### Remove Servers

```bash
curl -X DELETE http://127.0.0.1:5000/rm \
-H "Content-Type: application/json" \
-d '{"n": 1, "hostnames": ["Server 4"]}'

```

## Run Load Distribution Analysis

### Apache

```bash
sudo apt-get install apache2-utils

```

```bash
ab -n 10000 -c 100 http://127.0.0.1:5000/home

```
