/**
 * Created by yandou on 2017/2/27.
 */

$(function () {
    saltapi_stats();
    saltapi_jobs();
    saltapi_minions();
});


setInterval("saltapi_stats()", "360000");
setInterval("saltapi_jobs()", "60000");
setInterval("saltapi_minions()", "100000");


function saltapi_stats() {
    $.getJSON('/salt/stats', function (json) {
        var idle = json["Threads Idle"];
        $("#idle").html(idle + "<small>%</small>")
    });
}
function saltapi_jobs() {
    $.getJSON('/salt/jobs', function (data) {
        var length = Object.keys(data["return"]['0']).length ;
        $("#jobs").text(length)
    })
}
function saltapi_minions() {
    $.getJSON('/salt/minions', function (json) {
        var minion = Object.keys(json['return']['0']).length;
        $("#client").text(minion)
    })
}