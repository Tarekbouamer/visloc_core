from abc import ABC

import torch


class ModelInfo(ABC):
    """
    Abstract base class to hold metadata for a deep learning model.
    Designed to be extended for various uses and to accommodate multiple inheritance.
    """

    def __init__(self):
        self._name = None
        self._input_names = None
        self._output_names = None
        self._model_type = None
        self._preprocessing = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def input_names(self):
        return self._input_names

    @input_names.setter
    def input_names(self, value):
        self._input_names = value

    @property
    def output_names(self):
        return self._output_names

    @output_names.setter
    def output_names(self, value):
        self._output_names = value

    @property
    def model_type(self):
        return self._model_type

    @model_type.setter
    def model_type(self, value):
        self._model_type = value

    @property
    def preprocessing(self):
        return self._preprocessing

    @preprocessing.setter
    def preprocessing(self, value):
        self._preprocessing = value

    def metadata(self):
        """
        Returns all metadata of the model as a dictionary.
        """
        return {
            "name": self.name,
            "input_names": self.input_names,
            "output_names": self.output_names,
            "model_type": self.model_type,
            "preprocessing": self.preprocessing,
        }

    def cuda(self, device=None):
        """
        Moves the model to the GPU if available.
        """
        if device is None:
            device = torch.device("cuda")

        return super().cuda(device)
    
    def cpu(self):
        """
        Moves the model to the CPU.
        """
        return super().cpu()
