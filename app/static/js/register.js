function finishRegister(){
	// alert(document.getElementById("userName").value) 用这种方式来根据id获取值，注意最后的.value
	if (document.getElementById("register-userName").value == ""){
		alert("You must enter your userName.");
		return false;
	} else if (document.getElementById("register-password").value == "") {
		alert("You must enter your password.");
		return false;
	}else if (document.getElementById("register-repeat-password").value == "") {
		alert("You must repeat your password.");
		return false;
	} else if (document.getElementById("mail").value == "") {
		alert("You must enter your email.");
		return false;
	}else if (document.getElementById("info-of-yourself").value == "") {
		alert("You must enter your infomation.");
		return false;
	}
	else{
		if(document.getElementById("register-password").value != document.getElementById("register-repeat-password").value){
			alert("Two password must be the same.")
		}
		else{
			// 传递给后端
		}
		
		
	}
}