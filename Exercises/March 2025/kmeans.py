from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

iris = load_iris()

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df = iris_df.drop(['sepal length (cm)', 'sepal width (cm)'], axis=1)

"""
plt.scatter(iris_df.iloc[:, 0], iris_df.iloc[:, 1], c='blue')
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.title('Scatterplot of Iris Dataset')
plt.show()
"""

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Elbow plot
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(iris_df)
    inertia.append(kmeans.inertia_)

ax1.plot(range(1, 11), inertia, marker='o')
ax1.set_xlabel('Number of clusters')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method For Optimal k')

# KMeans clustering plot
kmeans = KMeans(n_clusters=3)
kmeans.fit(iris_df)

iris_df['cluster'] = kmeans.labels_

ax2.scatter(iris_df.iloc[:, 0], iris_df.iloc[:, 1], c=iris_df['cluster'], cmap='viridis')
ax2.set_xlabel(iris.feature_names[2])
ax2.set_ylabel(iris.feature_names[3])
ax2.set_title('KMeans Clustering of Iris Dataset')

plt.tight_layout()
plt.show()