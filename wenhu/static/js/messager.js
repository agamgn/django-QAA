$(function () {

    // 滚动条下拉到底
    function scrollConversationScreen() {
        $("input[name='message']").focus();
        $('.messages-list').scrollTop($('.messages-list')[0].scrollHeight);
    }

    // 添加消息函数
    function addNewMessage(message_id) {
        $.ajax({
            url: '/messages/receive-message/',
            data: {'message_id': message_id},
            cache: false,
            success: function (data) {
                $(".send-message").before(data); // 将接收到的消息插入到聊天框
                scrollConversationScreen(); // 滚动条下拉到底
            }
        });
    }

    // AJAX POST发送消息
    $("#send").submit(function () {
        $.ajax({
            url: '/messages/send-message/',
            data: $("#send").serialize(),
            cache: false,
            type: 'POST',
            success: function (data) {
                $(".send-message").before(data);  // 将接收到的消息插入到聊天框
                $("input[name='message']").val(''); // 消息发送框置为空
                scrollConversationScreen();  // 滚动条下拉到底
            }
        });
        return false;
    });

    // WebSocket连接
    var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";  // 使用wss(https)或者ws(http)
    var ws_path = ws_scheme + '://' + window.location.host + "/ws/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    window.onbeforeunload = function () {
        // Small function to run instruction just before closing the session.
        var payload = {
            "type": "recieve",
            "sender": currentUser,
            "set_status": "offline"
        };
        webSocket.send(payload);
    };

    // 监听后端发送过来的消息
    webSocket.listen(function (event) {
        switch (event.key) {
            case "message":
                if (event.sender === activeUser) {
                    addNewMessage(event.message_id);
                } else {
                    $("#new-message-" + event.sender).show();
                }
                break;

            case "set_status":
                setUserOnlineOffline(event.sender, event.status);
                break;

            default:
                console.log('error: ', event);
                break;
        }
    });
});
