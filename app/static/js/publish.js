/**
 * Created by yandou on 2017/2/28.
 */
$(function () {


    $("#publish_form").validate({
        rules: {
            project: {
                required: true
            }
        },
        messages: {
            project: {
                required: "缺少项目名称"
            }
        }
    });
    get_host();
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
    var project_name = $("#project_name").val();
    var cur_hex = $("#cur_info").val();
    var new_hex = $("#all_hex").val();
    var master = "master";
    var client = $("#clients").val();


    $("#submit").click(function () {
        var project_name = $("#project_name").val();
        var cur_hex = $("#cur_info").val();
        var new_hex = $("#all_hex").val();
        var client = $("#clients").val();
        var html = "";
        html = html.concat("项目：", project_name, '<br>',
            "当前版本号：", "<strong>", cur_hex, "</strong>", "<br>",
            "更新后版本号：", "<strong>", new_hex, "</strong>", "<br>",
            "选中节点：", "<strong>", client, "</strong>"
        );
        $("#operator").html(html);
    });


    $("#confirm").click(function () {
        var project_name = $("#project_name").val();
        var cur_hex = $("#cur_info").val();
        var new_hex = $("#all_hex").val();
        var master = "master";
        var client = $("#clients").val();
        var data = JSON.stringify([master, project_name, new_hex, client]);
        if (project_name === "" || cur_hex === "" || new_hex === null) {
            return alert('提交失败');
        } else {
            alert("正在执行，请稍后");
            ajax('/salt/publish/git/reset', 'POST', data, function (data) {
                var info = data['return'][0]['master'];
                $("#result").modal('show');
                $("#result_info").text(JSON.stringify(info)).css({
                    "overflow-y": "auto",
                    "word-break": "break-all"
                });
            })
        }
    });

    $("#all_close").click(function () {
        $('.modal').modal('hide');
    });

    $("#reset").click(function () {
        var project_name = $("#project_name").val();
        var cur_hex = $("#cur_info").val();
        var new_hex = $("#all_hex").val();
        var client = $("#clients").val();
        var html = "";
        html = html.concat("项目：", project_name, '<br>',
            "当前版本号：", "<strong>", cur_hex, "</strong>", "<br>",
            "回滚后版本号：", "<strong>", new_hex, "</strong>", "<br>",
            "选中节点：", "<strong>", client, "</strong>"
        );
        $("#operator").html(html);
    });

    $("#cur_hex_info").click(get_cur_pro_version);
    $("#history_refre").click(get_cur_pro_all_version);
    $("#host_refre").click(get_host);

});


//获取所有客户端节点
function get_host() {
    $("#host_refre").addClass("fa-spin");
    ajax('/salt/minions', "GET", undefined, function (data) {
        var info = data['return'][0];
        var length = Object.keys(info).length;
        var html = "";
        for (var i = 0; i < length; i++) {
            var client_name = Object.keys(info)[i];
            html = html.concat("<option id=server-", i, ">", client_name, "</option>");
            $("#clients").html(html);
        }
        $("#host_refre").removeClass("fa-spin")

    });
}
// 获取当前hexsha
function get_cur_pro_version() {
    $("#cur_hex_info").addClass("fa-spin");
    var project_name = $("#project_name").val();
    var data = JSON.stringify([project_name]);
    ajax('/salt/publish/git/get_master_cur_hex', type = "POST", data, function (data) {
        $('#cur_info').val(data['return']['0']['master']);
        $("#cur_hex_info").removeClass("fa-spin");
        get_cur_pro_all_version();
    });

}

//获取所有git hexsha
function get_cur_pro_all_version() {
    $("#history_refre").addClass("fa-spin");
    var project_name = $("#project_name").val();
    var data = JSON.stringify([project_name]);
    var cur_hex = $('#cur_info').val();


    ajax('/salt/publish/git/get_master_all_hex', "POST", data, function (data) {
        ret = data['return']['0']['master'];
        ret_length = Object.keys(ret).length;
        var html = "";
        for (var i = 0; i < ret_length; i++) {
            var hex = ret[i];
            if (hex === cur_hex) {
                html = html.concat("<option id=version-", i, " style='color:red'>", hex, "</option>");
                continue;
            }
            html = html.concat("<option id=version-", i, ">", hex, "</option>");
            $("#all_hex").html(html);
        }
        $("#history_refre").removeClass("fa-spin");
    });
}

function ajax(url, type, data, fun) {
    if (data !== undefined) {
        data = data;
    }
    $.ajax({
            url: url,
            type: type,
            contentType: 'application/json',
            async: true,
            data: data,
            success: fun
        }
    )
}