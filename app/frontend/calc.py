import io
import os

import pandas as pd
import requests
import seaborn as sns


def corr(data):
    """
    データの相関係数を出力
    """

    return data.corr(method="pearson")


def pairplot(data):
    """
    散布図行列の画像を作成し、パスを返す
        :param data:行列データ
    """

    base = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, "/")
    filename = "/static/tmp/seaborn_pairplot.png"
    fullpath = base + filename
    if os.path.exists(fullpath):
        os.remove(fullpath)
    pg = sns.pairplot(data)
    pg.savefig(fullpath)

    return
