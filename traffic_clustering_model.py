import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import style
style.use('ggplot')
from sklearn.cluster import KMeans

#my own data set
server_list=[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3]
usage_time=[]
for _ in range(24):
    usage_time.append(random.randint(1,60))

server1=[]
server2=[]
server3=[]
for i in range(24):
    if server_list[i]==1:
        server1.append(usage_time[i])
    if server_list[i]==2:
        server2.append(usage_time[i])
    if server_list[i]==3:
        server3.append(usage_time[i])

data1=[]
data2=[]
data3=[]

for i in range(len(server1)):
    data1.append([1,server1[i]])
for i in range(len(server2)):
    data2.append([2,server2[i]])
for i in range(len(server3)):
    data3.append([3,server3[i]])

data1=np.array(data1)
data2=np.array(data2)
data3=np.array(data3)

def cluster(data,server,client_no):
    kmeans=KMeans(n_clusters=3)
    kmeans.fit(data)
    centroids=kmeans.cluster_centers_
    labels=kmeans.labels_
    colors=['r.','b.','g.']
    for i in range(len(data)):
        plt.plot(client_no,server[i],colors[labels[i]],markersize=10)
    plt.show()

cluster(data1,server1,1)
cluster(data2,server2,2)
cluster(data3,server3,3)

def range_times(data,server):
    kmeans=KMeans(n_clusters=3)
    kmeans.fit(data)
    labels=kmeans.labels_
    c1=[]
    c2=[]
    c3=[]
    for i in range(len(data)):
        if(labels[i]==1):
            c2.append(server[i])
        if(labels[i]==2):
            c3.append(server[i])
        if(labels[i]==0):
            c1.append(server[i])
    range1=(min(c1),max(c1))
    range2=(min(c2),max(c2))
    range3=(min(c3),max(c3))
    return [range1,range2,range3]
