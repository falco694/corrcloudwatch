"""
AWS全般のハンドリング
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
"""

import boto3
import datetime

cloudwatch = boto3.client('cloudwatch', region_name='ap-northeast-1')


def list_metrics():
    """
    すべてのメトリクスを取得します
    """

    list_metrics = cloudwatch.list_metrics()
    return list_metrics["Metrics"]


# TODO: 複数のメトリクスを同時に取得できるようにする
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html?highlight=cloudwatch#CloudWatch.Client.get_metric_data
def get_metrics(metricDataQueries):
    """
    指定したメトリクスの統計情報を取得します
    """

    # https://aws.amazon.com/jp/cloudwatch/faqs/
    # 期間が 60 秒 (1 分) のデータポイントは、15 日間使用できます。
    # 期間が 300 秒 (5 分) のデータポイントは、63 日間使用できます。
    # 期間が 3600 秒 (1 時間) のデータポイントは、455 日 (15 か月) 間使用できます。
    days = int(
        int(metricDataQueries[0]['MetricStat']['Period']) * 1440 / 3600 / 24)

    return cloudwatch.get_metric_data(
        MetricDataQueries=metricDataQueries,
        StartTime=datetime.datetime.now() - datetime.timedelta(days=days),
        EndTime=datetime.datetime.now()
    )

# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(list_metrics)
