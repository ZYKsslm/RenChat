define config.rollback_enabled = False
define config.save = False


# 开始游戏
label start:

    window hide
    show screen bg

    menu:
        "请选择模式"

        "服务器":
            python:
                with store.server:
                    store.mode = "server"
                    renpy.call_screen("chat")

        "客户端":
            python:
                ip = renpy.input("请输入服务器ip地址")
                port = int(renpy.input("请输入服务器端口号"))
                
                with store.client.set_target(ip, port):
                    store.mode = "client"
                    renpy.call_screen("chat")

    return
    