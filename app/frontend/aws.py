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

    result = []
    token = ''

    # 初回取り込み
    response = cloudwatch.list_metrics()
    if "NextToken" in response:
        token = response["NextToken"]

    result.extend(response["Metrics"])
    print("{}件取得".format(len(result)))

    # 2回目以降
    while token is not '':
        response = cloudwatch.list_metrics(NextToken=token)
        token = ''
        if "NextToken" in response:
            token = response["NextToken"]

        result.extend(response["Metrics"])
        print("{}件取得".format(len(result)))

    return result


# TODO: 複数のメトリクスを同時に取得できるようにする
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html?highlight=cloudwatch#CloudWatch.Client.get_metric_data
def get_metrics(
    metricDataQueries,
    start_time=datetime.datetime.now(),
    end_time=datetime.datetime.now()
):
    """
    指定したメトリクスの統計情報を取得します
    """

    # https://aws.amazon.com/jp/cloudwatch/faqs/
    # 期間が 60 秒 (1 分) のデータポイントは、15 日間使用できます。
    # 期間が 300 秒 (5 分) のデータポイントは、63 日間使用できます。
    # 期間が 3600 秒 (1 時間) のデータポイントは、455 日 (15 か月) 間使用できます。
    # days = int(
    #     int(metricDataQueries[0]['MetricStat']['Period']) * 1440 / 3600 / 24)

    result = []
    token = ''

    # 初回取り込み
    response = cloudwatch.get_metric_data(
        MetricDataQueries=metricDataQueries,
        StartTime=start_time,
        EndTime=end_time,
        ScanBy="TimestampAscending",
        MaxDatapoints=5000
    )

    if "NextToken" in response:
        token = response["NextToken"]

    for index in range(len(response["MetricDataResults"])):
        if len(response["MetricDataResults"][index]["Timestamps"]) != 0:
            result.append(response["MetricDataResults"][index])
            print(len(result))

    # 2回目以降
    while token is not '':
        response = cloudwatch.get_metric_data(
            MetricDataQueries=metricDataQueries,
            StartTime=start_time,
            EndTime=end_time,
            NextToken=token,
            ScanBy="TimestampAscending",
            MaxDatapoints=5000
        )
        token = ''
        if "NextToken" in response:
            token = response["NextToken"]

        for index in range(len(response["MetricDataResults"])):
            if len(response["MetricDataResults"][index]["Timestamps"]) != 0:
                result.append(response["MetricDataResults"][index])
                print(len(result))

    return result
