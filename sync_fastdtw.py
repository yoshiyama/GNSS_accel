import numpy as np
import pickle
import sys
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def load_pickle_file(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def compute_dtw(series_1, series_2):
    distance, path = fastdtw(series_1, series_2, dist=euclidean)
    return distance, path

def compute_correlation(series_1, series_2):
    series_1 = np.array(series_1).reshape(-1)
    series_2 = np.array(series_2).reshape(-1)
    correlation, _ = pearsonr(series_1, series_2)
    return correlation



def main(file1, start_index1, end_index1, column_name1, file2, start_index2, end_index2, column_name2):
    # Load the time series data from pickle files
    df1 = load_pickle_file(file1)
    df2 = load_pickle_file(file2)

    # Select the data based on the index range for each series
    series_1 = df1.loc[start_index1:end_index1, column_name1]
    series_2 = df2.loc[start_index2:end_index2, column_name2]

    # Convert the pandas series into 1D numpy arrays
    series_1 = series_1.values.reshape(-1, 1)
    series_2 = series_2.values.reshape(-1, 1)

    # Compute the DTW between the two series
    distance, path = compute_dtw(series_1, series_2)
    print(f'DTW distance between the two series: {distance}')

    # Extract the series values along the optimal path
    path_series_1 = [series_1[i] for i, j in path]
    path_series_2 = [series_2[j] for i, j in path]

    # Compute the correlation for the series values along the optimal path
    correlation = compute_correlation(path_series_1, path_series_2)
    print(f'Correlation between the series along the optimal path: {correlation}')

    # Prepare indices for plotting
    indices_1, indices_2 = zip(*path)

    # Plot the two series
    plt.figure(figsize=(10, 6))
    plt.scatter(indices_1, indices_2)
    plt.title('Scatter plot of the matching indices from the two series')
    plt.xlabel('Index in Series 1')
    plt.ylabel('Index in Series 2')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python dtw.py <pickle_file_1> <start_index_1> <end_index_1> <column_name1> <pickle_file_2> <start_index_2> <end_index_2> <column_name2>")
        sys.exit(1)

    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), int(sys.argv[7]), sys.argv[8])


#
# if __name__ == "__main__":
#     if len(sys.argv) != 7:
#         print("Usage: python dtw.py <pickle_file_1> <start_index_1> <end_index_1> <pickle_file_2> <start_index_2> <end_index_2>")
#         sys.exit(1)
#
#     main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
