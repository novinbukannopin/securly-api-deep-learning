import torch

class URLPreprocessor:
    @staticmethod
    def preprocess_url(url, tokenizer, pad_size=200):
        tokens = tokenizer.tokenize(url)
        tokens = ["[CLS]"] + tokens + ["[SEP]"]
        ids = tokenizer.convert_tokens_to_ids(tokens)
        types = [0] * len(ids)
        masks = [1] * len(ids)

        if len(ids) < pad_size:
            padding = [0] * (pad_size - len(ids))
            ids += padding
            types += padding
            masks += padding
        else:
            ids = ids[:pad_size]
            types = types[:pad_size]
            masks = masks[:pad_size]

        return torch.tensor(ids).unsqueeze(0), torch.tensor(types).unsqueeze(0), torch.tensor(masks).unsqueeze(0)
