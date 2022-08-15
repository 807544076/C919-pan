//js部分代码
<script type="text/javascript"> 
    	function checkpassword() {
    		var password = document.getElementById("pw").value;//读取第一次输入的口令
    		var repassword = document.getElementById("repw").value;//读取第二次输入的口令
    		
            //判断两次口令输入是否一致
    		if(password == repassword) {
    			 document.getElementById("reminder").innerHTML="<br><font color='green'>两次密码输入一致</font>";//一致时显示绿色文字提示
    			 document.getElementById("submit").disabled = false;
    			
			 }else {
				 document.getElementById("reminder").innerHTML="<br><font color='red'>两次输入密码不一致!</font>";//不一致时显示红色文字提示
	    		 document.getElementById("submit").disabled = true; 
			 } 
    	}
    </script>