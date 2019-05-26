import pandas as pd

import io
import requests
# response_text = requests.get("https://raw.githubusercontent.com/pandas-dev/pandas/master/pandas/tests/data/iris.csv").text
# df = pd.read_csv(io.StringIO(response_text))

# 相関係数の計算 df.corr(method="pearson") でも結果は同様 デフォルト動作
# df.corr()

# from pandas.tools.plotting import scatter_matrix
# pd.scatter_matrix(df) # 散布図行列を描く

# plt.show() # 対話的に画像を表示する場合

def corr(data):
    """
    データの相関係数を出力
    """
