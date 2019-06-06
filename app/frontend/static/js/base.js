// 一定時間で消えるメッセージを表示
function set_message(value, level) {
    if (typeof level === 'undefined') level = "info";

    $('[name="message"]').css("color", "");
    $('[name="message"]').fadeIn(0);
    // $('[name="message"]').text(value);
    $('[name="message"]').html(value);
    if (level == "warning") {
        $('[name="message"]').css("color", "Red");
    }
    $('[name="message"]').fadeOut(2000);
    setTimeout(function () {
        $('[name="message"]').text("");
    }, 2000);
}

// プッシュ通知
function push_message(message) {
    if (Push.count() == 0) {
        Push.create("corrcloudwatch", {
            body: message.replace("<br>", "\r"),
            timeout: 2000,
            onClick: function () {
                this.close();
            }
        });
    }
}

$(function () {
    // inputタグの時のみ、enter無効化
    $("input").on("keydown", function (e) {
        if ((e.which && e.which === 13) || (e.keyCode && e.keyCode === 13)) {
            return false;
        } else {
            return true;
        }
    });

    // 日時入力補助UI
    $('input[name*=datetime]').bootstrapMaterialDatePicker({
        weekStart: 0,
        lang: "ja",
        format: "YYYY-MM-DD HH:mm"
    });
});
