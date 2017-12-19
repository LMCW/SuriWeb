function changeInfo(){
	if (document.getElementById("register-password").value == "") {
		alert("You must enter new password.");
		return false;
	}else if (document.getElementById("register-repeat-password").value == "") {
		alert("You must repeat new password.");
		return false;
	}
	else if (document.getElementById("info-of-yourself").value == "") {
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