var userid = getCookie("userid");
var password = getCookie("password");
if (userid == "" || password == "") {
	$(location).attr("href", "login");
}
//Check Login
$.post("api/reader_login", { "certificateNo": userid, "password": password }, function (data) {
	if (data.result != "yes") {
		$(location).attr('href', 'login');
	}
	else {
		console.log("login result: yes");
		$(document).ready(function () {
			$("#user-id").text(userid);
		});
	}
}, "json");
// 动态效果
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

	$("#sign-out").click(function () {
		removeCookie("userid");
		removeCookie("password");
		$(location).attr('href', '/');
	});
	
});

/********************************************************************************/
$(document).ready(function () {
	function insertRow(num) {
		var html = "<tr>";
		for (var i = 0; i < num; i++)
			html += "<td class='text-center'></td>";
		html += "</tr>";
		$(this).append(html);
	}

	function deltDate(date) {
		var cDate = new Date();
		var tDate = Date(date);
		return parseInt((cDate - tDate) / 1000 / 60 / 60 / 24);
	}

	function getDate(date) {
		var myDate = new Date(date);
		return myDate.toDateString();
	}

	function head(res, item, i) {
		var tr = item.children("tr:eq(" + i + ")");
		var html = "<p>No." + (i + 1) + "</p>";
		tr.children("td:eq(0)").append(html);
		if (res[i].cover == "null") res[i].cover = "../static/img/nothing.png";
		html = "<img src='" + res[i].cover + "'/>";
		tr.children("td:eq(1)").append(html);
		tr.children("td:eq(1)").css({ padding: "0" });
		html = "<a href='bookinfo?search=" + res[i].ISBN + "'><p>";
		html += res[i].title + "</p></a>";
		tr.children("td:eq(2)").append(html);
		html = "<p>" + res[i].ISBN + "</p>"
		tr.children("td:eq(3)").append(html);
		return tr;
	}

	function load() {
		var item = $("#" + $(this).attr("id") + "-detail").find("tbody");
		console.log("load");
		$.get("api/reader_lend_list", { "certificateNo": userid }, function (data, status) {
			console.log("get data");
			if (status == "success") {
				console.log("success");
				item.empty();
				var res = data.result;
				var num = data.total;
				for (var i = 0; i < num; i++) {
					insertRow.call(item, 6);
					var tr = head(res, item, i);
					html = "<p>" + res[i].bookID + "</p>";
					tr.children("td:eq(3)").append(html);
					html = "<p>" + getDate(res[i].borrowTime) + "</p><p ";
					if (deltDate(res[i].dueTime) > 0) html += " class='overdue' ";
					html += ">" + getDate(res[i].dueTime) + "</p>";
					tr.children("td:eq(4)").append(html);
					html = "<button class='btn'>ReNew</button>";
					tr.children("td:eq(5)").append(html);
				}
				item.find("button").click(function () {
					var bookid = $(this).parents("tr").children("td:eq(3)").children("p:eq(1)").text();
					var modal = $("#myModal div.modal-body");
					$.post("api/renew", { bookID: bookid }, function (data, status) {
						console.log("get");
						if (status == "success") {
							if (data.result == "yes") {
								modal.text("Success! The book has been renewed.");
								load.call($("#current-books"));
							}
							else modal.text("Sorry! " + data.reason);
						} else {
							modal.text("Sorry. The server request failed!");
						}
						$("#myModal").modal('toggle');
					}, "json");
				});
			} else {
				alert("Sorry.The request to sever failed!");
			}
		}, "json");
	}
	load.call($("#current-books"));
	$("#current-books").click(load);

	$("#borrow-history").click(function () {
		var item = $("#" + this.id + "-detail").find("tbody");	
		$.get("api/reader_lend_history", { "certificateNo": userid }, function (data, status) {
			if (status == "success") {
				item.empty();
				var res = data.result;
				var num = data.total;
				for (var i = 0; i < num; i++) {
					insertRow.call(item, 5);
					var tr = head(res, item, i);
					html = "<p>" + res[i].bookID + "</p>";
					tr.children("td:eq(3)").append(html);
					html = "<p>" + getDate(res[i].borrowTime) + "</p>";
					html += "<p>" + getDate(res[i].returnTime) + "</p>";
					tr.children("td:eq(4)").append(html);
				}
			} else {
				alert("Sorry.The server request failed!");
			}
		}, "json");
	});
});



