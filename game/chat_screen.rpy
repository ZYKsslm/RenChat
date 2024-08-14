default current_chat = None
default mode = None
default persistent.bg = "images/bg.png"
default msg_dict = {}


screen chat():
    # 主窗体
    frame:
        align (0.5, 0.5)
        xysize (1000, 1000)

        if store.current_chat:
            text "与[store.current_chat!q]的聊天："

        # 聊天框
        fixed:
            xysize (1000, 600)
            align (0.5, 0.0)
            yoffset 50

            viewport:
                mousewheel True
                draggable True
                arrowkeys True

                vbox:
                    xsize 1000
                    spacing 10

                    if store.current_chat in store.msg_dict.keys():
                        for info in store.msg_dict[current_chat]:
                            use chat_panel(info)
        
        use input_screen()
    use bg()

screen chat_panel(info):
    $ msg, p = info

    if msg.type == Message.STRING:
        if p == "opposite":
            text "[msg.log_info['message']!q]":
                xalign 0.0 
                xoffset 50

        elif p == "me":
            text "[msg.log_info['message']!q]":
                xalign 1.0
                xoffset -50

    elif msg.type == Message.IMAGE:
        imagebutton:
            idle Transform(msg.get_image(), zoom=0.1)
            hover Transform(msg.get_image(), zoom=0.1, matrixcolor=BrightnessMatrix(-0.3))
            action ShowMenu("show_img", msg)

            if p == "opposite":
                xalign 0.0 
                xoffset 50

            elif p == "me":
                xalign 1.0
                xoffset -50
                
    elif msg.type == Message.AUDIO:
        imagebutton:
            idle "icon audio"
            hover "icon audio selected"
            action Function(play_audio, msg.get_audio())

            if p == "opposite":
                xalign 0.0 
                xoffset 50

            elif p == "me":
                xalign 1.0 
                xoffset -50
    
    elif msg.type == Message.MOVIE:
        imagebutton:
            idle "icon movie"
            hover "icon movie selected"
            action ShowMenu("play_video", msg.get_movie())

            if p == "opposite":
                xalign 0.0 
                xoffset 50
                
            elif p == "me":
                xalign 1.0 
                xoffset -50
    
screen input_screen():
    default content = ""

    frame:
        xysize (950, 300)
        align (0.5, 1.0)
        yoffset -20
            
        input yalign 0.0 copypaste True multiline True value LocalVariableInputValue("content")
        
        hbox:
            align (0.0, 1.0)
            spacing 10

            textbutton "菜单" text_size 40 action Show("chat_menu")
            textbutton "列表" text_size 40 action Show("conn_screen")

            if current_chat in store.msg_dict.keys():
                textbutton "图片" text_size 40 action Function(choose_file, mode=Message.IMAGE)
                textbutton "音频" text_size 40 action Function(choose_file, mode=Message.AUDIO)
                textbutton "视频" text_size 40 action Function(choose_file, mode=Message.MOVIE)
            
        if current_chat in store.msg_dict.keys():
            textbutton "发送" align (1.0, 1.0) text_size 40 action Function(send_handler, Message.string(content))
            # TODO: key "keyup_K_KP_ENTER"

screen conn_screen():
    # 连接列表
    frame:
        xysize (400, 1000)

        text "连接列表：" align (0.0, 0.0)
        textbutton "关闭" align (1.0, 0.0) action Hide()

        viewport:
            xysize (400, 920)
            mousewheel True
            draggable True
            arrowkeys True
            yoffset 50

            vbox:
                xsize 400
                spacing 10
                style_prefix "radio"

                if store.mode == "server":
                    for client_name in store.server.client_socket_dict.keys():
                        textbutton "[client_name!q]" action [SetVariable("current_chat", client_name), Hide()]
                else:
                    textbutton "[store.client.target_address!q]" action [SetVariable("current_chat", store.client.target_address), Hide()]

        at transform:
            on show:
                xpos -400
                linear 0.15 xpos 0
            on hide:
                linear 0.15 xpos -400

screen chat_menu():

    frame:
        xysize (400, 1000)
        textbutton "关闭" align (1.0, 0.0) action Hide()

        vbox:
            xsize 400
            spacing 20
            
            if store.mode == "server":
                text "IP地址"
                textbutton "[store.server.ip!q]" action NullAction()
                text "端口号"
                textbutton "[store.server.port!q]" action NullAction()
                text "服务"
                textbutton "重启服务" action [Function(store.server.reboot), Hide()]
                textbutton "断开当前连接" action [Function(close_handler), Hide()]
            else:
                text "服务"
                textbutton "重启服务" action [Function(store.client.reboot), Hide()]
                textbutton "断开连接" action [Function(store.client.close), Hide()]
                
            textbutton "日志" action Function(start_log)

            text "界面"
            textbutton "选择壁纸" action Function(set_bg)

        at transform:
            on show:
                xpos -400
                linear 0.15 xpos 0
            on hide:
                linear 0.15 xpos -400

screen bg():
    add DynamicDisplayable(get_bg)

screen show_img(msg):
    add msg.get_image() at truecenter

    hbox:
        style_prefix "quick"
        align (0.5, 1.0)

        textbutton "保存" action Function(save_file, msg)
        textbutton "返回" action Return()

screen play_video(movie):
    add movie at truecenter
    