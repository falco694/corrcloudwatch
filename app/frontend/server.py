import datetime
import os

import pandas as pd
from flask import Flask, render_template, request, url_for

import aws
import calc

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        list_metrics = aws.list_metrics()
        return render_template(
            'index.html',
            list_metrics=list_metrics,
            list_metrics_count=len(list_metrics)
        )
    else:
        metricDataQueries = []

        query = {}
        period = int(request.form["period"])
        statistics = str(request.form["statistics"])
        start_datetime = datetime.datetime.strptime(
            request.form["start_datetime"], '%Y-%m-%d %H:%M'
        )
        end_datetime = datetime.datetime.strptime(
            request.form["end_datetime"], '%Y-%m-%d %H:%M'
        )
        tmp_metrics_id = request.form.getlist("target_metrics_id")
        tmp_metrics = request.form.getlist("target_metrics")

        # i = 0
        # for item in tmp_metrics:
        #     namespace = item.split(",")[0]
        #     metricName = item.split(",")[1]
        #     if len(item.split(",")) == 3:
        #         name = item.split(",")[2].split("=")[0]
        #         value = item.split(",")[2].split("=")[1]

        for index in range(len(tmp_metrics)):
            namespace = tmp_metrics[index].split(",")[0]
            metricName = tmp_metrics[index].split(",")[1]
            if len(tmp_metrics[index].split(",")) == 3:
                name = tmp_metrics[index].split(",")[2].split("=")[0]
                value = tmp_metrics[index].split(",")[2].split("=")[1]

            if len(tmp_metrics[index].split(",")) == 3:
                metricDataQueries.append(
                    {
                        'Id': tmp_metrics_id[index],
                        'Label': tmp_metrics[index],
                        'MetricStat': {
                            'Metric': {
                                'Namespace': namespace,
                                'MetricName': metricName,
                                'Dimensions': [
                                    {
                                        'Name': name,
                                        'Value': value
                                    },
                                ]
                            },
                            'Period': period,
                            'Stat': statistics,
                        }
                    },
                )

            else:
                metricDataQueries.append(
                    {
                        'Id': tmp_metrics_id[index],
                        'Label': tmp_metrics[index],
                        'MetricStat': {
                            'Metric': {
                                'Namespace': namespace,
                                'MetricName': metricName,
                            },
                            'Period': period,
                            'Stat': statistics,
                        }
                    },
                )

        data = aws.get_metrics(
            metricDataQueries=metricDataQueries,
            start_time=start_datetime,
            end_time=end_datetime,
        )

        metrics_datas = []

        labelindex = []
        metrics_data_tmp = {}
        for item in data:
            if len(labelindex) < len(metricDataQueries):
                labelindex.append(
                    {
                        "id": item["Id"],
                        "label": item["Label"]
                    }
                )
                metrics_data_tmp[item["Id"]] = []
            for index in range(len(item["Timestamps"])):
                metrics_data_tmp[item["Id"]].append(
                    {
                        "Timestamps": item["Timestamps"][index],
                        item["Id"]: item["Values"][index],
                    }
                )

        for key in metrics_data_tmp:
            metrics_data = pd.DataFrame(metrics_data_tmp[key])
            metrics_datas.append(metrics_data)

        marge_data = pd.DataFrame()
        try:
            for index in range(len(labelindex)):
                if index > 0:
                    # on_columns = list(
                    #     set(marge_data.columns) & set(
                    #         metrics_datas[index].columns)
                    # )
                    marge_data = marge_data.merge(
                        metrics_datas[index],
                        how="inner",
                        on="Timestamps")
                else:
                    marge_data = metrics_datas[0]

            # 相関係数算出
            corr_data = calc.corr(marge_data)

        except:
            import traceback
            error = traceback.format_exc()
            return render_template(
                'corr_result.html',
                result="データが欠損しているなど<br>{}".format(error)
            )

        return render_template(
            'corr_result.html',
            result=corr_data.to_html(),
            src_data=marge_data[0:5].to_html(),
            labelindex=labelindex
        )


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
