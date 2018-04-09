function logout() {
	removeCookie("password");
	var url = 'http://47.95.205.76';
	window.location.href = url;
}
function fillBoxes(page, isbn) {
	var title="";
	$.ajax({
		type: "GET",
		url: "https://api.douban.com/v2/book/isbn/" + isbn,
		data: {},
		dataType: "jsonp",
		async: false,
		cache: false,
		success: function (data) {
			console.log(data);
			$("#add_submit").removeAttr("disabled");
			$("#book_detail").css("display", "block");
			$("#book_detail").find("img").attr("src", data.image);
			$("#book_detail").find("#title").text(data.title);
			title = data.title;
			$("#book_detail").find("#author").text(data.author);
			$("#book_detail").find("#publisher").text(data.publisher);
			$("#book_detail").find("#pubdate").text(data.pubdate);
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			$("#book_detail").attr("display", "none");
			alert("Book Not Found!");
			$("#add_submit").attr("disabled", "true");
			$('#add_books_detail').find('#InputISBN').val("");
			$("#add_books_detail").find("input").focus();
		}
	});
	return title;
}
function getFine(bookid, bookCondition) {
	var fine = new Array()
	$.ajax({
		type: "GET",
		url: "http://47.95.205.76/api/get_fine_by_bookID",
		dataType: "json",
		data: { "bookID": bookid, "bookCondition": bookCondition },
		async: false,
		cache: false,
		success: function (data) {
			console.log(data);
			fine[0] = data.overdue_fine;
			fine[1] = data.damage_fine;
			fine[2] = data.lost_fine;
			console.log(fine);
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			// alert("Fine cannot be calculated!\nstatus: "+XMLHttpRequest.status+"; readyState: "+XMLHttpRequest.readyState+"; textStatus: "+textStatus);
			alert("Book is in the library!");
		},
	});
	return fine;
}
function returnBook(bookid) {
	$.ajax({
		type: "POST",
		url: "http://47.95.205.76/api/rebook",
		dataType: "json",
		data: { "bookID": bookid, "bookCondition": 0 },
		async: false,
		cache: false,
		success: function (data) {
			if (data.result == "yes") {
				alert("Return Succeeded!");
				$("#return_books_detail").find("#InputBookId").val("").focus();
			}
			else
				alert("Return Failed!" + data.reason);
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			alert("Submit return\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
		},
	});
}
//Delete damaged or lost book
function deleteBook(bookid) {
	$.ajax({
		type: "POST",
		url: "http://47.95.205.76/api/delete_book",
		dataType: "json",
		data: { "bookID": bookid },
		async: false,
		cache: false,
		success: function (data) {
			if (data.result == "yes") {
				alert("Delete Succeeded!");
			}
			else
				alert("Delete Failed!" + data.reason);
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			alert("Submit return\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
		},
	});
}


function fillBarcode(ids) {
	for (var i = 0; i < ids.length; i++) {
		$("#img" + i).css("display", "block");
		$("#img" + i).JsBarcode(ids[i]);
	}
	for (i; i <= 8; i++) {
		$("#img" + i).css("display", "none");
	}
}
function GetBorrowerByBookId(bookid) {
	var res = "";
	$.ajax({
		type: "GET",
		url: "http://47.95.205.76/api/search_readerID_by_bookID",
		data: { "bookID": bookid },
		dataType: "json",
		async: false,
		cache: false,
		success: function (data) {
			console.log(data);
			res = data.reader_who_borrow[0].readerID;
		}
	});
	return res;
}

//Input ISBN, display all the books which have that ISBN
function displayBooks(table, isbn) {
	$.ajax({
		type: "GET",
		url: "http://47.95.205.76/api/search_each_book_by_ISBN",
		data: { "ISBN": isbn },
		dataType: "json",
		async: false,
		cache: false,
		success: function (data) {
			console.log(data);
			var bookid, status, location;
			var html = "";
			html +=
				'<tbody>' +
				'<th>Book ID</th>' +
				'<th>Status</th>' +
				'<th>Location</th>' +
				'<th>Delete</th>';
			for (var i = 0; i < data.total; i++) {
				bookid = data.bookID_location_state[i].bookID;
				if (data.bookID_location_state[i].state == "1") {
					status = "In Library";
					location = data.bookID_location_state[i].location;
				}
				else if (data.bookID_location_state[i].state == "0") {
					status = "Borrowed Out";
					location = GetBorrowerByBookId(bookid);
				}
				else {
					status = "Unknown";
					location = "Unknown";
				}
				html +=
					'<tr>' +
					'<td class="book_id">' + bookid + '</td>' +
					'<td class="book_status">' + status + '</td>' +
					'<td>' + location + '</td>' +
					'<td><button class="btn btn-danger delete_btn">Delete</button></td>' +
					'</tr>';
			}
			html += '</tbody>';
			table.html(html);
		}
	});
	//Delete Books
	$("#delete_books_detail").find(".delete_btn").click(function () {
		console.log("delete");
		var bookid = $(this).parent().siblings(".book_id").text();
		console.log(bookid);
		$.ajax({
			type: "POST",
			url: "http://47.95.205.76/api/delete_book",
			data: { "bookID": bookid },
			dataType: "json",
			async: false,
			cache: false,
			success: function (data) {
				if (data.result == "yes") {
					alert("Delete Succeeded!");
					$("#delete_books_detail").find(".check").click();
				}
				else {
					alert("Delete Failed!");
				}
			}
		});
	});
}


// 打开Submenu的动态效果
$(document).ready(function () {
	jQuery('#sidebar .sub-menu > a').click(function () {
		var last = jQuery('.sub-menu.open', $('#sidebar'));
		last.removeClass("open");
		jQuery('.arrow', last).removeClass("open");
		jQuery('.sub', last).slideUp(200);
		var sub = jQuery(this).next();
		if (sub.is(":visible")) {
			jQuery('.arrow', jQuery(this)).removeClass("open");
			jQuery(this).parent().removeClass("open");
			sub.slideUp(200);
		} else {
			jQuery('.arrow', jQuery(this)).addClass("open");
			jQuery(this).parent().addClass("open");
			sub.slideDown(200);
		}
	});
});

// 显示不同操作时的主界面
$(document).ready(function () {
	$('.open_detail').click(function () {
		var last = $('.active');
		last.removeClass('active');
		$(this).addClass("active");
		var id = this.id + '_detail';
		var list = document.getElementsByClassName("detail");
		for (var t = 0; t < list.length; t++)
			list[t].style.display = "none";
		document.getElementById(id).style.display = "block";
		$("#" + id).find(":input:first").focus();
	});
});

// 默认登录操作
var userid = getCookie("userid");
var password = getCookie("password");
console.log("ready for default login");
if (userid == "" || password == "") {
	$(location).attr("href", "loginAdmin");
}
else {
	$.ajax({
		type: "POST",
		url: "http://47.95.205.76/api/admin_login",
		data: { "ID": userid, "password": password },
		dataType: "json",
		async: false,
		cache: false,
		success: function (data) {
			if (data.result == "yes") {
				$(function () { document.getElementById('user_id').innerHTML = userid });
			}
			else
				$(location).attr("href", "loginAdmin");
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			alert("Login\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
		},
	});
}


$(document).ready(function () {
	//Userid
	$("#userid").click(function () {
		$(location).attr("href", "userIndex");
	});

	//Sign Out
	$("#signout").click(function () {
		logout();
	});

	//Borrow Books
	$("#borrow_submit").click(function () {
		var bookid = $("#borrow_books_detail").find("#InputBookId").val();
		var userid = $("#borrow_books_detail").find("#InputUserId").val();
		console.log("bookid: " + bookid + " / userid: " + userid);
		if (bookid == "" || userid == "") {
			alert("Book ID and Reader ID cannot be empty!")
		}
		else {
			$.ajax({
				type: "POST",
				url: "http://47.95.205.76/api/borrow",
				data: { "bookID": bookid, "certificateNo": userid },
				dataType: "json",
				async: false,
				cache: false,
				success: function (data) {
					console.log(data);
					if (data.result == "yes") {
						alert("Borrow Succeeded!");
					}
					else
						alert("Borrow Failed!\n" + data.reason);
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Borrow Books\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
				},
			});
		}

		$("#borrow_books_detail").find("#InputBookId").val("").focus();
		$("#borrow_books_detail").find("#InputUserId").val("");
	});

	//Return Books
	var bookid;
	var bookCondition;
	//Checkbox only one option valid
	// $('#condition_checkbox').find('input[type=checkbox]').bind('click', function(){  
	//   	$('#condition_checkbox').find('input[type=checkbox]').not(this).attr("checked", false); 
	//   	bookCondition = $('#condition_checkbox').find('input[type=checkbox]:checked').val();//1 broken; 2 lost; 0 good
	//   	console.log(bookCondition);
	//   	if(bookCondition=="0"){
	//   		$('#calculate_fine').attr('disabled',"true");
	//   	} 
	//   	else{
	//   		$('#calculate_fine').removeAttr("disabled");
	//   	}
	//   });
	//Calculate fine



	//Submit return
	$("#return_submit").click(function () {
		bookid = $("#return_books_detail").find("#InputBookId").val();
		bookCondition = $('#condition_checkbox').find('input[type=radio]:checked').val();//1 broken; 2 lost; 0 good
		if (bookid == "") {
			alert("Book ID cannot be empty!");
		}
		else {
			var fine = getFine(bookid, bookCondition);
			if (fine.length != 0) {
				console.log(fine);
				var overdue = parseFloat(fine[0]);
				var damage = parseFloat(fine[1]);
				var lost = parseFloat(fine[2]);
				console.log(overdue);
				console.log(damage);
				console.log(lost);
				var total = overdue+damage+lost;
				total = parseFloat(total).toFixed(2);
				console.log(total);
				if (total == 0) {
					returnBook(bookid);
				}
				else {
					$("#myModal").modal("show");
					$("#overdue_fine").text(overdue.toFixed(2));
					$("#damage_fine").text(damage.toFixed(2));
					$("#lost_fine").text(lost.toFixed(2));
					$("#total_fine").text(total);
					$("#go_on").click(function () {
						returnBook(bookid);
						if (bookCondition != 0)
							deleteBook(bookid);
					});
				}
			}
		}
		$("#return_books_detail").find("#InputBookId").val("").focus();
	});


	//Renew Books
	$("#renew_submit").click(function () {
		var bookid = $("#renew_books_detail").find("#InputBookId").val();
		if (bookid == "" || userid == "") {
			alert("Book ID cannot be empty!");
		}
		else {
			$.ajax({
				type: "POST",
				url: "http://47.95.205.76/api/renew",
				data: { "bookID": bookid },
				dataType: "json",
				async: false,
				cache: false,
				success: function (data) {
					if (data.result == "yes") {
						alert("Renew Succeeded!");
						$("#renew_books_detail").find("#InputBookId").val("").focus();
					}
					else
						alert("Renew Failed!\n" + data.reason);
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Renew Books\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
				},
			});
		}

	});

	//Add Books
	//Global Variants in Add Books
	var if_exist = false;
	var page;
	var isbn = "";
	var quantity = "";
	var location = "";
	var book_title = "";

	//Show book info from Douban API
	$('#add_books_detail').find('#InputISBN').bind('input propertychange', function () {
		if ($(this).val().length == 13) {
			isbn = $(this).val();
			$("#add_submit").removeAttr("disabled");
			page = $('#add_books_detail');
			book_title = fillBoxes(page, isbn);
		}
		else {
			$("#book_detail").css("display", "none");
			$("#barcode").css("display", "none");
			$("#add_submit").attr("disabled", "true");
		}
	});

	//Submit Add Book
	$("#add_submit").click(function () {
		quantity = $('#add_books_detail').find("#select_quantity").val();
		location = $('#add_books_detail').find("#select_library").val() + $('#add_books_detail').find("#select_room").val() + "-" + $('#add_books_detail').find("#select_shelf").val();
		$.ajax({
			type: "POST",
			url: "http://47.95.205.76/api/add_book",
			data: { "ISBN": isbn, "quantity": quantity, "location": location },
			dataType: "json",
			async: false,
			cache: false,
			success: function (data) {
				if (data.result == "yes") {
					$("#add_book_title").html(book_title);
					$("#barcode").css("display", "block");
					fillBarcode(data.bookID_range);
					$("#add_books_detail").find("input").val("");
					$("#add_books_detail").find("input").focus();
				}
				else{
					$("#barcode").css("display", "none");
					alert(data.reason);
					$("#add_books_detail").find("input").val("").focus();
				}
			},
			error: function (XMLHttpRequest, textStatus, errorThrown) {
				$("#barcode").css("display", "none");
				alert("Submit Add Books\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
				$("#add_books_detail").find("input").val("").focus();
			},
		});
	});

	//Edit Books
	$("#edit_books_submit").click(function () {
		location = $('#edit_books_detail').find("#select_library").val() + $('#edit_books_detail').find("#select_room").val() + "-" + $('#edit_books_detail').find("#select_shelf").val();
		var bookid = $('#edit_books_detail').find("#InputBookId").val();
		if (bookid == "") {
			alert("Book ID cannot be empty!");
		}
		else {
			$.ajax({
				type: "POST",
				url: "http://47.95.205.76/api/edit_book",
				data: { "bookID": bookid, "location": location },
				dataType: "json",
				async: false,
				cache: false,
				success: function (data) {
					if (data.result == "yes") {
						alert("Edit Succeeded!");
						$("#edit_books_detail").find("input").focus();
					}
					else
						alert(data.reason);
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Edit Books\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
				},
			});
		}

	})


	//View Delete Books
	$("#delete_books_detail").find(".check").click(function () {
		page = $("#delete_books_detail");
		isbn = page.find("#InputISBN").val();
		console.log(isbn);
		if (isbn == "") {
			alert("ISBN cannot be empty!");
		}
		else {
			$.ajax({
				type: "GET",
				url: "https://api.douban.com/v2/book/isbn/" + isbn,
				data: {},
				dataType: "jsonp",
				async: false,
				cache: false,
				success: function (data) {
					page.find("img").attr('src', data.image);
					page.find(".title").html(data.title);
					var otherinfo = data.author + '/' +
						data.publisher + '/' +
						data.pubdate;
					page.find("#other_info").html(otherinfo);
					displayBooks(page.find("#booklist"), isbn);
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Book is not found!");
					// alert("View/Delete\nstatus: "+XMLHttpRequest.status+"; readyState: "+XMLHttpRequest.readyState+"; textStatus: "+textStatus);
				},
			});
		}
	});

	//View Reader Records
	$("#reader_records_detail").find("button").click(function(){
		var reader_id = $("#reader_records_detail").find("#reader_id").val();
		if(reader_id.length < 11){
			alert("Please insert a valid Reader ID (11 numbers)");
			$("#reader_records_detail").find("#reader_id").focus();
		}
		else{
			$.ajax({
				type: "GET",
				url: "http://47.95.205.76/api/reader_lend_list",
				data: {"certificateNo":reader_id},
				dataType: "json",
				async: false,
				cache: false,
				success: function (data) {
					if(data.total!=0){
						$("#reader_records_detail").find("#records").css("display","block");
						for(var i=0;i<data.total;i++){
							$("#reader_records_detail").find("#row_"+i).css("display","table-row");
							$("#reader_records_detail").find("#book_id_"+i).text(data.result[i].bookID);
							$("#reader_records_detail").find("#book_isbn_"+i).text(data.result[i].ISBN);
							$("#reader_records_detail").find("#book_borrowtime_"+i).text(data.result[i].borrowTime);
							$("#reader_records_detail").find("#book_duetime_"+i).text(data.result[i].dueTime);
						}
						for(i;i<=1;i++){
							$("#reader_records_detail").find("#row_"+i).css("display","none");
						}
					}
					else{
						$("#reader_records_detail").find("#records").css("display","none");
						alert("No borrow records!");
						$("#reader_records_detail").find("#reader_id").focus();
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Reader is not found!");
					$("#reader_records_detail").find("#reader_id").focus();
					// alert("View/Delete\nstatus: "+XMLHttpRequest.status+"; readyState: "+XMLHttpRequest.readyState+"; textStatus: "+textStatus);
				},
			});
		}
	});

	//register account
	$("#reader_register").click(function(){
		$.ajax({
			type: "GET",
			url: "http://47.95.205.76/api/fine_configuration",
			data: {},
			dataType: "json",
			async: false,
			cache: false,
			success: function (data) {
				console.log(data);
				$("#register_submit").find("#overdue").text(data.DueFine);
				$("#register_submit").find("#damage").text(data.DamageFine);
				$("#register_submit").find("#lost").text(data.LostFine);
				$("#register_submit").find("#deposit").text(data.deposit);
			},
			error: function (XMLHttpRequest, textStatus, errorThrown) {
				alert("Charging Rules cannot be Retrieved!\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
			},
		});
	});
	$("#register_submit").submit(function () {
		var reader_id = $("#reader_register_detail").find("#reader_id").val();
		var name = $("#reader_register_detail").find("#name").val();
		var psw = $("#reader_register_detail").find("#psw").val();
		$.ajax({
			type: "POST",
			url: "http://47.95.205.76/api/signup",
			data: { "certificateNo": reader_id, "name": name, "password": psw },
			dataType: "json",
			async: false,
			cache: false,
			success: function (data) {
				console.log(data);
				if (data.result == "yes") {
					alert("Register Succeeded!");
				}
				else {
					alert(data.reason);
				}
			},
			error: function (XMLHttpRequest, textStatus, errorThrown) {
				alert("Register\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
			},
		});
		$("#reader_register_detail").find("#reader_id").val("").focus();
		return false;
	});

	//remove account
	var reader_id = "";
	var if_exist = false;
	$('#remove_account_detail').find('#reader_id').bind('input propertychange', function () {
		if ($(this).val().length == 11) {
			reader_id = $(this).val();
			$.ajax({
				type: "GET",
				url: "http://47.95.205.76/api/get_name_by_certificateNo",
				data: { "certificateNo": reader_id },
				dataType: "json",
				async: false,
				cache: false,
				success: function (data) {
					if (data.name != "") {
						$("#reader_name").text(data.name);
						$("#return_deposit").text(data.deposit);
						$("#remove_notice").css("display", "block");
						if_exist = true;
					}
					else {
						$("#remove_notice").css("display", "none");
						alert("Reader ID does not exist!");
						$('#remove_account_detail').find('#reader_id').val("").focus();
						if_exist = true;
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Remove Account\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
				},
			});
		}
		else {
			$("#remove_notice").css("display", "none");
		}
	});

	$("#remove_account_submit").submit(function () {
		if (if_exist == false) {
			alert("Reader ID does not exist!");
			$('#remove_account_detail').find('#reader_id').val("").focus();
		}
		else {
			$.ajax({
				type: "POST",
				url: "http://47.95.205.76/api/return_deposit",
				data: { "certificateNo": reader_id },
				dataType: "json",
				async: false,
				cache: false,
				success: function (data) {
					console.log(data);
					if (data.result == "yes") {
						alert("Remove Account Succeeded!");
						if_exist = false;
						$('#remove_account_detail').find('#reader_id').val("").focus();
					}
					else {
						alert("Remove Account Failed!\n" + data.reason);
						$("#remove_notice").css("display", "none");
						if_exist = false;
						$('#remove_account_detail').find('#reader_id').val("").focus();
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					alert("Remove Account\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
					$("#remove_notice").css("display", "none");
				},
			});
		}
		return false;
	});

	$("#penalty_rules_submit").submit(function(){
		var overdue_fine = $("#penalty_rules_detail").find("#overdue").val();
		var damage_fine = $("#penalty_rules_detail").find("#damage").val();
		var lost_fine = $("#penalty_rules_detail").find("#lost").val();
		var deposit = $("#penalty_rules_detail").find("#deposit").val();
		console.log(overdue_fine+"/"+damage_fine+"/"+lost_fine+"/"+deposit);
		$.ajax({
			type: "POST",
			url: "http://47.95.205.76/api/edit_configuration",
			data: { "DueFine": overdue_fine,"DamageFine":damage_fine,"LostFine":lost_fine,"deposit":deposit },
			dataType: "json",
			async: false,
			cache: false,
			success: function (data) {
				console.log(data);
				if (data.result == "yes") {
					alert("Edit Penalty Rules Succeeded!");
					$("#penalty_rules_detail").find("#overdue").val("").focus();
					$("#penalty_rules_detail").find("#damage").val("");
					$("#penalty_rules_detail").find("#lost").val("");
					$("#penalty_rules_detail").find("#deposit").val("");	
				}
				else {
					alert("Edit Penalty Rules Failed!\n" + data.reason);
				}
			},
			error: function (XMLHttpRequest, textStatus, errorThrown) {
				alert("Edit Penalty Rules Failed!\nstatus: " + XMLHttpRequest.status + "; readyState: " + XMLHttpRequest.readyState + "; textStatus: " + textStatus);
			},
		});
		return false;
	});
});