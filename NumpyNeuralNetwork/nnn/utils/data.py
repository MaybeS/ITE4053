from typing import Tuple

import numpy as np


class Dataset(object):
    def __init__(self, size: int, shape: Tuple = (2, ),
                 normal: bool = True):
        self.size = int(size)
        self.shape = shape
        self.iteration = 0

        generator = np.random.randn if normal else np.random.rand

        self.X = generator(self.size, *shape)
        self.Y = np.zeros(self.size)

        self.Y[self.X[:, 0] * self.X[:, 0] > self.X[:, 1]] = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteration < self.size:

            yield self.X[self.iteration], self.Y[self.iteration]

            self.iteration += 1

        else:
            raise StopIteration
