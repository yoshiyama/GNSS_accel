import matplotlib.pyplot as plt
import pandas as pd
import sys
from scipy.fft import fft, ifft
import numpy as np

# コマンドライン引数からpickleファイルのパスを取得
pickle_file = sys.argv[1]

# pickleファイルを読み込み、DataFrameを作成
df = pd.read_pickle(pickle_file)
print(df)

# ローパスフィルタのカットオフ周波数を設定
low_cutoff_frequency = 0.0003

# ハイパスフィルタのカットオフ周波数を設定
high_cutoff_frequency = 0.000

# すべての列に対してループを回す
for column in df.columns:
    # データからフーリエ変換を実行
    N = df[column].size
    yf = fft(df[column].values)  # Numpy配列に変換
    xf = np.linspace(0.0, 0.5, N // 2)

    # ローパスフィルタを適用
    yf[int(low_cutoff_frequency * N):] = 0  # N//2 を超える周波数成分を0に設定

    # ハイパスフィルタを適用
    yf[:int(high_cutoff_frequency * N)] = 0  # N//2 以下の周波数成分を0に設定

    # 逆フーリエ変換を実行
    filtered_data = np.real(ifft(yf) / N)  # スケーリングするためにNで割る

    # グラフをプロット
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, filtered_data)
    plt.title(f"Band-pass Filtered Signal for {str(column)}")
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()

# すべての列に対してループを回す
for column in df.columns:
    # データからフーリエ変換を実行
    N = df[column].size
    yf = fft(df[column].values)  # Numpy配列に変換
    xf = np.linspace(0.0, 0.5, N // 2)

    # フーリエ変換後の数値を出力
    print(f"For column {str(column)}, the FFT results are as follows:")
    print("Frequency:", xf)
    print("Magnitude:", 2.0/N * np.abs(yf[0:N//2]))
    print()

    plt.figure()  # 新しい図を作成
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))  # グラフをプロット
    plt.title(str(column) + ' - FFT')  # グラフのタイトルを設定
    # plt.xlim([0, 0.00003])  # 例：x軸を0から0.1までの範囲に設定
    plt.xlim([0, 0.5])  # 例：x軸を0から0.1までの範囲に設定

    plt.xlabel('frequency')  # x軸のラベルを設定
    plt.ylabel('magnitude')  # y軸のラベルを設定
    plt.show()  # グラフを表示

# 'frame'列を除くすべての列に対してループを回す
for column in df.columns:
    plt.figure()  # 新しい図を作成
    plt.plot(df.index, df[column])  # グラフをプロット
    plt.title(column)  # グラフのタイトルを設定
    plt.xlabel('index')  # x軸のラベルを設定
    plt.ylabel('value')  # y軸のラベルを設定
    plt.show()  # グラフを表示
#
