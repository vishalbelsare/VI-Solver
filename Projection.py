import numpy as np

from Utilities import *


class Projection:
    def __init__(self):
        pass

    def p(self, data, step, direc):
        print('This function projects the data.')
        return None


class IdentityProjection(Projection):

    def p(self, data, step, direc):
        return data + step * direc


class BoxProjection(Projection):

    def __init__(self, low=0., high=1.):
        self.low = low
        self.high = high

    def p(self, data, step, direc):
        return np.minimum(np.maximum(self.low, data + step * direc), self.high)


class LinearProjection(Projection):
    def __init__(self, low=0., high=1.):
        self.low = low
        self.high = high

    def p(self, data, step, direc):
        # compute the projection values:
        projected = data + (step*direc)
        # do they lie outside of the allowed box?
        projector = np.array([1., 1.])
        if np.max(projected) > self.high and np.max(projected) != 0.0:
            projector[1] = self.high/np.max(projected)
        if np.min(projected) < self.low and np.min(projected) != 0.0:
            projector[0] = self.low/np.min(projected)
        print projected * np.min(projector)
        return projected * np.min(projector)


class RPlusProjection(Projection):

    def p(self, data, step, direc):
        return np.maximum(0, data + step * direc)


class EntropicProjection(Projection):

    def p(self, data, step, direc):
        projected_data = data * np.exp(machine_limit_exp(step, direc) * direc)
        return projected_data / np.sum(projected_data)


class EuclideanSimplexProjection(Projection):
    # Taken from: https://gist.github.com/daien/1272551

    def p(self, data, step, direc, s=1):
        assert s > 0, "Radius s must be strictly positive (%d <= 0)" % s
        data = data + step * direc
        n, = data.shape  # will raise ValueError if data is not 1-D
        # check if we are already on the simplex
        if data.sum() == s and np.alltrue(data >= 0):
            # best projection: itself!
            return data
        # get the array of cumulative sums of a sorted (decreasing) copy of
        # data
        u = np.sort(data)[::-1]
        cssd = np.cumsum(u)
        # get the number of > 0 components of the optimal solution
        rho = np.nonzero(u * np.arange(1, n + 1) > (cssd - s))[0][-1]
        # compute the Lagrange multiplier associated to the simplex constraint
        theta = (cssd[rho] - s) / (rho + 1.0)
        # compute the projection by thresholding data using theta
        w = (data - theta).clip(min=0)
        return w
