from flask import Flask
from core.limiter import LimiterService
from app.routes import setup_routes

app = Flask(__name__)

limiter_service = LimiterService(app)
limiter = limiter_service.get_limiter()
redis_client = limiter_service.get_redis_client()

setup_routes(app, limiter, redis_client)

if __name__ == "__main__":
    app.run(debug=True)
