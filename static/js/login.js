$(document).ready(function () {
    var pop1 = { "data-toggle": "popover", "data-trigger": "manual", "data-content": "Use 11 numbers."};
    var pop2 = { "data-toggle": "popover", "data-trigger": "manual", "data-content": "Use 6-16 numbers or letters." };
    var idInput = $("input:eq(0)");
    var pwInput = $("input:eq(1)");
    idInput.attr(pop1);
    pwInput.attr(pop2);

    $("form").submit(function () {
        var userid = idInput.val();
        var password = pwInput.val();
        var pattern1 = /^\d{11}$/;
        var pattern2 = /^[a-zA-Z0-9]{6,16}$/;
        if (!pattern1.test(userid)) {
            idInput.popover("show");
            idInput.val("");
        } else if (!pattern2.test(password)) {
            pwInput.popover("show");
            pwInput.val("");
        } else {
            $.ajax({
                type: "POST",
                url: "http://47.95.205.76/api/reader_login",
                data: { "certificateNo": userid, "password": password },
                dataType: "json",
                async: false,
                cache: false,
                success: function (data) {
                    console.log(data);
                    if (data.result == "yes") {
                        setCookie("userid", userid, 7);
                        setCookie("password", password, 7);
                        $(location).attr('href', "userIndex");
                    }
                    else if (data.result == "no") {
                        $("#mySdialog div.sdialog-content").text(data.reason);
                        $("#mySdialog").dialog("show");
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    $("#mySdialog div.sdialog-content").text("Sever error!");
                    $("#mySdialog").dialog("show");
                }
            });
            $("#mySdialog").on("dialog.hiden", function () {
                location.reload();
            })
        }
        $("body").one("mousedown",function () {
            idInput.popover("hide");
            pwInput.popover("hide");
        })
        return false;
    });
});




