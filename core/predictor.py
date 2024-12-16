from core.preprocessor import URLPreprocessor
import torch


class URLPredictor:
    @staticmethod
    def predict_url(model, tokenizer, url, device):
        input_ids, input_types, input_masks = URLPreprocessor.preprocess_url(url, tokenizer)
        input_ids, input_types, input_masks = input_ids.to(device), input_types.to(device), input_masks.to(device)

        with torch.no_grad():
            _, _, y_pred = model([input_ids, input_types, input_masks])
            probabilities = torch.softmax(y_pred, dim=-1).squeeze()
            pred = y_pred.argmax(dim=-1).item()

        score = probabilities[pred].item()
        return "benign" if pred == 0 else "malicious", score
