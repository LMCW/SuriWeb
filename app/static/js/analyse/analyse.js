
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
    alert(obj.value);           
}
