import sys
import pandas as pd
import matplotlib.pyplot as plt


def read_csv_file(file_path):
    # ファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None)

    # カラム名を設定
    df.columns = ["no", "time", "accl", "strain"]

    # acclデータを可視化
    plt.plot(df["time"], df["accl"], label='Acceleration')

    # strainデータも同様に可視化
    plt.plot(df["time"], df["strain"], label='Strain')

    plt.xlabel("Time")
    plt.ylabel("Measurement")
    plt.title("Acceleration and Strain over time")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        read_csv_file(file_path)
