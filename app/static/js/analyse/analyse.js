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
        var ys = {"udp":17,"tcp": 6};
    	if (!data.proto.hasOwnProperty(ys["tcp"]))
    	    data.proto[ys["tcp"]] = 0;
        if (!data.proto.hasOwnProperty(ys["udp"]))
            data.proto[ys["udp"]] = 0;

        $('#div3').highcharts({
            credits:{
                enabled:false
            },
	    chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
		//backgroundColor: 'rgba(0,0,0,0)'
            },
            title: {
                text: '传输层协议'
            },
            tooltip: {
                //headerFormat: '{series.name}<br>',
                //pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
        	formatter:function(){ 
		return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.percentage, 1) +'% ('+Highcharts.numberFormat(this.y, 0, ',') +' 个)';
	    	}
	    },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: '传输层协议',
                data: [
                    
			['TCP',data.proto[ys["tcp"]]],
		    
		    
                    
                        ['UDP',data.proto[ys["udp"]]]
                    ]
                   
                    // {
                    //     name: 'Chrome',
                    //     y: 12.8,
                    //     sliced: true,
                    //     selected: true
                    // },
               
            }]
        });

        $('#div5').highcharts({
            credits:{
                enabled:false
            },
	    chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
		//backgroundColor: 'rgba(0,0,0,0)'
            },
            title: {
                text: '传输层协议'
            },
            tooltip: {
                //headerFormat: '{series.name}<br>',
                //pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
                formatter:function(){
                return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.percentage, 1) +'% ('+Highcharts.numberFormat(this.y, 0, ',') +' 个)';
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: '不同IP地址数',
                data: [
                    ['源IP',   Object.keys(data.srcIP).length],
                    ['目的IP',   Object.keys(data.dstIP).length]
                    // {
                    //     name: 'Chrome',
                    //     y: 12.8,
                    //     sliced: true,
                    //     selected: true
                    // },
                ]
            }]
        });
       	
        var chart = Highcharts.chart('div7', {
            credits:{
		enabled:false
	    },
	    chart:{
		//backgroundColor: 'rgba(0,0,0,0)'
	    },
	    title: {
                text: '流量密度曲线'
            },
            yAxis: {
                title: {
                    text: '密度'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            xAxis: {
		
                title: {
                    text: '时间'
                },
            	categories: data.segments
            },
            series: [{
		name: "流量密度曲线",
                data: data.cumulate
            }],
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom'
                        }
                    }
                }]
            }
        });


    });          
}
