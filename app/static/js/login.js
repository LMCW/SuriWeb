function validate(){
	// alert(document.getElementById("userName").value) 用这种方式来根据id获取值，注意最后的.value
	if (document.getElementById("userName").value == ""){
		alert("You must enter your userName.");
		return false;
	} else if (document.getElementById("password").value == "") {
		alert("You must enter your password.");
		return false;
	}
	else{
		// 传递给后端
		
	}
}