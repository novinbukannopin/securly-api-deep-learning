from flask import Blueprint, jsonify
from flask_pydantic import validate
from schemas.url_input import URLInput
from core.predictor import URLPredictor
from core.model_loader import ModelLoader
from pytorch_pretrained_bert import BertTokenizer
from config import MODEL_PATH, VOCAB_FILE, DEVICE

bp = Blueprint("routes", __name__)

model = ModelLoader.load_model(MODEL_PATH, DEVICE)
tokenizer = BertTokenizer(vocab_file=VOCAB_FILE)


@bp.route("/predict", methods=["POST"])
@validate()
def predict(body: URLInput):
    try:
        url = str(body.url)
        prediction, score = URLPredictor.predict_url(model, tokenizer, url, DEVICE)
        return jsonify({"status": "success", "data": {"url": str(url), "prediction": prediction, "score": score}}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint health check
@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "success", "message": "API is healthy."}), 200
