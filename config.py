import os
import torch
from dotenv import load_dotenv

FLASK_ENV = os.getenv("FLASK_ENV", "development")

if FLASK_ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

UINSA_MODEL_PATH = os.getenv("UINSA_MODEL_PATH", "files/uinsa.pth")
KAGGLE_MODEL_PATH = os.getenv("KAGGLE_MODEL_PATH", "files/600-32.pth")
BERT_PATH = os.getenv("BERT_PATH", "files/charbert-bert-wiki")
VOCAB_FILE = os.getenv("VOCAB_FILE", "files/charbert-bert-wiki/vocab.txt")
BLOCKLIST_FILE = os.getenv("BLOCKLIST_FILE", "files/negative.json")

# MODEL_CONFIGS = {
#     "uinsa-base": {
#         "model_path": os.getenv("UINSA_MODEL_PATH", "files/uinsa.pth"),
#         "vocab_file": os.getenv("VOCAB_FILE", "files/charbert-bert-wiki/vocab.txt"),
#     },
#     "kaggle-base": {
#         "model_path": os.getenv("KAGGLE_MODEL_PATH", "files/600-32.pth"),
#         "vocab_file": os.getenv("VOCAB_FILE", "files/charbert-bert-wiki/vocab.txt")
#     }
# }

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

DEVICE = torch.device("cuda" if os.getenv("DEVICE", "cpu") == "cuda" and torch.cuda.is_available() else "cpu")

PORT = int(os.getenv("PORT", 5000))
CORS_ORIGINS = os.getenv("CORS_ORIGINS_DEV") if FLASK_ENV == "development" else os.getenv("CORS_ORIGINS_PROD")

print(f"Running in {FLASK_ENV} mode on port {PORT}")
