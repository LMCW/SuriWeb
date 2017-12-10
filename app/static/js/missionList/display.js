
function insertItem(table, myItem, i) {
    var item = document.createElement('tr');
    item.id = i;

    //创建表项
    var item_id = document.createElement('td');
    item_id.innerText = i;
    var item_status = document.createElement('td');
    item_status.innerText = myItem['isCompleted'];
    var item_beginTime = document.createElement('td');
    item_beginTime.innerText = myItem['beginTime'];
    var item_endTime = document.createElement('td');
    item_endTime.innerText = myItem['endTime'];
   

    //将表项添加进行
    item.appendChild(item_id);
    item.appendChild(item_status);
    item.appendChild(item_beginTime);
    item.appendChild(item_endTime);

    table.appendChild(item);
}


$(function () {
    function submit_form(e) {
        $.getJSON($SCRIPT_ROOT + '/display', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val(),
            now: new Date().getTime()
        },
        function (data) {
            var table = document.getElementById("myTable");
            for (var i in data.result) {
                insertItem(table, data.result[i], i);
            }
        });
    };
    window.onload = submit_form;
});