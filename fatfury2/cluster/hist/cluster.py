import numpy
import random
import pickle
import sys

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def create_train_kmeans(data, number_of_clusters):
    k = KMeans(n_clusters=number_of_clusters, n_jobs=2, random_state=0)
    k.fit(data)
    return k

h = sys.argv[1]
H = numpy.load(h)

k = create_train_kmeans(H, int(sys.argv[2]))

Z = []
for i in H:
    p = k.predict([i])
    Z.append(p)

plt.plot(Z)
plt.show()