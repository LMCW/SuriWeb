

function insertItem(table, myItem, i) {
    var item = document.createElement('tr');
    item.id = i;

    //创建表项
    var item_id = document.createElement('td');
    item_id.innerText = i;
    var item_status = document.createElement('td');
    if (myItem['isCompleted'] == 0) 
        item_status.innerText = 'no';
    else
        item_status.innerText = 'yes';
    var item_beginTime = document.createElement('td');
    var timestamp = myItem['beginTime'];
    var newDate = new Date();
    newDate.setTime(timestamp * 1000);
    item_beginTime.innerText = newDate.toUTCString();
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
            var data2 = [
                    ];
            for (var i in data.result) {
                data2[i] = {
                    "id":data.result[i].id,
                    "status":0,
                    "beginTime":0,
                    "endTime":0
                };
                if (data.result[i].isCompleted == 0)
                    data2[i].status = "no";
                else
                    data2[i].status = "yes";

                var timestamp = data.result[i].beginTime;
                var newDate = new Date();
                newDate.setTime(timestamp * 1000);
                data2[i].beginTime = newDate.toLocaleString();
                timestamp = data.result[i].endTime;
                newDate.setTime(timestamp * 1000);
                data2[i].endTime = newDate.toLocaleString();
                if (data.result[i].isCompleted == 0)
                    data2[i].endTime = "-";

               
            }            
            var $table = $('#table');
            $table.bootstrapTable({
                classes: 'table table-bordered',
                data:data2,
                hover:false,
                locale:'zh-CN',
                sortable: true,                     //是否启用排序
                sortName : "beginTime",
                sortOrder: "asc", 
                pagination: true,
                pageSize: 10,
                pageNumber:1, 
                pageList: [5,10,15],//可供选择的每页的行数（*）
                sidePagination: "client"
            });
            // var table = document.getElementById("mission_list");
            // for (var i in data.result) {
            //     insertItem(table, data.result[i], i);
            // }
        });
    };
    window.onload = submit_form;
});