image chat_bg:
    "images/bg.png"
    xysize (1920, 1080)
    alpha 0.15

image file_icon:
    "images/file.png"
    xysize (80, 80)

image voice_icon:
    "images/voice.png"
    xysize (80, 80)

image video_icon:
    "images/video.png"
    xysize (80, 80)

image file_icon selected:
    "images/file.png"
    xysize (80, 80)
    alpha 0.5

image voice_icon selected:
    "images/voice.png"
    xysize (80, 80)
    alpha 0.5

image video_icon selected:
    "images/video.png"
    xysize (80, 80)
    alpha 0.5


init python:
    config.always_shown_screens.append("bg")

    def server_conn_handler(socket):
        socket_name = str(socket.getpeername())
        store.socket_dict[socket_name] = socket
        if not socket_name in store.msg_dict.keys():
            store.msg_dict[socket_name] = []
        renpy.notify(f"有新的连接：{socket_name}，请到列表中查看")
    
    def client_conn_handler():
        socket_name = store.client.target_ip
        store.socket_dict[socket_name] = store.client.socket
        if not socket_name in store.msg_dict.keys():
            store.msg_dict[socket_name] = []
        renpy.notify(f"成功连接：{socket_name}，请到列表中查看")
 
    def disconn_handler(name=None):
        if not name:
            name = store.ip
        renpy.notify(f"{name}断开连接")
 
    def receive_handler(msg, socket=None):
        if socket:
            socket_name = str(socket.getpeername())
        else:
            socket_name = store.ip

        if msg["type"] == Message.STRING:
            renpy.notify(f"收到{socket_name}的消息：\n{msg['message']}")
        elif msg["type"] == Message.IMAGE:
            renpy.notify(f"收到{socket_name}的消息：\n[图片]")
        elif msg["type"] == Message.VOICE:
            renpy.notify(f"收到{socket_name}的消息：\n[语音]")
            msg["save_path"] = None
        elif msg["type"] == Message.VIDEO:
            renpy.notify(f"收到{socket_name}的消息：\n[视频]")
            msg["save_path"] = None
        else:
            renpy.notify(f"收到{socket_name}的消息：\n[文件]")
            msg["save_path"] = None

        store.msg_dict[socket_name].append([msg, "opposite"])

    def send_handler(mode, msg, socket=None, tp=Message.STRING):
        if msg == "":
            return
        if not isinstance(msg, Message):
            msg = Message(msg, tp)
            info = pickle.loads(msg.info)
        if tp != Message.STRING:
            info["save_path"] = None
        
        if info["format"] and tp == Message.STRING:
            renpy.notify("文件格式错误！")
            return

        try:
            if mode == "server":
                store.server.send(socket, msg)
            else:
                store.client.send(msg)
        except:
            pass
        else:
            if store.current_chat:
                store.msg_dict[store.current_chat].append([info, "me"])
    

    def set_bg(img_path):
        with open(img_path, "rb") as f:
            img = im.Data(f.read(), img_path)
        img = Transform(img)
        img.alpha = 0.15
        img.xysize = (1920, 1080)
        persistent.bg = img_path

    def save_file(data, fmt, notice=True):
        import time, re

        save_path = os.path.join(config.gamedir, "chat_file", str(time.time()) + fmt)
        save_path = re.sub(r"\\", "/", save_path)
        with open(save_path, "wb") as f:
            f.write(data)
        
        if notice:
            renpy.notify("保存成功")

        return save_path

    def save_dialog():
        save_path = os.path.join(config.gamedir, "dialog", f"dialog.pkl")
        with open(save_path, "wb+") as f:
            dialog = {}
            for name in store.msg_dict.keys():
                dialog[f"{name}-save"] = store.msg_dict[name]
            pickle.dump(dialog, f)

    def load_dialog():
        save_path = os.path.join(config.gamedir, "dialog", f"dialog.pkl")
        if os.path.exists(save_path):
            with open(save_path, "rb") as f:
                return pickle.load(f)

    def clean_cache():
        cache_path = os.path.join(config.gamedir, "chat_file")
        for file in os.listdir(cache_path):
            f = os.path.join(cache_path, file)
            os.remove(f)

    def play_voice(msg):
        if msg["save_path"]:
            voice_path = msg["save_path"]
        else:
            voice_path = save_file(msg["data"], msg["format"], False)
            msg["save_path"] = voice_path

        renpy.play(voice_path, "voice")

    def start_file(msg):
        if msg["save_path"]:
            file_path = msg["save_path"]
        else:
            file_path = save_file(msg["data"], msg["format"], False)
            msg["save_path"] = file_path

        os.startfile(file_path)