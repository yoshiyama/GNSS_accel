# //Goproの3軸加速度データを可視化する

import sys
import pandas as pd
import matplotlib.pyplot as plt

def read_csv_file(file_path):
    # ファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None)

    # カラム名を設定
    df.columns = ["acc_x", "acc_y", "acc_z"]

    # acc_xデータを可視化
    plt.plot(df["acc_x"])
    plt.xlabel("Index")
    plt.ylabel("Acceleration X")
    plt.title("Acceleration GoPro-X over index")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        read_csv_file(file_path)
