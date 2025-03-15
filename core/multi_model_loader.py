from pytorch_pretrained_bert import BertTokenizer

from config import DEVICE
from core.model_loader import ModelLoader

class MultiModelLoader:
    models = {}
    tokenizers = {}

    @staticmethod
    def load_model(name, model_path, vocab_file, device):
        model = ModelLoader.load_model(model_path=model_path, device=DEVICE)
        tokenizer = BertTokenizer(vocab_file=vocab_file)
        return model, tokenizer

    @classmethod
    def initialize_models(cls, configs, device):
        for model_name, config in configs.items():
            model_path = config["model_path"]
            vocab_file = config["vocab_file"]
            cls.models[model_name] = {
                "model": ModelLoader.load_model(model_path, device),
                "tokenizer": BertTokenizer(vocab_file=vocab_file)
            }

    @classmethod
    def get_model(cls, model_name):
        return cls.models.get(model_name, None)
