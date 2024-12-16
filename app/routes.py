import json
from urllib.parse import urlparse

from flask import Blueprint, jsonify
from flask_pydantic import validate
from schemas.url_input import URLInput
from core.predictor import URLPredictor
from core.model_loader import ModelLoader
from pytorch_pretrained_bert import BertTokenizer
from config import MODEL_PATH, VOCAB_FILE, DEVICE, BLOCKLIST_FILE

bp = Blueprint("routes", __name__)

model = ModelLoader.load_model(MODEL_PATH, DEVICE)
tokenizer = BertTokenizer(vocab_file=VOCAB_FILE)

with open(BLOCKLIST_FILE, "r") as f:
    BLOCKLIST = set(json.load(f))


@bp.route("/predict", methods=["POST"])
@validate()
def predict(body: URLInput):
    try:
        url = str(body.url)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '').split(':')[0]  # Pastikan menghilangkan port jika ada

        if any(domain == blocked_domain or domain.endswith(f".{blocked_domain}") for blocked_domain in BLOCKLIST):
            return jsonify({"status": "success", "data": {"url": url, "prediction": "blocked",
                                                          "reason": "URL matches a blocked domain"}}), 200

        prediction, score = URLPredictor.predict_url(model, tokenizer, url, DEVICE)
        return jsonify({"status": "success", "data": {"url": url, "prediction": prediction, "score": score}}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint health check
@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "success", "message": "API is healthy."}), 200
