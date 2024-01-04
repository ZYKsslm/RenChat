# 确保回到标题前关闭连接
label before_main_menu:
    python:
        try:
            if server.has_communicated:
                server.close()
            if client.has_communicated:
                client.close()
        except:
            pass
    return

# 确保退出前关闭连接
label quit:
    python:
        try:
            if server.has_communicated:
                server.close()
            if client.has_communicated:
                client.close()

        except:
            pass
    return

 
# 开始游戏
label start:
    if not hasattr(persistent, "bg"):
        default persistent.bg = ""

    python:
        msg_dict = {}
        dialog = load_dialog()
        if dialog:
            msg_dict.update(dialog)
        socket_dict = {None: None}
        current_chat = None

    menu:
        "请选择模式"

        "服务端":
            python:
                server = RenServer()    
                server.run()
                server.set_conn_event(server_conn_handler)
                server.set_receive_event(receive_handler)
                server.set_disconn_event(disconn_handler)

            call screen chat("server")

        "客户端":
            python:
                ip = renpy.input("请输入ip地址")
                port = int(renpy.input("请输入端口号"))
                client = RenClient(ip, port)
                client.set_conn_event(client_conn_handler)
                client.set_receive_event(receive_handler)
                client.set_disconn_event(disconn_handler)
                msg_dict[ip] = []
                socket_dict[ip] = client.socket
                client.run()
                    
            call screen chat("client")

    return
    