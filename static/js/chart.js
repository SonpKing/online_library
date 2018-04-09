var userid = getCookie("userid");
var password = getCookie("password");


function selectOnchang(obj) {

    if (obj.selectedIndex == 2) {
        $('.form_date').datetimepicker('remove');
        $('.form_date').datetimepicker({
            format: 'yyyy',
            weekStart: 1,
            autoclose: true,
            startView: 4,
            minView: 4,
            forceParse: false,
            todayBtn: true,
            language: 'zh-CN'
        });

        var date = new Date();
        date = date.getFullYear();
        chartDatetimepicker.value = date;
        $('.form_date').datetimepicker('setStartDate', "2014-09-01");
        $('.form_date').datetimepicker('setEndDate', new Date);
    }

    else if (obj.selectedIndex == 1) {
        $('.form_date').datetimepicker('remove');
        $('.form_date').datetimepicker({
            format: 'yyyy-mm',
            weekStart: 1,
            autoclose: true,
            startView: 3,
            minView: 3,
            forceParse: false,
            todayBtn: true,
            language: 'zh-CN'
        });

        var date = new Date();
        date = date.getFullYear() + '-' + (date.getMonth() + 1);
        chartDatetimepicker.value = date;
        $('.form_date').datetimepicker('setStartDate', "2014-09");
        $('.form_date').datetimepicker('setEndDate', new Date);
    }

    else if (obj.selectedIndex == 0) {
        $('.form_date').datetimepicker('remove');
        $('.form_date').datetimepicker({
            format: 'yyyy-mm-dd',
            weekStart: 1,
            autoclose: true,
            startView: 2,
            minView: 2,
            forceParse: false,
            todayBtn: true,
            language: 'zh-CN'
        });

        var date = new Date();
        date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
        chartDatetimepicker.value = date;
        $('.form_date').datetimepicker('setStartDate', "2014");
        $('.form_date').datetimepicker('setEndDate', new Date);
    }
}

function mGetDate(year, month) {
    var d = new Date(year, month, 0);
    return d.getDate();
}

function getData(obj) {
    var type = ShowType.selectedIndex;
    var date = chartDatetimepicker.value;

    type = 2 - type;
    if (type == 0)
        date += "-01-01";
    else if (type == 1)
        date += "-01";

    $.get("api/cuz_we_love_money", { "date_type": type, "dateInfo": date }, function (Data, status) {

        $('#pie').remove(); // this is my <canvas> element
        $('#pieChart').append('<canvas id="pie"></canvas>');

        $('#liner').remove(); // this is my <canvas> element
        $('#linerChart').append('<canvas id="liner"></canvas>');

        chartTable.style.display = "none";

        var due = Data.dic_sum2[0];
        var damage = Data.dic_sum2[1];
        var lost = Data.dic_sum2[2];
        var deposit = Data.dic_sum2[3];
        var refund = Data.dic_sum2[4];
        var total = due + damage + lost + deposit - refund;

        due = due.toFixed(2);
        damage = damage.toFixed(2);
        lost = lost.toFixed(2);
        deposit = deposit.toFixed(2);
        refund = -refund;
        refund = refund.toFixed(2);
        total = total.toFixed(2);

        document.getElementById("tableDue").innerHTML = due;
        document.getElementById("tableDamage").innerHTML = damage;
        document.getElementById("tableLost").innerHTML = lost;
        document.getElementById("tableDeposit").innerHTML = deposit;
        document.getElementById("tableReturnDeposit").innerHTML = refund;
        document.getElementById("tableTotal").innerHTML = total;

        if (total <= 0) {
            if (type == 0)
                alert("No Income During This Year");
            else if (type == 1)
                alert("No Income During This Month");
            else if (type == 2)
                alert("No Income On This Day");
        }
        if(refund == 0 && total <= 0)
        {
            pieChart.style.display = "none";
        }
        else {
            pieChart.style.display = "";
            var ctx1 = document.getElementById("pie").getContext('2d');


            var value = {
                datasets: [{
                    data: [due, damage, lost, deposit],
                    backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#6aa84f']
                }],

                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: [
                    'Due',
                    'Damege',
                    'Lost',
                    'Deposit'
                ]
            };
            var myPieChart = new Chart(ctx1, {
                type: 'pie',
                data: value,
                options: {
                    title: {
                        display: true,
                        text: 'Proportion'
                    },

                }
            });

        }

        chartTable.style.display = "";


        var today = new Date();
        var todayMonth = today.getMonth() + 1;
        var todayYear = today.getFullYear();
        today = today.getDate();

        var inputTime = date.split('-');

        var monthEnd;
        var dayEnd;

        if (todayYear == inputTime[0]) {
            monthEnd = todayMonth;
        }
        else monthEnd = 12;

        if (todayMonth == inputTime[1]) {
            dayEnd = today;
        }
        else dayEnd = mGetDate(inputTime[0], inputTime[1]);

        var dueArray = new Array();
        var damageArray = new Array();
        var lostArray = new Array();
        var depositArray = new Array();
        var refund = new Array();
        var totalArray = new Array();

        var lineLabels = new Array();
        var month = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];

        if (type == 0) {
            for (var i = 0; i < monthEnd; ++i) {
                lineLabels[i] = month[i];
                dueArray[i] = Data.dic_sum0[0][i + 1];
                damageArray[i] = Data.dic_sum0[1][i + 1];
                lostArray[i] = Data.dic_sum[2][i + 1];
                depositArray[i] = Data.dic_sum0[3][i + 1];
                refund[i] = Data.dic_sum0[4][i];
                totalArray[i] = Data.dic_sum[i + 1];
            }

        }
        else if (type == 1) {
            for (var i = 0; i < dayEnd; ++i) {
                var timeCor;
                timeCor = inputTime[0] + '-' + inputTime[1] + '-' + (i + 1);
                lineLabels[i] = timeCor;
                dueArray[i] = Data.dic_sum0[0][i + 1];
                damageArray[i] = Data.dic_sum0[1][i + 1];
                lostArray[i] = Data.dic_sum[2][i + 1];
                depositArray[i] = Data.dic_sum0[3][i + 1];
                refund[i] = Data.dic_sum0[4][i];
                totalArray[i] = Data.dic_sum[i + 1];
            }

        }

        if (type != 2) {
            var value = {
                labels: lineLabels,
                datasets: [{
                    label: "Due",
                    backgroundColor: '#ff6384',
                    borderColor: '#ff6384',
                    data: dueArray,
                    fill: false,
                }, {
                    label: "Damage",
                    fill: false,
                    backgroundColor: '#36a2eb',
                    borderColor: '#36a2eb',
                    data: damageArray,
                },
                {
                    label: "Lost",
                    fill: false,
                    backgroundColor: '#ffce56',
                    borderColor: '#ffce56',
                    data: lostArray,
                },
                {
                    label: "Deposit",
                    fill: false,
                    backgroundColor: '#6aa84f',
                    borderColor: '#6aa84f',
                    data: depositArray,
                },
                {
                    label: "Refund",
                    fill: false,
                    backgroundColor: '#cc65fe',
                    borderColor: '#cc65fe',
                    data: refund,
                },
                {
                    label: "Total",
                    fill: false,
                    backgroundColor: '#708090',
                    borderColor: '#708090',
                    data: totalArray,
                }]

            };

            linerChart.style.display = "";

            var ctx = document.getElementById("liner").getContext('2d');
            var myLineChart = new Chart(ctx, {
                type: 'line',
                data: value,
                options: {
                    title: {
                        display: true,
                        text: 'Trend'
                    },
                    legend:
                        {
                            position: 'bottom',
                        }
                }
            });
        }

    });

}

$(document).ready(function () {

    if (userid == "") {
        alert("Please login first");
        window.location.href = "login";
    }
    else {
        $.post("api/admin_login", { "ID": userid, "password": password }, function (data) {
            if (data.result == "no") {
                alert("You are not a librarian");
                window.location.href = "/";
            }

            else {
                $('#usertype').selectpicker({
                    'selectedText': 'cat'
                });

                $('.form_date').datetimepicker({
                    format: 'yyyy-mm-dd',
                    weekStart: 1,
                    autoclose: true,
                    startView: 2,
                    minView: 2,
                    forceParse: false,
                    todayBtn: true,
                    language: 'zh-CN'
                });

                var date = new Date();
                date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
                chartDatetimepicker.value = date;
                $('.form_date').datetimepicker('setStartDate', "2014-09-01");
                $('.form_date').datetimepicker('setEndDate', new Date());

                linerChart.style.display = "none";
            }
        }, "json");

    }


});