import sys
import pandas as pd

def read_csv_file(file_path):
    # ファイルからデータを読み込む
    df = pd.read_csv(file_path, header=None)

    # カラム名を設定
    df.columns = ["acc_x", "acc_y", "acc_z"]

    print(df)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        read_csv_file(file_path)
