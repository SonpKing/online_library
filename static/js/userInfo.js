var userid = getCookie("userid");
var password = getCookie("password");

// 打开Submenu的动态效果
$(document).ready(function () {
	function fetchNurl(ch) {
		var it = $(this).find(".icon-change");
		var url = it.css("background-image");
		var indx = url.substring(url.length - 7, url.length - 6);
		var nurl = "url(../static/img/" + ch + indx + ".png)";//千万注意
		it.css("background-image", nurl);
	}

	$('#sidebar .sidebar-menu li > a').click(function () {// 显示不同操作时的主界面
		var last = $('.active');
		last.removeClass('active');
		$(this).addClass("active");
		fetchNurl.call(last, 3);
		fetchNurl.call(this, 4);
		var list = $(".detail");
		for (var t = 0; t < list.length; t++)
			list[t].style.display = "none";
		$("#" + this.id + "-detail").css("display", "block");
	});


	$('#arrow').click(function () {
		var bar = $('#sidebar');
		var cont = $('#right-display');
		if (bar.hasClass("hidebar")) {
			$(this).find("img").attr("src", "../static/img/left.png");
		} else {
			$(this).find("img").attr("src", "../static/img/right.png");
		}
		bar.toggleClass("hidebar");
		cont.toggleClass("leftcont");
	});

	$("#userRecord").click(function () {
		window.location.href = "userIndex";
	});

	$("#sign-out").click(function () {
		removeCookie("userid");
		removeCookie("password");
		$(location).attr('href', '/');
	});
});



/********************************************************************************/

function submitPWD() {
	var InfoX = document.getElementById('oldPWD').value;
	var InfoY = document.getElementById('newPWD').value;
	var InfoZ = document.getElementById('confirmPWD').value;
	//var Infog = document.getElementById('port');


	if (InfoY.length < 6) {
		alert("The password is at least 6 bits");
		$('#notificationTable').attr("style", "width:400px;text-align:center;margin: 0 auto;margin-bottom:0px");
	}

	else if (InfoY.length > 16) {
		alert("The password is at most 16 bits");
	}

	else if (InfoX != password) {
		alert("The old password is wrong");
	}

	else if (InfoY != InfoZ) {
		alert("The password should be consistent");
	}

	else {
		$.post("api/change_info", { "certificateNo": userid, "password": InfoY },
			function (data) {
				alert(data.result + '\n' + data.reason);
				if (data.result == 'yes') {
					removeCookie("userid");
					removeCookie("password");
					window.location.href = "login";
				}

			}, "json");
	}

}

$(document).ready(function () {


	if (userid == "") {
		alert("Please login first");
		window.location.href = "login";
	}
	else {
		document.getElementById('user-id').innerHTML = userid;

		function getInfo() {
			$.get(" api/user_info", { "certificateNo": userid }, function (data) {
				var InfoA = data.result[0].borrowedNumber;
				var InfoB = data.result[0].certificateNo;
				var InfoC = data.result[0].name;
				var InfoD = data.result[0].password;
				var InfoE = new Date(data.result[0].registerTime);
				InfoE = InfoE.toDateString();

				document.getElementById('textID').innerHTML = InfoB;
				document.getElementById('textName').innerHTML = InfoC;
				document.getElementById('textRegister').innerHTML = InfoE;
			}, "json");
		}

		function load() {
			$("#Alter-PWD").hide();
			$("#MyInfomation").show();
			getInfo();
			console.log("load");
		}
		load.call($("#My-Information"));
		$("#My-Information").click(load);

		$("#Alter-Password").click(function () {
			$("#MyInfomation").hide();
			$("#Alter-PWD").show();
		});



		$("#My-Information").click(function () {
			load();
		});


	}



});