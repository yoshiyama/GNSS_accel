# python peak_get.py /mnt/c/Users/survey/Desktop/ACCL_Sync/20230609/GoPro_ACCL/accl_all+id.pickle /mnt/c/Users/survey/Desktop/ACCL_Sync/20230609/TML_ACCL/f008+009_no_header.pickle acc_x accl --start1 27000 --end1 101000 --start2 18300 --end2 55500 --distance1 5000 --distance2 3000

# python peak_get.py /mnt/c/Users/survey/Desktop/ACCL_Sync/20230609/GoPro_ACCL/accl_all+id.pickle /mnt/c/Users/survey/Desktop/ACCL_Sync/20230609/TML_ACCL/f008+009_no_header.pickle acc_y accl --start1 936000 --end1 1003000 --start2 478000 --end2 511000 --distance1 6000 --distance2 3000

# python peak_get_merge.py /mnt/c/Users/survey/Desktop/ACCL_Sync/20230609/GoPro_ACCL/accl_all+id.pickle /mnt/c/Users/survey/Desktop/ACCL_Sync/20230609/TML_ACCL/f008+009_no_header.pickle acc_y accl --start1 [27000,936000] --end1 [101000,1003000] --start2 [18300,478000] --end2 [55500,511000] --distance1 6000 --distance2 3000

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.stats import pearsonr
import numpy as np
from sklearn.linear_model import LinearRegression

# コマンドライン引数を解析
parser = argparse.ArgumentParser()
parser.add_argument("file1", help="Path to the first pickle file")
parser.add_argument("file2", help="Path to the second pickle file")
parser.add_argument("column1", help="Column name for the first data set")
parser.add_argument("column2", help="Column name for the second data set")
parser.add_argument("--start1", type=int, nargs=2, help="Start of ranges for first data set", default=[0, 0])
parser.add_argument("--end1", type=int, nargs=2, help="End of ranges for first data set", default=[100, 100])
parser.add_argument("--start2", type=int, nargs=2, help="Start of ranges for second data set", default=[0, 0])
parser.add_argument("--end2", type=int, nargs=2, help="End of ranges for second data set", default=[100, 100])
parser.add_argument("--distance1", type=int, help="Minimum horizontal distance (in number of data points) between neighboring peaks for first data set", default=200)
parser.add_argument("--distance2", type=int, help="Minimum horizontal distance (in number of data points) between neighboring peaks for second data set", default=200)
args = parser.parse_args()

# データの読み込み
data1 = pd.read_pickle(args.file1)[args.column1]
data2 = pd.read_pickle(args.file2)[args.column2]

# 特定の区間と列を指定してピークを見つける
data1_combined = pd.concat([data1[args.start1[0]:args.end1[0]], data1[args.start1[1]:args.end1[1]]])
data2_combined = pd.concat([data2[args.start2[0]:args.end2[0]], data2[args.start2[1]:args.end2[1]]])

peaks1, _ = find_peaks(data1_combined, height=0, distance=args.distance1)
peaks2, _ = find_peaks(data2_combined, height=0, distance=args.distance2)

# ピークの数が異なる場合、少ない方のピークの数で調整
min_length = min(len(peaks1), len(peaks2))
peaks1 = peaks1[:min_length]
peaks2 = peaks2[:min_length]

# 結果をグラフにプロット
plt.figure(figsize=(12, 6))

# データ1のプロット
plt.subplot(2, 1, 1)
plt.plot(data1_combined)
plt.plot(data1_combined.index[peaks1], data1_combined.iloc[peaks1], "x")
plt.title('Data 1')

# データ2のプロット
plt.subplot(2, 1, 2)
plt.plot(data2_combined)
plt.plot(data2_combined.index[peaks2], data2_combined.iloc[peaks2], "x")
plt.title('Data 2')

plt.tight_layout()
plt.show()

# ピークのインデックスをプロット
plt.figure(figsize=(6, 6))
plt.scatter(peaks1, peaks2)

# 近似直線を計算
z = np.polyfit(peaks1, peaks2, 1)
p = np.poly1d(z)

# 近似直線をプロット
plt.plot(peaks1, p(peaks1), color='r')
plt.xlabel('Peak index of Data 1')
plt.ylabel('Peak index of Data 2')

# 近似式を表示
print(f'Approximation formula: {p}')

plt.show()

# ピークのインデックス間の相関係数を計算
corr, _ = pearsonr(peaks1, peaks2)
print(f'Correlation coefficient between the peak indices: {corr}')

# ピークのインデックスを保存
df = pd.DataFrame({'Data1_Peak_Index': data1_combined.index[peaks1], 'Data2_Peak_Index': data2_combined.index[peaks2]})
df.to_csv('peaks.csv', index=False)
