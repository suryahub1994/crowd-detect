from config import *
from kmeans import *
from db_scan import *


def getcentroidalgorithm():
    if ALGORITHM == "KMEANS":
        return KMeansAlgo()
    if ALGORITHM == "DBSCAN":
        return DBSCANAlgo()
