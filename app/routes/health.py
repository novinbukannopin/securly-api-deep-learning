from flask import jsonify

def health_routes(bp, limiter, redis_client):
    @bp.route("/health", methods=["GET"])
    @limiter.limit("5 per minute")
    def health_check():
        return jsonify({"status": "success", "message": "API is healthy."}), 200
