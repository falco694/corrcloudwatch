// メトリクスを絞り込む
function filter_metrics() {
    // フィルターテキストを取得
    var metrics_filter = $('input[name="metrics_filter"]')[0];
    var values = metrics_filter.value

    // メトリクスリストを取得
    var selectBox = $('select[name="list_metrics"]')[0];
    var items = selectBox.children;
    if (values == "") {
        for (var i = items.length - 1; i >= 0; i--) {
            if ($(items[i])[0].tagName == "SPAN") {
                $(items[i].children[0]).unwrap();
            }
            set_message("メトリクスフィルターが選択されていません");
        }
        return;
    }

    var words = values.split(" ");
    var words = $.grep(words, function (e) {
        return e !== "";
    });
    for (var i = items.length - 1; i >= 0; i--) {
        if ($(items[i])[0].tagName == "SPAN") {
            $(items[i].children[0]).unwrap();
        }
    }

    words.forEach(function (value) {
        var reg = new RegExp(".*" + value + ".*", "i");
        // 先頭の初期選択肢は常に表示する
        for (var i = items.length - 1; i >= 1; i--) {
            if (!items[i].textContent.match(reg)) {
                if ($(items[i])[0].tagName == "OPTION") {
                    $(items[i]).wrap("<span>");
                }
                items[i].selected = false;
            }
            selectBox.children[0].selected = true;
        }
    });

    var result_count = 0;
    for (var i = items.length - 1; i >= 0; i--) {
        if ($(items[i])[0].tagName == "OPTION") {
            result_count++
        }
    }

    set_message(`検索ワード:${words}, ヒット数:${result_count - 1}`);
}

// 選択したメトリクスを下に追加する
function add_metrics() {

    // 現在選択されているメトリクスの値を取得する
    var list_metrics = $('select[name="list_metrics"]');

    var metrics_val = list_metrics.val();
    var metrics_index = list_metrics.prop("selectedIndex");

    if (metrics_index == 0) {
        set_message("メトリクスが選択されていません");
        return;
    }

    // 既に選択されていた場合はアラート表示し、追加しない
    var selected_metrics = false
    $('input[name="target_metrics"]').each(function () {
        if ($(this).val() == metrics_val) {
            set_message("選択済みのメトリクスです");
            selected_metrics = true
        }
    });

    if (selected_metrics) {
        return;
    }

    // 現在の選択数
    var selected_count = $('input[name="target_metrics"]').length;

    // 相関出力の際のラベルとなるテキストを表示
    // ラベルの文字列を作成
    var edit = metrics_val;
    var metricName = edit.split(",")[1];
    if (edit.split(",").length > 2) {
        var Dimensions_value = edit.split(",")[2].split("=")[1];
        var labelstr = metricName + "_" + Dimensions_value;
    } else {
        var labelstr = metricName;
    }

    $('<input>', {
        id: `target_metrics_label_${selected_count}`,
        type: "text",
        name: "target_metrics_label",
        value: `${labelstr}`,
        class: "form-control metrics",
        html: `${labelstr}&nbsp;`,
    }).appendTo('div[name="target_metrics_group"]');

    // テキストボックスにて選択したメトリクスを表示
    $('<input>', {
        id: `target_metrics_${selected_count}`,
        type: "text",
        name: "target_metrics",
        value: `${metrics_val}`,
        class: "form-control metrics",
        readonly: "readonly",
    }).appendTo('div[name="target_metrics_group"]');

    // 統計選択を表示
    var statistics_html = $('select[name="statistics"]').html();
    var statistics_index = $('select[name="statistics"]').prop("selectedIndex");
    $('<select>', {
        id: `target_metrics_statistics_${selected_count}`,
        name: "target_metrics_statistics",
        class: "form-control statistics",
        html: `${statistics_html}`,
    }).appendTo('div[name="target_metrics_group"]');

    $(`#target_metrics_statistics_${selected_count}`).prop(
        "selectedIndex", `${statistics_index}`
    );

    // マイナスボタンを作成
    $('<button>', {
        id: `metricsminus_${selected_count}`,
        type: "button",
        value: `${metrics_val}`,
        class: "btn btn-default",
        onclick: "del_metrics(this);",
        html: "<i class='fa fa-minus' aria-hidden='true'></i> 削除",
    }).appendTo('div[name="target_metrics_group"]');

    set_message("メトリクスを追加しました");
}

// メトリクス選択削除
function del_metrics(value) {
    var index = value.id.split("_")[1];
    $(`#target_metrics_label_${index}`).remove();
    $(`#target_metrics_${index}`).remove();
    $(`#${value.id}`).remove();
};

// 相関分析実行
function run_corr() {
    message = ""
    if ($('input[name="target_metrics"]').length < 3) {
        message += "3つ以上のメトリクスを選択してください<br>"
    };

    if ($('input[name="start_datetime"]').val() == "" || $('input[name="end_datetime"]').val() == "") {
        message += "開始日時と終了日時どちらとも指定してください"
    } else if ($('input[name="start_datetime"]').val() >= $('input[name="end_datetime"]').val()) {
        message += "終了日時には開始日時より後を指定してください"
    }

    if (message != "") {
        set_message(message, level = "warning");
        push_message(message)
        return false
    }
};

// 日付入力補助
function set_date(start, end) {
    $('input[name="start_datetime"]').val(
        start.format('YYYY-MM-DD HH:mm')
    );
    $('input[name="end_datetime"]').val(
        end.format('YYYY-MM-DD HH:mm')
    );
}

function set_relative_date(period) {

    start = moment();
    end = moment();
    switch (period) {
        case "days":
            start = moment().add(-1, "days");
            break;
        case "week":
            start = moment().add(-1, "week");
            break;
        case "month":
            start = moment().add(-1, "month");
            break;
        case "years":
            start = moment().add(-1, "years");
            break;
        default:
            break;

    }

    set_date(start, end);
}

$(function () {});
