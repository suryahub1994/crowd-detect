from config import *
import numpy as np
from sklearn.cluster import DBSCAN

class DBSCANAlgo:
    def __init__(self, eps=EPSILON, min_samples=MIN_SAMPLES, use_library=True):
        self.eps = eps
        self.min_samples = min_samples
        self.use_library = use_library
        self.labels = None

    def getcentroids(self, boxes):
        if len(boxes) == 0:
            return boxes
        X = np.array([[box.x_centroid, box.y_centroid] for box in boxes])
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        db.fit(X)
        self.labels = db.labels_
        for box, label in zip(boxes, self.labels):
            box.centroid_class = int(label)  # -1 will mean noise / unclustered

        return boxes
      
    def getnoofcentroids(self):
        count = 0
        for el in self.labels:
            if el != -1:
                count+=1
        return count
