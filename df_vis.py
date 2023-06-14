import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# コマンドライン引数からファイルパスを取得
file_path = sys.argv[1]

# PickleファイルからDataFrameを読み込み
df = pd.read_pickle(file_path)

# xとyのL2ノルムを計算して新しい列として追加
df['l2_norm'] = np.sqrt(df['x']**2 + df['y']**2)

# DataFrameの内容を表示
print(df)

# # 日時の範囲を指定（データ型を変換）
# start_time = pd.Timestamp('2023-06-09 01:27:00', tz='UTC')
# end_time = pd.Timestamp('2023-06-09 01:32:00', tz='UTC')

# 日時の範囲を指定（データ型を変換）
start_time = pd.Timestamp('2023-06-09 02:42:00', tz='UTC')
end_time = pd.Timestamp('2023-06-09 02:48:00', tz='UTC')

# 指定した範囲のデータを抽出
selected_data = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time) & (df['gps_quality'] == 4)]

# 以降のコードはそのまま


l2_norm = selected_data['l2_norm']

plt.plot(selected_data['timestamp'], l2_norm)
plt.xlabel('Timestamp')
plt.ylabel('L2 Norm')
plt.title('L2 Norm over Time')

plt.show()