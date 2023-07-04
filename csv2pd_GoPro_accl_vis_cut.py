# //Goproの3軸加速度データを可視化する
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
        df.columns = ["acc_x", "acc_y", "acc_z"]
    elif file_extension == ".pickle":
        df = pd.read_pickle(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Visualize acc_x data
    plt.plot(df["acc_x"])
    plt.xlabel("Index")
    plt.ylabel("Acceleration X")
    plt.title("Acceleration GoPro-X over index")
    plt.show()

    # Save data as a pickle file if a save file path is specified
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



