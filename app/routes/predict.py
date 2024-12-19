import json
from urllib.parse import urlparse

from flask import jsonify
from flask_pydantic import validate
from schemas.url_input import URLInput
from core.predictor import URLPredictor
from core.model_loader import ModelLoader
from pytorch_pretrained_bert import BertTokenizer
from config import MODEL_PATH, VOCAB_FILE, DEVICE, BLOCKLIST_FILE

model = ModelLoader.load_model(MODEL_PATH, DEVICE)
tokenizer = BertTokenizer(vocab_file=VOCAB_FILE)

with open(BLOCKLIST_FILE, "r") as f:
    BLOCKLIST = set(json.load(f))

def predict_routes(bp, limiter, redis_client):
    @bp.route("/predict", methods=["POST"])
    @validate()
    @limiter.limit("5 per minute")
    def predict(body: URLInput):
        try:
            client = redis_client

            url = str(body.url)
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '').split(':')[0]

            cache_key = f"blocklist:{domain}"
            cached_result = client.get(cache_key)

            if cached_result:
                cached_result = json.loads(cached_result)
                print("Cache hit")
                return jsonify(cached_result), 200

            if any(
                    blocked_domain.startswith("*.") and domain.endswith(blocked_domain[1:])
                    or domain == blocked_domain
                    or domain.endswith(f".{blocked_domain}")
                    for blocked_domain in BLOCKLIST
            ):
                response = {
                    "status": "success",
                    "data": {
                        "url": url,
                        "prediction": "blocked",
                        "reason": "URL matches a blocked domain",
                        "score": 1.0
                    }
                }

                client.setex(cache_key, 300, json.dumps(response))
                return jsonify(response), 200

            prediction, score = URLPredictor.predict_url(model, tokenizer, url, DEVICE)
            response = {
                "status": "success",
                "data": {
                    "url": url,
                    "prediction": prediction,
                    "reason": "URL is not in the blocklist",
                    "score": score
                }
            }

            redis_client.setex(cache_key, 300, json.dumps(response))
            return jsonify(response), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
