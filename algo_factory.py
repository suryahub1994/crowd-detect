from config import *
from kmeans import *


def getcentroidalgorithm():
    if ALGORITHM == "KMEANS":
        return KMeansAlgo()