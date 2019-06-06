import io
import os

import matplotlib
import pandas as pd
import requests
import seaborn as sns

import misc

matplotlib.use("TkAgg")


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

    fullpath = misc.get_filepath_tmp("seaborn_pairplot.png")
    if os.path.exists(fullpath):
        os.remove(fullpath)
    pg = sns.pairplot(data)
    pg.savefig(fullpath)

    return
