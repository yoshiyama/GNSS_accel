import sys
import pandas as pd

def read_pickle(file_path):
    df = pd.read_pickle(file_path)
    print(df)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        read_pickle(file_path)
