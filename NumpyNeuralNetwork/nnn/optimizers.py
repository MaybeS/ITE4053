from typing import List

import numpy as np


class Optimizer(object):

    def __init__(self, *args, **kwargs):
        self.iteration = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.iteration += 1

    def get_update(self, params: np.ndarray, grads: np.ndarray):
        pass


class SGD(Optimizer):

    def __init__(self, lr: float = .001, **kwargs):
        super(SGD, self).__init__(**kwargs)

        self.lr = lr

    def get_update(self, params: np.ndarray, grads: np.ndarray):
        return params - self.lr * grads


class Adam(Optimizer):

    def __init__(self, lr: float = .001, beta1: float = .9, beta2: float = .999,
                 epsilon: float = 1e-8, decay: float = .0, **kwargs):
        super(Adam, self).__init__(**kwargs)

        self.lr = lr
        self.beta1, self.beta2 = beta1, beta2
        self.decay = decay
        self.epsilon = epsilon
        self.initial_decay = decay

    def get_update(self, params: List[np.ndarray], grads: List[np.ndarray]):
        lr = self.lr * ((1. / (1. + self.deacy * self.iteration)) if self.initial_decay > 0. else 1) * \
             (np.sqrt(1. - np.power(self.beta2, 1+self.iteration)) / (1. - np.power(self.beta1, 1+self.iteration)))

        results = np.zeros(np.size(params, 0))

        if not hasattr(self, 'ms') and not hasattr(self, 'vs'):
            self.ms = [np.zeros(p.shape) for p in params]
            self.vs = [np.zeros(p.shape) for p in params]

        for i, (p, g, m, v) in enumerate(zip(params, grads, self.ms, self.vs)):
            self.ms[i] = (self.beta1 * m) + (1. - self.beta1) * g
            self.vs[i] = (self.beta2 * v) + (1. - self.beta2) * np.square(g)
            results[i] = (p - lr * self.ms[i] / (np.sqrt(self.vs[i]) + self.epsilon)).reshape(params[i].shape)

        return results
