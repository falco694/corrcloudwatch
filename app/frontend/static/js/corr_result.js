// 相関係数の数値に色を付ける
function set_color_corr() {
    var table = $("#corr_table_parent").children()[0]
    var tbody = table.children[1]
    var tr = tbody.children
    for( var i=0,l=tr.length;i<l;i++ ){
        var td = tr[i].children;
        for( var j=1,m=td.length;j<m;j++ ){
            var target = parseFloat(td[j].innerText);
            if(target == 1){
                $(td[j]).css("color", "");
            }
            else if(target > 0.7)
            {
                $(td[j]).css("background-color", "#ff8080");
            }
            else if(target < -0.7)
            {
                $(td[j]).css("background-color", "#8080ff");
            }
            else if(target > 0.4)
            {
                $(td[j]).css("background-color", "#ffd5d5");
            }
            else if(target < -0.4)
            {
                $(td[j]).css("background-color", "#d5d5ff");
            }
        }
    }
}

$(function () {});
