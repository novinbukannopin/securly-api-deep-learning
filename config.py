import os
import torch
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "files/600-32.pth")
BERT_PATH = os.getenv("BERT_PATH", "files/charbert-bert-wiki")
VOCAB_FILE = os.getenv("VOCAB_FILE", "files/charbert-bert-wiki/vocab.txt")
BLOCKLIST_FILE = os.getenv("BLOCKLIST_FILE", "files/blocklist.txt")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

DEVICE = torch.device("cuda" if os.getenv("DEVICE", "cpu") == "cuda" and torch.cuda.is_available() else "cpu")

FLASK_ENV = os.getenv("FLASK_ENV", "development")
CORS_ORIGINS_DEV = os.getenv("CORS_ORIGINS_DEV", "http://localhost:3001")
CORS_ORIGINS_PROD = os.getenv("CORS_ORIGINS_PROD", "")
PORT = os.getenv("PORT", 5000)