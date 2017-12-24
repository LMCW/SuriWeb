$(function () {
    function submit_form(e) {
  	 $.getJSON('/display', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val(),
            now: new Date().getTime()
        },
        function (data) {
            for (var i in data.result) {
	     	var obj = document.getElementById("mySelect"); //获取select对象
		var optionObj = document.createElement("option"); //创建option对象
		optionObj.value = data.result[i].id;
		optionObj.innerHTML = data.result[i].id;
		optionObj.selected = false;//默认选中
		obj.appendChild(optionObj);  //添加到select
	    }
        });
    };

    window.onload = submit_form;
});

function analyse() {
    var obj = document.getElementById("mySelect"); //获取select对象 
    $.getJSON('/getChart', {
        a: obj.value
    },
    function (data) {
    	if (data.flag == 0)
		alert("开始分析");
	else
		alert("请等待当前分析结束");
    });
}

function refresh() {
    var obj = document.getElementById("mySelect"); //获取select对象 
    $.getJSON('/refresh', {
        a: obj.value
    },
    function (data) {
	if (data.flag == 1) { 
		alert("正在分析中");
		return;
	}
	alert("分析结束");
	$('#myChart').remove();
    	
        $('#myChart2').remove();
	$('#div3').append('<canvas id="myChart"></canvas>');
	
        $('#div5').append('<canvas id="myChart2"></canvas>');
	var pieData = [];  
	var ys = {"udp":17,"tcp": 6};
	if (!data.proto.hasOwnProperty(ys["tcp"]))
	    data.proto[ys["tcp"]] = 0;
        if (!data.proto.hasOwnProperty(ys["udp"]))
            data.proto[ys["udp"]] = 0;
	var value = [data.proto[ys["tcp"]],data.proto[ys["udp"]]];
	var label = ["TCP","UDP"];
            var colorarr = ["#949FB1", "#4D5360"];
            var highlightarr = ["#A8B3C5", "#616774"];
            for (var i = 0; i < 2; i++) {
                pieData[i] = {
                    value: value[i],
                    color: colorarr[i % 2],
                    highlight: highlightarr[i % 2],
                    label: label[i]
                };
            }
            var ctx = document.getElementById("myChart").getContext("2d");
            window.myPie = new Chart(ctx).Pie(pieData);
    
	var pieData2 = [];
	var value2 = [Object.keys(data.srcIP).length, Object.keys(data.dstIP).length];
        var label2 = ["SrcIp","DstIp"];
            var colorarr2 = ["#FDB45C", "#46BFBD"];
            var highlightarr2 = ["#FFC870", "#5AD3D1"];
            for (var i = 0; i < 2; i++) {
                pieData2[i] = {
                    value: value2[i],
                    color: colorarr2[i % 2],
                    highlight: highlightarr2[i % 2],
                    label: label2[i]
                };
            }
            var ctx = document.getElementById("myChart2").getContext("2d");
            window.myPie = new Chart(ctx).Pie(pieData2);
    


    });          
}
