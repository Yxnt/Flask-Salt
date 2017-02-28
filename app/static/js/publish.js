/**
 * Created by yandou on 2017/2/28.
 */
$(function () {
    get_host();
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });

});


function get_host() {
    $("#host_refre").addClass("fa-spin");

    $.getJSON('/salt/minions', function (data) {
        var info = data['return'][0];
        var length = Object.keys(info).length;
        var html = "";
        for (var i = 0; i < length; i++) {
            var client_name = Object.keys(info)[i];
            html = html.concat("<option id=server-", i, ">", client_name, "</option>");
            $("#clients").html(html);
        }
        $("#host_refre").removeClass("fa-spin")
    })
}

function get_project_info() {
    // $("#submit").click(function () {

    $.ajax({
        url: "/salt/publish/git/get_branches",
        type: 'POST',
        contentType: 'application/json',
        async: true,
        data: JSON.stringify({
            project_name: project_name
        }),
        success: function (data) {
            ret = data['return'][0]['master'];
            ret_length = Object.keys(ret).length;
            var html = "";
            for (var i = 0; i < ret_length; i++) {
                var branches_name = ret[i];
                html = html.concat("<option id=branches-", i, ">", branches_name, "</option>");
                $("#branches").html(html);
            }
        }
    });
}


function get_cur_pro_version() {
    ajax('/salt/publish/git/get_master_cur_hex', function (data) {
        $('#cur_info').val(data['return']['0']['master']);
    })
}

function get_cur_pro_all_version() {
    ajax('/salt/publish/git/get_master_all_hex', function (data) {
            ret = data['return']['0']['master'];
            ret_length = Object.keys(ret).length;
            var html = "";
            for (var i = 0; i < ret_length; i++) {
                var hex = ret[i];
                html = html.concat("<option id=version-", i, ">", hex, "</option>");
                $("#all_hex").html(html);
            }
        })
}

function ajax(url, fun) {
    var project_name = $("#project_name").val();
    $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            async: true,
            data: JSON.stringify({
                project_name: project_name
            }),
            success: fun
        }
    )
}