from flask import Flask, request, jsonify
import redis
import time

print("Starting Flask app...")

app = Flask(__name__)

"""
Try block: This section tries to connect to Redis.

redis.StrictRedis(...): Connects to Redis running on your machine at localhost on port 6379.

decode_responses=True tells Redis to return strings instead of bytes.

redis_client.ping(): Sends a ping to Redis to check if it's working.

If connection fails, it shows an error message and exits.

"""
try:
    print("Connecting to Redis...")
    redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
    redis_client.ping()
    print("Connected to Redis successfully.")
except redis.exceptions.ConnectionError as e:
    print("Failed to connect to Redis:", e)
    exit(1)

# Config the parameters
"""This means: allow only 10 requests per 60 seconds from the same IP address."""
request_limit = 10  # max request
time_window = 60    # in seconds

"""
This function is called before every request to any route.
We're using this to check if the client is sending too many requests.
"""
@app.before_request
def rate_limit():
    client_ip = request.remote_addr
    current_time = int(time.time())
    print("current_time",current_time)
    key = f"rate_limit:{client_ip}:{current_time // time_window}"
    print("key", key)

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, time_window)

    if count > request_limit:
        return jsonify({"error": "Too Many Requests"}), 429


"""
Default Route
This defines what to do when a user visits /.
It simply returns a success message.

"""
@app.route("/")
def home():
    return "Welcome!! you are within the rate limit"


"""
This makes sure the app runs only if you run rate_limiter.py directly.

debug=True gives helpful error messages while developing.
"""
if __name__ == "__main__":
    app.run(debug=True)
