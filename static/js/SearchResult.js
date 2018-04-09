var text;
var type;
var page;
var totalpages;

function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]); return null;
}

function adjustPageNav() {
    console.log("adjustPageNav entered");
    if (page == 1)
        $(".prepage").parent("li").addClass("disabled");
    else if (page == totalpages)
        $(".nextpage").parent("li").addClass("disabled");
    else {
        $(".prepage").parent("li").removeClass("disabled");
        $(".prepage").parent("li").removeClass("disabled");
    }

    console.log("adjustPageNav 1");
    $(".active").removeClass("active");
    if (totalpages < 5) {
        console.log("adjustPageNav 2");
        for (i = totalpages + 1; i <= 5; i++) {
            $(".page" + i.toString()).parent("li").css("display", "none");
        }
        for (i = 1; i <= totalpages; i++) {
            $(".page" + i.toString()).html(i);
        }
        $(".page" + page.toString()).parent("li").addClass("active");
    }
    else {
        if ((page + 2 <= totalpages) && (page - 2 >= 1)) {
            console.log("adjustPageNav 3");
            $(".page1").html(page - 2);
            $(".page2").html(page - 1);
            $(".page3").html(page);
            $(".page4").html(page + 1);
            $(".page5").html(page + 2);
            $(".page3").parent("li").addClass("active");
        }
        else {
            if (page + 2 > totalpages) {
                console.log("adjustPageNav 4");
                $(".page1").html(totalpages - 4);
                $(".page2").html(totalpages - 3);
                $(".page3").html(totalpages - 2);
                $(".page4").html(totalpages - 1);
                $(".page5").html(totalpages);
                var t = 5 - (totalpages - page);
                $("#page" + t.toString()).parent("li").addClass("active");
            }
            else if (page - 2 < 1) {
                console.log("adjustPageNav 5");
                $(".page1").html(1);
                $(".page2").html(2);
                $(".page3").html(3);
                $(".page4").html(4);
                $(".page5").html(5);
                $(".page" + page.toString()).parent("li").addClass("active");
            }
        }
    }
}

function displayBooklist(data) {
    console.log("total records: " + data.total);
    console.log("point 2 ok");
    totalpages = Math.max(Math.ceil(parseInt(data.total) / 15), 1);
    console.log("totalpages: " + totalpages + text);
    $("#searchfor").html(text);
    $("#total").html(data.total);
    console.log("point 2 ok, entering adjustPageNav " + $("#searchfor"));
    adjustPageNav();

    if (data.total == 0)
        $("#noresult").css("display", "block");
    else
        $("#noresult").css("display", "none");
    for (var i = 0; i < data.result.length; i++) {
        var tr = $("tr:eq(" + i + ")");
        tr.css("display", "block");
        tr.find("img").attr("src", data.result[i].cover);
        tr.find(".title").text(data.result[i].title);
        tr.find(".remaining").text(data.result[i].remain);
        var detail = data.result[i].author + ' / ' + data.result[i].press + ' / ' +
            data.result[i].pubdate + ' / ' + data.result[i].price;
        tr.find(".detail").text(detail);
        tr.find(".isbn").text(data.result[i].ISBN);
    }
    while (i <= 14) {
        var tr = $("tr:eq(" + i + ")");
        tr.css("display", "none");
        i++;
    }
}

$(document).ready(function () {
    var userid = getCookie("userid");
    var password = getCookie("password");
    console.log(userid + '/' + password);
    $.ajax({
        type: "POST",
        url: "http://47.95.205.76/api/reader_login",
        data: { "certificateNo": userid, "password": password },
        dataType: "json",
        async: false,
        cache: false,
        success: function (data) {
            console.log(data.admin);
            if (data.result == "yes") {
                console.log("login result: yes");
                $("#user").css("display", "block");
                $("#username").text(userid);
                $("#signin").css("display", "none");
            }
            else {
                console.log("authorization: no");
                $("#signin").css("display", "block");
                $("#user").css("display", "none");
            }
        }
    });
});

//Load Booklist from previous Search HomePage
$(document).ready(function () {
    text = getUrlParam("search");
    type = getUrlParam("type");
    page = getUrlParam("page");
    if (page == null) page = 1;
    page = parseInt(page);

    console.log("text: " + text + '/' + "type: " + type + '/' + "page: " + page);
    $.ajax({
        type: "GET",
        url: "http://47.95.205.76/api/search",
        data: { "search": text, "type": type, "page": page },
        dataType: "json",
        async: false,
        cache: false,
        success: function (data) {
            console.log("point 1 ok");
            displayBooklist(data);
        }
    });
});

$(document).ready(function () {
    //Sign Out
    $("#signout").click(function () {
        removeCookie("password");
        location.reload();
    });
    $(".nextpage").click(function () {
        if(page == totalpages);
        else{
             page = (parseInt(page) == parseInt(totalpages) )? parseInt(page) : (parseInt(page) + 1);
            $("#formpage").val(page);
            console.log("page: " + page);
            $("#formtype").val(type);
            $("#formsearch").val(text);
            $("#changepage").submit();
        }
    });
    $(".prepage").click(function () {
        if(parseInt(page) == 1);
        else{
            page = (parseInt(page) > 1) ? (parseInt(page) - 1) : 1;
            $("#formpage").val(page);
            console.log("page: " + page);
            $("#formtype").val(type);
            $("#formsearch").val(text);
            $("#changepage").submit();
        }    
    })
    $(".page").click(function () {
        page = parseInt($(this).text());
        $("#formpage").val(page);
        console.log("page: " + page);
        $("#formtype").val(type);
        $("#formsearch").val(text);
        $("#changepage").submit();
    })
});

//To Book detail page
$(document).ready(function () {
    $("table").find("img").click(function () {
        var isbn = $(this).parent(".image").siblings(".book_info").find(".isbn").text();
        console.log(isbn);
        var url = "bookinfo?search=" + isbn;
        window.open(url);
    });
    $("table").find(".title").click(function () {
        var isbn = $(this).parent("li").siblings().find(".isbn").text();
        console.log(isbn);
        var url = "bookinfo?search=" + isbn;
        window.open(url);
    });
})
