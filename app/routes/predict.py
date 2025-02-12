import json
from urllib.parse import urlparse
import os
import pandas as pd
from flask import jsonify, request
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

RESULTS_FOLDER = "files/test/benign/result"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def batch_predict_routes(bp, limiter, redis_client):
    @bp.route("/batch_predict", methods=["POST"])
    @validate()
    # @limiter.limit("5 per minute")
    def batch_predict():
        try:
            file = request.files.get("file")
            if not file:
                return jsonify({"status": "error", "message": "No file uploaded"}), 400

            urls = json.load(file)  # Membaca file JSON
            results = []
            client = redis_client

            for idx, url in enumerate(urls):
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.replace('www.', '').split(':')[0]
                cache_key = f"blocklist:{domain}"
                cached_result = client.get(cache_key)

                if cached_result:
                    cached_result = json.loads(cached_result)
                    prediction = cached_result["data"]["prediction"]
                else:
                    if any(
                            blocked_domain.startswith("*.") and domain.endswith(blocked_domain[1:]) or
                            domain == blocked_domain or
                            domain.endswith(f".{blocked_domain}")
                            for blocked_domain in BLOCKLIST
                    ):
                        prediction = "blocked"
                    else:
                        prediction, _ = URLPredictor.predict_url(model, tokenizer, url, DEVICE)

                results.append({"idx": idx, "url": url, "hasil": prediction})

            # Simpan hasil ke CSV dengan nama file yang sama (ganti ekstensi ke .csv)
            original_filename = os.path.splitext(file.filename)[0]  # Ambil nama file tanpa ekstensi
            csv_filename = f"{original_filename}.csv"
            csv_path = os.path.join(RESULTS_FOLDER, csv_filename)

            df = pd.DataFrame(results)
            df.to_csv(csv_path, index=False)

            return jsonify({"status": "success", "file": csv_filename}), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
