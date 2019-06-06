# etc
import os


def str_to_html(rawstr: str):
    """
    文字列に含まれる改行や空白をhtml用に変換します
        :param rawstr:str: 変換する文字列
    """
    result = rawstr
    result = result.replace("\n", "<br>")
    result = result.replace(" ", "&nbsp;")

    return result


def get_filepath_tmp(filename):
    """
    /static/tmp/{filename}のフルパスを取得します
        :param filename: ファイル名
    """

    base = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, "/")
    return base + "/static/tmp/" + filename
