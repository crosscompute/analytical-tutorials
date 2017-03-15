import numpy as np
import scipy.spatial.kdtree


class KDTree(object):
    
    def __init__(self, points):
        points = np.array(points)
        self.point_count = len(points)
        self.kdtree = scipy.spatial.kdtree.KDTree(points)
    
    def query(self, x, maximum_count=None, maximum_distance=None):
        x = np.array(x)
        if x.ndim == 1:
            x = np.array([x])
        distances, indices = self.kdtree.query(
            x,
            k=maximum_count or self.point_count,
            distance_upper_bound=maximum_distance or np.inf)
        try:
            return distances[distances != np.inf], indices[indices != self.point_count]
        except (TypeError, IndexError):
            return distances, indices
