import os
import cv2
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler

# Path to the directory containing the frames
directory = 'E:/ASEB/3rd Year/Maths/End Sem Final/extracted_frames/testing/segmented_12'

# Initialize an empty list to store the frames
segmented_frames = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Construct the full path to the frame
        frame_path = os.path.join(directory, filename)
        # Read the frame and append it to the list
        frame = cv2.imread(frame_path)
        segmented_frames.append(frame)
    else:
        continue

print("The Segmented Frames are loaded: ", len(segmented_frames))

# Assuming each segmented frame is a 2D array, reshape it into a 1D array for clustering
flattened_segments = [frame.flatten() for frame in segmented_frames]

# Standardize the data
scaler = StandardScaler()
flattened_segments_standardized = scaler.fit_transform(flattened_segments)

# Apply DBSCAN clustering
eps = 0.5  # Adjust the distance threshold based on your data
min_samples = 5  # Adjust the minimum number of samples for a cluster
min_cluster_size = 20  # Adjust the minimum cluster size

dbscan = DBSCAN(eps=eps, min_samples=min_samples)
cluster_labels = dbscan.fit_predict(flattened_segments_standardized)
print(cluster_labels)
# Filter out frames belonging to smaller clusters
unique_clusters, cluster_counts = np.unique(cluster_labels, return_counts=True)
valid_clusters = unique_clusters[cluster_counts >= min_cluster_size]
anomalies = np.where(np.isin(cluster_labels, valid_clusters, invert=True))[0]
print("Anomalous Frames:", anomalies)
# Print the file names of anomalous frames
print("Anomalous Frame File Names:")
for idx in anomalies:
    print(os.path.basename(os.path.join(
        directory, os.listdir(directory)[idx])))
