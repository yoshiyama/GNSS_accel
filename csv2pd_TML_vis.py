import sys
import pandas as pd
import matplotlib.pyplot as plt
import os


def read_and_plot_data(file_path, save_file_path=None):
    # Check file extension
    _, file_extension = os.path.splitext(file_path)

    # Read data from file based on its format
    if file_extension == ".csv":
        df = pd.read_csv(file_path, header=None)
        # Set column names
        df.columns = ["no", "time", "accl", "strain"]
    elif file_extension == ".pickle":
        df = pd.read_pickle(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Visualize accl data
    # plt.plot(df["time"], df["accl"], label='Acceleration')
    plt.plot(df.index, df["accl"], label='Acceleration')

    # Visualize strain data
    # plt.plot(df["time"], df["strain"], label='Strain')
    plt.plot(df.index, df["strain"], label='Strain')

    plt.xlabel("Index")
    plt.ylabel("Measurement")
    plt.title("Acceleration and Strain over time")
    plt.legend()
    plt.show()

    # Save data as a pickle file
    if save_file_path is not None:
        df.to_pickle(save_file_path)
        print("Data saved as pickle file: " + save_file_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path> [<save_file_path>]")
    else:
        file_path = sys.argv[1]
        save_file_path = sys.argv[2] if len(sys.argv) >= 3 else None
        read_and_plot_data(file_path, save_file_path)
