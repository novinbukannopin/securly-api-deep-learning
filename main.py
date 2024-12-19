from flask import Flask, jsonify
from flask_cors import CORS
from core.limiter import LimiterService
from app.routes import setup_routes
from config import FLASK_ENV, CORS_ORIGINS, PORT

app = Flask(__name__)

@app.errorhandler(429)
def rate_limit_handler(e):
    response = {
        "error": "Too Many Requests",
        "message": "You have exceeded the rate limit.",
        "retry_after": "1 minute"
    }
    return jsonify(response), 429

CORS(app, resources={
    r"/predict": {"origins": CORS_ORIGINS},
}, allow_headers=["Content-Type", "Authorization"])

limiter_service = LimiterService(app)
limiter = limiter_service.get_limiter()
redis_client = limiter_service.get_redis_client()

setup_routes(app, limiter, redis_client)

if __name__ == "__main__":
    app.run(debug=FLASK_ENV == "development", port=PORT, host="0.0.0.0")
