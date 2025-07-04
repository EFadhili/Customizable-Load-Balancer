from flask import Flask, jsonify, request
import docker
import os
from consistent_hashing import ConsistentHashing

app = Flask(__name__)
client = docker.from_env()

# Initialize consistent hashing with default 3 servers
hash_map = ConsistentHashing(num_servers=3)

@app.route('/rep', methods=['GET'])
def replicas():
    """Returns the list of server replicas currently managed."""
    servers = hash_map.get_all_servers()
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": servers
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_servers():
    """Adds new server instances (containers) and registers them in the hash map."""
    data = request.get_json()
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])

    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than newly added instances", "status": "failure"}), 400

    for i in range(n):
        server_name = hostnames[i] if i < len(hostnames) else f"Server_{os.urandom(2).hex()}"
        container_name = f"server_{server_name.split()[-1]}"
        
        # Add server to hash map
        hash_map.add_server(server_name)

        # Start Docker container for the server
        try:
            client.containers.run(
                "server_image",  # Ensure this matches your server image name
                detach=True,
                name=container_name,
                environment={"SERVER_ID": server_name},
                network="net1",
                hostname=container_name
            )
        except Exception as e:
            print(f"Failed to start container {container_name}: {e}")

    return jsonify({
        "message": {
            "N": len(hash_map.get_all_servers()),
            "replicas": hash_map.get_all_servers()
        },
        "status": "successful"
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    """Removes server instances (containers) from the hash map and Docker."""
    data = request.get_json()
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])

    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than removable instances", "status": "failure"}), 400

    to_remove = hostnames[:n] if hostnames else hash_map.get_all_servers()[:n]

    for server_name in to_remove:
        container_name = f"server_{server_name.split()[-1]}"
        
        # Remove from hash map
        hash_map.remove_server(server_name)

        # Stop and remove Docker container
        try:
            container = client.containers.get(container_name)
            container.stop()
            container.remove()
        except Exception as e:
            print(f"Failed to remove container {container_name}: {e}")

    return jsonify({
        "message": {
            "N": len(hash_map.get_all_servers()),
            "replicas": hash_map.get_all_servers()
        },
        "status": "successful"
    }), 200

@app.route('/<path:req>', methods=['GET'])
def route_request(req):
    """Routes the request to the appropriate server using consistent hashing."""
    try:
        server = hash_map.get_server(req)
        container_name = f"server_{server.split()[-1]}"
        
        print(f"Routing request '{req}' to container '{container_name}' (server '{server}')")
        
        response = client.containers.get(container_name).exec_run(
            f"curl -s http://{container_name}:5000/{req}"
        )
        return response.output.decode(), 200

    except Exception as e:
        return jsonify({
            "message": f"<Error> Failed to route request to {server}: {str(e)}",
            "status": "failure"
        }), 500

@app.route('/favicon.ico')
def favicon():
    """Ignore favicon requests from browsers."""
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
