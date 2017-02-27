/**
 * Created by yandou on 2017/2/27.
 */

$(function () {
    saltapi_stats();
    saltapi_jobs();
    saltapi_minions();
});


setInterval("saltapi_stats()", "36000");
setInterval("saltapi_jobs()", "5000");
setInterval("saltapi_minions()", "10000");


function saltapi_stats() {
    $.getJSON('/salt/stats', function (json) {
        var idle = json["Threads Idle"];
        $("#idle").html(idle + "<small>%</small>")
    });
}
function saltapi_jobs() {
    $.getJSON('/salt/jobs', function (json) {
        var jobs = json["return"].length - 1;
        $("#jobs").text(jobs)
    })
}
function saltapi_minions() {
    $.getJSON('/salt/minions', function (json) {
        var minion = json["return"].length - 1;
        $("#client").text(minion)
    })
}