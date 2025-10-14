from config import *
import numpy as np
from sklearn.cluster import KMeans

class KMeansAlgo:
    def __init__(self, n_clusters= NO_OF_CLUSTERS, max_iters=100, use_library=True):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.use_library = use_library
    
    def getcentroids(self, boxes):
        X = np.array([[box.x_centroid, box.y_centroid] for box in boxes])
        kmeans = KMeans(n_clusters=NO_OF_CLUSTERS, random_state=0, n_init='auto')
        kmeans.fit(X)
        labels = kmeans.predict(X)
        for box, label in zip(boxes, labels):
            box.centroid_class = int(label)
        return boxes
