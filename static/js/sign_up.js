$(document).ready(function(){
	$("form").submit(function(){
		var userid = $("input:eq(0)").val();
		var password = $("input:eq(2)").val();
		var email = $("input:eq(3)").val();
		var name = $("input:eq(4)").val();
		 $.ajax({  
            type: "POST",  
            url: "http://47.95.205.76/api/signup",
            data: {"username":userid,"password":password,"name":name,"email":email},  
            dataType:"json",  
            async:false,  
            cache:false,  
            success: function(data){
                console.log(data);
                if(data.result=="yes")
                {
                    alert("Sign Up Succeeded!");
                    window.open("http://47.95.205.76/login");
                }
                else
                    alert(data.reason);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Server Error.\nstatus: "+XMLHttpRequest.status+"\nreadyState: "+XMLHttpRequest.readyState+"\ntextStatus: "+textStatus);
            }
        });
	});
});
function validatePassword(){
  var password = document.getElementById("password");
  var confirm_password = document.getElementById("confirm_password");;
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
    $("#confirm").addClass("has-error");
  } else {
    confirm_password.setCustomValidity('');
    $("#confirm").removeClass("has-error");
  }
}
