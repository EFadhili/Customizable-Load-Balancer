from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get server ID from environment variable
SERVER_ID = os.environ.get("SERVER_ID", "Unknown")

@app.route('/home', methods=['GET'])
def home():
    """Return a simple message identifying the server instance."""
    return jsonify({
        "message": f"Hello from Server: {SERVER_ID}",
        "status": "successful"
    }), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    """Heartbeat check endpoint for health monitoring."""
    return '', 200  # Simple empty 200 OK response

@app.route('/<path:req>', methods=['GET'])
def catch_all(req):
    """Catch-all route for any undefined paths (e.g., numeric request IDs)."""
    return jsonify({
        "message": f"Handled request '{req}' by Server: {SERVER_ID}",
        "status": "successful"
    }), 200

if __name__ == '__main__':
    # Bind to all network interfaces inside the container
    app.run(host='0.0.0.0', port=5000)
