import torch
from abc import abstractmethod
from torchinfo import summary
from torch import nn


class Model(nn.Module):

    def __init__(self, cfg):
        super().__init__()  # Don't forget to call the superclass initializer
        self.cfg = cfg

    @abstractmethod
    def build_model(self):
        pass

    def train(self, train_loader, val_loader=None):
        raise NotImplementedError("train method is not yet implemented.")

    def evaluate(self, val_loader):
        raise NotImplementedError("evaluate method is not yet implemented.")

    def predict(self, data):
        raise NotImplementedError("predict method is not yet implemented.")

    def save(self, save_path):
        torch.save(self.state_dict(), save_path)

    def load(self, save_path):
        self.load_state_dict(torch.load(save_path))

    def summary(self):
        print(summary(self, input_size=self.cfg['input_shape']))

    def reset_weights(self):
        for m in self.modules():
            if hasattr(m, 'reset_parameters'):
                m.reset_parameters()

        for p in self.parameters():
            p.requires_grad = True

    def fuse(self):
        raise NotImplementedError("Model fusion is not yet supported.")

    def device(self):
        """Returns the device of the model."""
        return next(self.parameters()).device
