# 🚦 Flask Rate Limiting Middleware using Redis

This project is a simple implementation of **rate limiting** for a Flask web application using **Redis**. It prevents clients from sending too many requests in a short period of time.

---

## 🧠 What is Redis?

**Redis** (Remote Dictionary Server) is an open-source, in-memory data structure store, used as a database, cache, and message broker.

### 🔧 Why Redis here?

We use Redis to **store the request count** for each client (based on their IP address). Redis is ideal for this because:
- It is very fast (in-memory).
- It supports automatic key expiry (perfect for time-based limits).
- It can handle thousands of reads/writes per second.

In our project:
- Each client’s request count is saved in Redis with a key like:  
  `rate_limit:<client_ip>:<time_window_id>`
- Redis automatically deletes the key after 60 seconds (using `expire`).

---

## 🍶 What is Flask?

**Flask** is a lightweight Python web framework used for building web apps and APIs.

### 🔧 Why Flask here?

We're using Flask to:
- Create a simple web server.
- Handle HTTP requests (e.g., when someone visits `/`).
- Run middleware logic before processing the request.

In our app:
- We use `@app.before_request` to run the rate limiter before any route is executed.
- If the client sends more than 10 requests in 60 seconds, Flask returns a `429 Too Many Requests` response.

---

## 🛠 How It Works

1. When a client sends a request, we check their IP address.
2. We create a Redis key for that IP tied to the current time window.
3. Redis increments the request count.
4. If the count exceeds the allowed limit, we block the request.

---

## 🚀 How to Run This Project

### ✅ Requirements

- Python 3.7+
- Redis (or [Memurai](https://www.memurai.com/get-memurai) for Windows)
- Packages: Flask, redis-py

### 📦 Install Dependencies

```bash
pip install -r requirements.txt


### Start Redis
curl localhost:6379

### Run the APP
python rate_limiter.py

Visit: http://localhost:5000

After 10 rapid requests in a minute, you'll see:
{"error": "Too Many Requests"}

### 💡 Core Concepts (Server, Localhost, Ports)
🧑‍🍳 What is a Server?
A server is a program (or computer) that waits for a request and sends a response.

In this project:

Flask is your web server (it handles URL requests).

Redis is a server that stores and manages data.

### 🏡 What is Localhost?
localhost means "this computer" — your own machine.

IP address of localhost is 127.0.0.1.

It's used for testing apps locally (without needing the internet).

### 🔌 What is a Port?
A port is like a numbered door where programs listen for messages.

Program	Port	Purpose
Flask	5000	Handles web requests (default Flask port)
Redis	6379	Handles data requests (default Redis port)

So:

http://localhost:5000 = “Open browser and talk to Flask server running locally”

Flask connects to Redis at localhost:6379 = “Ask Redis to track requests”