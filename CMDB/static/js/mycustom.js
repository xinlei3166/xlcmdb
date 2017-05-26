/**
 * Created by junxi on 2017/5/22.
 */

/*删除主机函数*/
function delServer(id) {
    $.ajax(
        {
            type: "post",
            cache: false,
            url: "http://127.0.0.1:8080/web/remove/server/",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                "id": id,
            },
            success: function (data) {
                if (data["status"] == "success") {
                    window.location.reload();
                }
            },
            error: function (err) {
                console.log(err);
            }
        }
    )
}

/*删除用户函数*/
function delUser(id) {
    $.ajax(
        {
            type: "post",
            cache: false,
            url: "http://127.0.0.1:8080/web/delete/user/",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                "id": id,
            },
            success: function (data) {
                if (data["status"] == "success") {
                    // console.log(data['status'])
                    window.location.reload();
                }
            },
            error: function (err) {
                console.log(err);
            }
        }
    )
}

/*删除用户组函数*/
function delGroup(id) {
    $.ajax(
        {
            type: "post",
            cache: false,
            url: "http://127.0.0.1:8080/web/delete/group/",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                "id": id,
            },
            success: function (data) {
                if (data["status"] == "success") {
                    // console.log(data['status'])
                    window.location.reload();
                }
            },
            error: function (err) {
                console.log(err);
            }
        }
    )
}

/*saltapi函数*/
function saltStatus(action) {
    console.log(action);
    $.ajax(
        {
            type: "post",
            cache: false,
            url: "http://127.0.0.1:8080/web/server/saltapi/",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                "action": action
            },
            success: function (data) {
                if (data["status"] == "success") {
                    console.log(data);
                    // window.location.reload();
                }
            },
            error: function (err) {
                console.log(err);
            }
        }
    )
}


/*saltapi函数*/
function saltAction(hostname, action) {
    $.ajax(
        {
            type: "post",
            cache: false,
            url: "http://127.0.0.1:8080/web/server/saltapi/",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                "hostname": hostname,
                "action": action
            },
            success: function (data) {
                if (data["status"] == "success") {
                    console.log(data);
                    window.location.reload();
                }
            },
            error: function (err) {
                console.log(err);
            }
        }
    )
}

/*执行命令函数*/
function commandAction(hostname, command, action) {
    $.ajax(
        {
            type: "post",
            cache: false,
            url: "http://127.0.0.1:8080/web/server/saltapi/",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                "hostname": hostname,
                "command": command,
                "action": action
            },
            success: function (data) {
                if (data["status"] == "success") {
                    console.log(data["status"]);
                    // console.log(typeof data['result']);
                    var commandShowBox = $(".command-result-show")[0];
                    // commandShowBox.innerHTML = '';   // 清空上次请求的内容
                    var commandResult = data['result'];
                    for (key in commandResult){
                        // console.log(key);
                        hostname = key;
                        commandShowBox.innerHTML += '主机：' + hostname + '\n\n' + commandResult[hostname] + '\n\n';
                    }
                    // commandShowBox.innerHTML = '主机：' + hostname + '\n\n' + data['result'][hostname];
                    // window.location.reload();
                }
            },
            error: function (err) {
                console.log(err);
            }
        }
    )
}




