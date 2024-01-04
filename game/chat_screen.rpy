screen chat(mode):
    default content = ""

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

                    if store.current_chat:
                        for info in store.msg_dict[store.current_chat]:
                            $ msg = info[0]
                            $ p = info[1]

                            if msg["type"] == Message.STRING:
                                $ msg = msg["message"]
                                if p == "opposite":
                                    text "[msg!q]":
                                        xalign 0.0 
                                        xoffset 50
                                elif p == "me":
                                    text "[msg!q]":
                                        xalign 1.0
                                        xoffset -50

                            elif msg["type"] == Message.IMAGE:
                                python:
                                    img = im.Data(msg["data"], msg["format"])
                                    preview = Transform(img)
                                    preview.zoom = 0.1

                                if p == "opposite":
                                    imagebutton:
                                        idle preview
                                        xalign 0.0 
                                        xoffset 50
                                        action ShowMenu("show_img", img, msg["data"], msg["format"])

                                elif p == "me":
                                    imagebutton:
                                        idle preview
                                        xalign 1.0
                                        xoffset -50
                                        action ShowMenu("show_img", img, msg["data"], msg["format"])
                            
                            elif msg["type"] == Message.VOICE:
                                if p == "opposite":
                                    imagebutton:
                                        idle "voice_icon"
                                        hover "voice_icon selected"
                                        xalign 0.0 
                                        xoffset 50
                                        action Function(play_voice, msg)

                                elif p == "me":
                                    imagebutton:
                                        idle "voice_icon"
                                        hover "voice_icon selected"
                                        xalign 1.0 
                                        xoffset -50
                                        action Function(play_voice, msg)
                            
                            elif msg["type"] == Message.VIDEO:
                                if p == "opposite":
                                    imagebutton:
                                        idle "video_icon"
                                        hover "video_icon selected"
                                        xalign 0.0 
                                        xoffset 50
                                        action ShowMenu("play_video", msg)

                                elif p == "me":
                                    imagebutton:
                                        idle "video_icon"
                                        hover "video_icon selected"
                                        xalign 1.0 
                                        xoffset -50
                                        action ShowMenu("play_video", msg)
                            
                            elif msg["type"] == Message.FILE:
                                if p == "opposite":
                                    imagebutton:
                                        idle "file_icon"
                                        hover "file_icon selected"
                                        xalign 0.0 
                                        xoffset 50
                                        action Function(start_file, msg)

                                elif p == "me":
                                    imagebutton:
                                        idle "file_icon"
                                        hover "file_icon selected"
                                        xalign 1.0 
                                        xoffset -50
                                        action Function(start_file, msg)
        
        # 输入框
        frame:
            xysize (950, 300)
            align (0.5, 1.0)
            yoffset -20
                
            input yalign 0.0 copypaste True multiline True value ScreenVariableInputValue("content")
            
            hbox:
                align (0.0, 1.0)
                spacing 10

                textbutton "菜单" text_size 40 action Show("chat_menu", mode=mode, socket=socket)
                textbutton "列表" text_size 40 action Show("conn_screen", mode=mode)

                if store.current_chat in store.socket_dict:
                    $ socket = store.socket_dict[store.current_chat]
                    textbutton "文件" text_size 40 action ShowMenu("choose_file", mode, Message.FILE, socket)
                    textbutton "图片" text_size 40 action ShowMenu("choose_file", mode, Message.IMAGE, socket)
                    textbutton "音频" text_size 40 action ShowMenu("choose_file", mode, Message.VOICE, socket)
                    textbutton "视频" text_size 40 action ShowMenu("choose_file", mode, Message.VIDEO, socket)
                
            if store.current_chat in store.socket_dict:
                textbutton "发送" align (1.0, 1.0) text_size 40 action Function(send_handler, mode=mode, msg=content, socket=socket)
                # TODO: key "keyup_K_KP_ENTER"

    use bg


screen conn_screen(mode):
    roll_forward False
    $ dialog = load_dialog()

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

                if mode == "server":
                    for conn in store.server.client_socket_list:
                        $ name = str(conn.getpeername())
                        textbutton "[name!q]" action [SetVariable("current_chat", name), Hide()]
                else:
                    textbutton "[store.ip]" action [SetVariable("current_chat", store.ip), Hide()]

                if dialog:
                    for name in dialog.keys():
                        textbutton "[name!q]" action [SetVariable("current_chat", name), Hide()]

        
        at transform:
            on show:
                xpos -400
                linear 0.15 xpos 0
            on hide:
                linear 0.15 xpos -400
    
    use bg


screen chat_menu(mode, socket=None):
    roll_forward False

    frame:
        xysize (400, 1000)
        textbutton "关闭" align (1.0, 0.0) action Hide()

        vbox:
            xsize 400
            spacing 20

            if mode == "server":
                text "IP地址"
                textbutton "[store.server.ip!q]" action NullAction()
                text "端口号"
                textbutton "[store.server.port!q]" action NullAction()
                text "服务"
                textbutton "重启服务" action [Function(store.server.reboot), Hide()]
                textbutton "断开当前连接" action [Function(store.server.close_a_conn, socket), Hide()]
            else:
                text "服务"
                textbutton "重启服务" action [Function(store.client.reboot), Hide()]
                textbutton "断开连接" action [Function(store.client.close), Hide()]
                
            textbutton "清除缓存" action [Function(clean_cache), Hide()]
            textbutton "保存聊天记录" action [Function(save_dialog), Hide()]
            textbutton "日志" action ShowMenu("log", mode)

            text "界面"
            textbutton "选择壁纸" action ShowMenu("change_bg")

        at transform:
            on show:
                xpos -400
                linear 0.15 xpos 0
            on hide:
                linear 0.15 xpos -400
    
    use bg


screen change_bg():
    default img_path = ""

    frame:
        xysize (600, 300)
        align (0.5, 0.5)

        text "请输入壁纸目录" align (0.5, 0.0)
        input yalign 0.5 copypaste True value ScreenVariableInputValue("img_path")
        textbutton "完成" align (0.0, 1.0) action [Function(set_bg, img_path), Return()]
        textbutton "取消" align (1.0, 1.0) action Return()

    use bg


screen choose_file(mode, tp, socket=None):
    default file_path = ""

    text "文件发送失败很可能是主机最大接收数据大小过小，请更改max_data_size属性" xalign 0.5

    frame:
        xysize (600, 300)
        align (0.5, 0.5)

        text "请输入文件目录" align (0.5, 0.0)
        input yalign 0.5 copypaste True value ScreenVariableInputValue("file_path")
        textbutton "完成" align (0.0, 1.0) action [Function(send_handler, mode=mode, msg=file_path, tp=tp, socket=socket), Return()]
        textbutton "取消" align (1.0, 1.0) action Return()

    use bg


screen bg():
    $ img_path = persistent.bg
    if img_path:
        python:
            with open(img_path, "rb") as f:
                img = im.Data(f.read(), img_path)
            img = Transform(img)
            img.alpha = 0.15
            img.xysize = (1920, 1080)

        add img
    else:
        add "chat_bg"


screen show_img(img, img_data, tp):
    add img at truecenter

    hbox:
        style_prefix "quick"
        align (0.5, 1.0)

        textbutton "保存" action Function(save_file, img_data, tp)
        textbutton "返回" action Return()


screen play_video(msg):
    python:
        if msg["save_path"]:
            video_path = msg["save_path"]
        else:
            video_path = save_file(msg["data"], msg["format"], False)
            msg["save_path"] = video_path
        
        video = Movie(play=video_path, loop=False)
    
    add video at truecenter


screen log(mode):
    python:
        if mode == "server":
            log = server.log
        else:
            log = client.log

    frame:
        align (0.5, 0.5)
        xysize (500, 1000)

        text "错误日志"
        viewport:
            mousewheel True
            draggable True
            arrowkeys True
            yoffset 50
            
            vbox:
                spacing 20

                for e in log.keys():
                    text e
                    $ info = log[e]
                    textbutton "[info!q]" action NullAction()
    
    use bg