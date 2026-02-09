from flask import Flask, jsonify

app = Flask(__name__)

API_VERSION = "1.0"

# "Base de données" en mémoire (liste Python)
SERVERS = [
    {"id": 1, "hostname": "web-prod-01", "ip": "10.0.0.1", "status": "up"},
    {"id": 2, "hostname": "db-prod-01", "ip": "10.0.0.2", "status": "down"},
]


@app.get("/api/v1/health")
def health_check():
    return jsonify({"status": "OK", "version": API_VERSION}), 200


@app.get("/api/v1/servers")
def list_servers():
    return jsonify({"servers": SERVERS, "count": len(SERVERS)}), 200


@app.get("/api/v1/servers/<int:server_id>")
def get_server_by_id(server_id: int):
    server = next((s for s in SERVERS if s["id"] == server_id), None)
    if server is None:
        return jsonify({"error": "Server not found"}), 404
    return jsonify(server), 200


if __name__ == "__main__":
    # Host 0.0.0.0 pour compatibilité Docker, port 5000 demandé par le TP
    app.run(host="0.0.0.0", port=5000, debug=True)
