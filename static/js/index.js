var userid = getCookie("userid");
var password = getCookie("password");


function logged() {
    $("#user").css("display", "block");
    $("#signout").css("display", "block");
    $("#user-id").text(userid);
    $("#signin").css("display", "none");
}
function notlogged() {
    $("#signin").css("display", "block");
    $("#user").css("display", "none");
    $("#signout").css("display", "none");
    $("#user-id").text("");
}

// Check Login
$(document).ready(function () {
    console.log(userid + '/' + password);
    if (userid == "")
        notlogged();
    else {
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
                    logged();
                }
                else {
                    console.log("authorization: no");
                    notlogged();
                }
            }
        });
    }
});

//logout
$(document).ready(function () {
    $("#signout").find("a").click(function () {
        removeCookie("userid");
        removeCookie("password");
        window.location.reload();
    });

    $.get("api/fine_configuration", {}, function (data) {
        cont = "<p>Overdue Fine: <b>" + data.DueFine + "￥</b> /book/day<br/>";
        cont += "Damage Fine: <b>" + data.DamageFine + "￥+book-price</b><br/>";
        cont += "Lost Fine: <b>" + data.LostFine + "￥+book-price</b><br/>";
        cont += "Deposit: <b>" + data.deposit + "￥</b> /person</p>";
        var pop = { "data-toggle": "popover", "data-trigger": "hover", "title": "Charging Rules", "data-content": cont, "data-html": true };
        $("#bell-icon").attr(pop).popover();
    }, "json");
})

//search submit
$(document).ready(function () {
    $("#search-btn").click(function () {
        $("form").submit();
    });
});