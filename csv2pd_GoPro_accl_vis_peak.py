# //Goproの3軸加速度データを可視化する
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import argrelmax


def read_and_plot_data(file_path, column, start=None, end=None, save_file_path=None):
    # Check file extension
    _, file_extension = os.path.splitext(file_path)

    # Read data from file based on its format
    if file_extension == ".csv":
        df = pd.read_csv(file_path, header=None)
        # Set column names
        df.columns = ["acc_x", "acc_y", "acc_z"]
    elif file_extension == ".pickle":
        df = pd.read_pickle(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Check if the column is valid
    if column not in df.columns:
        raise ValueError(f"Invalid column name: {column}")

    # Visualize the selected column data
    plt.figure(figsize=(10, 6))
    print("column: ",  column)
    plt.plot(df[column], label=f'Acceleration {column}')

    # Find and plot peaks if start and end are specified
    if start is not None and end is not None:
        peaks = argrelmax(df[column].values[start:end])[0]
        plt.plot(peaks + start, df[column].values[peaks + start], "x", label='Peaks')

    plt.xlabel("Index")
    plt.ylabel(f"Acceleration {column}")
    plt.title(f"Acceleration GoPro-{column} over index")
    plt.legend()
    plt.show()

    # Save data as a pickle file if a save file path is specified
    if save_file_path is not None:
        df.to_pickle(save_file_path)
        print("Data saved as pickle file: " + save_file_path)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <file_path> <column_name> <start_index> <end_index> [<save_file_path>]")
    else:
        file_path = sys.argv[1]
        column = sys.argv[2]
        start = int(sys.argv[3])
        end = int(sys.argv[4])
        save_file_path = sys.argv[5] if len(sys.argv) >= 6 else None
        read_and_plot_data(file_path, column, start, end, save_file_path)
