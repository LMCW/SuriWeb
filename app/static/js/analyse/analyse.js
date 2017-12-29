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
	    if (data.flag == 2)
		alert("未选择任务");
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
	
        $('#myChart3').remove();
	$('#div3').append('<canvas id="myChart"></canvas>');
	
        $('#div5').append('<canvas id="myChart2"></canvas>');
	
        $('#div7').append('<canvas id="myChart3"></canvas>');
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
       	
        var lineChartData = {  
        //表的X轴参数
        labels : [],
        datasets : [
            {
                fillColor : "transparent",     //背景色，常用transparent透明
                strokeColor : "rgba(220,220,220,1)",  //线条颜色，也可用"#ffffff"
                pointColor : "rgba(220,220,220,1)",   //点的填充颜色
                pointStrokeColor : "#fff",            //点的外边框颜色
                data : []      //点的Y轴值
            }
          ]
        }

        for(var i = 0; i < data.segments.length;i++)
        { 
	 lineChartData.labels.push(data.segments[i]);
        }
	for (var i=0; i<data.cumulate.length; i++)
	 lineChartData.datasets[0].data.push(data.cumulate[i]);//将数组arr2中的值写入data
        var defaults = {    
            scaleStartValue :null,     // Y 轴的起始值
            scaleLineColor : "rgb(255,255,255)",    // Y/X轴的颜色
            scaleLineWidth : 3,        // X,Y轴的宽度
            scaleShowLabels : true,    // 刻度是否显示标签, 即Y轴上是否显示文字   
	    xLabelsSkip: 1000,
            scaleLabel : "<%=value%>", // Y轴上的刻度,即文字  
            scaleFontFamily : "'Arial'",  // 字体  
            scaleFontSize : 2,        // 文字大小 
            scaleFontStyle : "normal",  // 文字样式  
            scaleFontColor : "white",    // 文字颜色  
            scaleShowGridLines : true,   // 是否显示网格  
            scaleGridLineColor : "rgba(0,0,0,.05)",   // 网格颜色
            scaleGridLineWidth : 2,      // 网格宽度  
            bezierCurve : false,         // 是否使用贝塞尔曲线? 即:线条是否弯曲     
            pointDot : true,             // 是否显示点数  
            pointDotRadius : 3,          // 圆点的大小  
            pointDotStrokeWidth : 1,     // 圆点的笔触宽度, 即:圆点外层边框大小 
            datasetStroke : true,        // 数据集行程
            datasetStrokeWidth : 2,      // 线条的宽度, 即:数据集
            datasetFill : false,         // 是否填充数据集 
            animation : true,            // 是否执行动画  
            animationSteps : 60,          // 动画的时间   
            animationEasing : "easeOutQuart",    // 动画的特效   
            onAnimationComplete : null    // 动画完成时的执行函数   
            }
	
        var ctx = document.getElementById("myChart3").getContext("2d");
	 window.myLine = new Chart(ctx).Line(lineChartData,defaults); 

    });          
}
