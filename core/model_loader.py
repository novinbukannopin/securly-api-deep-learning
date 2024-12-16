import torch
from model.Model_PMA import Model

class ModelLoader:
    @staticmethod
    def load_model(model_path, device):
        model = Model().to(device)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        return model
