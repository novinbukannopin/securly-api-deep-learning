from flask import Blueprint
from .health import health_routes
from .predict import predict_routes


def setup_routes(app, limiter, redis_client):
    bp = Blueprint("routes", __name__)

    health_routes(bp, limiter, redis_client)

    predict_routes(bp, limiter, redis_client)

    # batch_predict_routes(bp, limiter, redis_client)

    app.register_blueprint(bp)
