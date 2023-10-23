from typing import Dict

import h5py
import torch

from core.device import to_numpy


class H5Writer:
    """H5Writer is a class for writing data to an HDF5 file."""

    def __init__(self, filename, mode="w", compression=None):
        self.filename = filename
        self.mode = mode
        self.compression = compression

        # Create the file
        self.hfile = h5py.File(filename, mode)

    def close(self):
        self.hfile.close()

    def write(self, data: Dict[str, torch.Tensor]):
        for key, value in data.items():

            value = to_numpy(value)

            self.hfile.create_dataset(
                key, data=value, compression=self.compression)


class FeatureWriter(H5Writer):
    """ Feature Writer is a class for writing features to an HDF5 file."""

    def __init__(self, filename, mode="w", compression=None):
        super().__init__(filename, mode, compression)

    def write_features(self, group_name: str, preds: Dict[str, torch.Tensor]):

        try:
            # delete the group if it already exists
            if group_name in self.hfile.keys():
                del self.hfile[group_name]

            # Create the group
            group = self.hfile.create_group(group_name)

            # Write the features
            for key, value in preds.items():
                value = to_numpy(value)
                group.create_dataset(
                    key, data=value, compression=self.compression)

        except OSError as error:
            raise error


class MatchesWriter(H5Writer):
    """ Matches Writer is a class for writing matches to an HDF5 file."""

    def __init__(self, filename, mode="w", compression=None):
        super().__init__(filename, mode, compression)

    def write_matches(self, group_name: str, matches: Dict[str, torch.Tensor]):
        try:
            # delete the group if it already exists
            if group_name in self.hfile.keys():
                del self.hfile[group_name]

            # Create the group
            group = self.hfile.create_group(group_name)

            # Write the features
            for key, value in matches.items():
                value = to_numpy(value)
                group.create_dataset(
                    key, data=value, compression=self.compression)

        except OSError as error:
            raise error
