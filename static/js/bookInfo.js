$(document).ready(function () {

    function overshowblock(id) {
        if (document.getElementById(id).innerHTML != undefined) {
            document.getElementById(id).style.display = "block";
        }
    }
    function overshow(item, parent, str) {
        if (str != undefined) {
            document.getElementById(item).innerHTML = str;
            document.getElementById(parent).style.display = "block";
        }
    }

    function padding(itemId, content) {
        if (content != undefined) {
            document.getElementById(itemId).innerHTML = content;
        }
    }
    var searchText, page, type, mData;
    searchText = window.location.href.split('=')[1];
    searchType = '3';
    $.ajax({
        type: "GET",
        url: "http://47.95.205.76/api/search",
        data: { "search": searchText, "type": searchType },
        dataType: "json",
        async: false,
        cache: false,

        success: function (data) {
            mData = data;
            console.log(data);
            // overshow("original_title_td", "original_title_tr", data.result[0].origintitle);
            overshow("author_td", "author_tr", data.result[0].author);
            // overshow("translator_td", "translator_tr", data.result[0].translator);
            overshow("publish_td", "publish_tr", data.result[0].press);
            overshow("pubdate_td", "pubdate_tr", data.result[0].pubdate);
            overshow("price_td", "price_tr", data.result[0].price);
            // overshow("page_td", "page_tr", data.result[0].pages);
            overshow("ISBN_td", "ISBN_tr", data.result[0].ISBN);

            document.getElementById("title").innerHTML = data.result[0].title;
            document.getElementById("picture").src = data.result[0].cover;
            padding("context_introduction", data.result[0].summary);
            padding("author_introduction", data.result[0].authorinfo);
            padding("catalogue_information", data.result[0].catalog);
            // padding("label_text",data.result[0].tag)
            overshowblock("title");

        },
        error: function (json) {
            alert("fault");
        }
    });
    var isbn = getUrlParam("search");
    $.ajax({
        type: "GET",
        url: "http://47.95.205.76/api/book_location",
        data: { "ISBN": isbn },
        dataType: "json",
        async: false,
        cache: false,
        success: function (data) {
            if (data.result != "no") {
                var num = data.len;
                var result = data.result;
                for (x in result) {
                    var html = "<tr><td class='black-item'>" + x + "</td>";
                    html += "<td class='black-item'>" + result[x] + "</td></tr>";
                    $("#libInfo").append(html);
                }
            }else{
                $("#libInfo").parents(".pad").children("table:eq(0)").css({"display":"none"});
                var html="<p style='width:100%;text-align:center;color:#333;line-height:25px;' class='black-item'>"+data.reason+"</p>";
                $("#libInfo").parents(".pad").append(html);
            }
            console.log(data);
        }
    })
});

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

    //Sign Out
    $("#signout").click(function () {
        removeCookie("password");
        location.reload();
        return 0;
    });
});

function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]); return null;
}