$('.form-group').removeClass('row');

/* Notifications JS basic client */
$(function () {
    let emptyMessage = '没有未读通知';

    function checkNotifications() {
        $.ajax({
            url: '/notifications/latest-notifications/',
            cache: false,
            success: function (data) {
                if (!data.includes(emptyMessage)) {
                    $("#notifications").addClass("btn-danger");
                }
            },
        });
    }

    function update_social_activity(id_value) {
        let newsToUpdate = $("[news-id=" + id_value + "]");
        payload = {
            'id_value': id_value,
        };
        $.ajax({
            url: '/news/update-interactions/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".comment-count", newsToUpdate).text(data.comments);
            },
        });
    }

    checkNotifications();

    $('#notifications').popover({
        html: true,
        trigger: 'manual',
        container: "body",
        placement: "bottom",
    });

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
            checkNotifications();
        } else {
            $("#notifications").popover('dispose');
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                success: function (data) {
                    $("#notifications").popover({
                        html: true,
                        trigger: 'focus',
                        container: "body",
                        placement: "bottom",
                        content: data,
                    });
                    $("#notifications").popover('show');
                    $("#notifications").removeClass("btn-danger")
                },
            });
        }
        return false;
    });

    // 选择WebSocket连接协议 ws:// and wss://
    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    let ws_path = ws_scheme + '://' + window.location.host + "/ws/notifications/";
    let webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // WebSocket调试帮助
    webSocket.socket.onopen = function () {
        console.log("Connected to " + ws_path);
    };

    webSocket.socket.onclose = function () {
        console.error("Disconnected from " + ws_path);
    };

    // 监听django-channels创建的Websocket连接
    webSocket.listen(function (event) {

        switch (event.key) {
            case "notification":
                if (event.actor_name !== currentUser) {  // 消息提示的发起者不提示
                    $("#notifications").addClass("btn-danger");
                }
                break;

            case "social_update":
                if (event.actor_name !== currentUser) {
                    $("#notifications").addClass("btn-danger");
                }
                update_social_activity(event.id_value);
                break;

            case "additional_news":
                if (event.actor_name !== currentUser) {
                    $(".stream-update").show();
                }
                break;

            default:
                console.log('error: ', event);
                break;
        }
    });
});
