import h5py

class H5Reader:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self._open()

    def _open(self):
        self.file = h5py.File(self.filename, "r")

    def close(self):
        self.file.close()

    def read(self, key):

        if key in self.file.keys():
            return self.file[key]   
        else:
            raise KeyError(f"Key {key} not found in {self.filename}")
        