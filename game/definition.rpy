image icon file:
    "images/file.png"
    xysize (80, 80)

image icon audio:
    "images/audio.png"
    xysize (80, 80)

image icon movie:
    "images/movie.png"
    xysize (80, 80)

image icon file selected:
    "images/file.png"
    xysize (80, 80)
    matrixcolor BrightnessMatrix(-0.3)

image icon audio selected:
    "images/audio.png"
    xysize (80, 80)
    matrixcolor BrightnessMatrix(-0.3)

image icon movie selected:
    "images/movie.png"
    xysize (80, 80)
    matrixcolor BrightnessMatrix(-0.3)
    

# 定义回调函数
init python:

    server = RenServer()
    client = RenClient()

    @server.on_conn()
    def server_conn_handler(server: RenServer, client_name: str, client_socket: socket.socket):
        if not client_name in store.msg_dict.keys():
            store.msg_dict[client_name] = []
        renpy.notify(f"有新的连接：{client_name}，请到列表中查看")
    
    @client.on_conn()
    def client_conn_handler(client: RenClient):
        if not client.target_address in store.msg_dict.keys():
            store.msg_dict[client.target_address] = []
        renpy.notify(f"成功连接：{client.target_address}，请到列表中查看")
    
    @server.on_disconn()
    def server_disconn_handler(server: RenServer, client_name: str):
        store.msg_dict.pop(client_name)
        renpy.notify(f"{client_name}断开连接")
 
    @client.on_disconn()
    def client_disconn_handler(client: RenClient):
        store.msg_dict.pop(client.target_address)
        renpy.notify(f"与服务器断开连接")

    @server.on_recv()
    def server_recv_handler(server: RenServer, client_name: str, client_socket: socket.socket, msg: Message):
        if msg.type == Message.STRING:
            renpy.notify(f"{client_name}：{msg.log_info['message']}")
        elif msg.type == Message.IMAGE:
            renpy.notify(f"{client_name}：[图片]")
        elif msg.type == Message.AUDIO:
            renpy.notify(f"{client_name}：[语音]")
        elif msg.type == Message.MOVIE:
            renpy.notify(f"{client_name}：[视频]")

        store.msg_dict[client_name].append((msg, "opposite"))

    @client.on_recv()
    def client_recv_handler(client: RenClient, msg: Message):
        socket_name = client.target_address

        if msg.type == Message.STRING:
            renpy.notify(f"{socket_name}：{msg.log_info['message']}")
        elif msg.type == Message.IMAGE:
            renpy.notify(f"{socket_name}：[图片]")
        elif msg.type == Message.AUDIO:
            renpy.notify(f"{socket_name}：[语音]")
        elif msg.type == Message.MOVIE:
            renpy.notify(f"{socket_name}：[视频]")

        store.msg_dict[socket_name].append((msg, "opposite"))

    def send_handler(msg: Message):
        if store.mode == "server":
            socket = store.server.client_socket_dict[store.current_chat]
            store.server.send(socket, msg)
        else:
            store.client.send(msg)
        
        store.msg_dict[store.current_chat].append((msg, "me"))

    def close_handler():
        if store.current_chat in store.server.client_socket_dict.keys():
            store.server.client_socket_dict[store.current_chat].close()

# 功能
init python: 
    
    import os
    import re
    import time

    import _renpytfd


    def get_bg(st, at):
        return Transform(Image(persistent.bg), alpha=0.15, xysize=(1920, 1080)), None
    
    config.always_shown_screens.append("bg")

    def set_bg():
        img_path = _renpytfd.openFileDialog("选择背景图片", "", "", "")
        if os.path.splitext(img_path)[1] not in [".jpg", ".png", ".jpeg", ".webp"]:
            renpy.notify("请选择正确的图片格式")
            return

        persistent.bg = re.sub(r"\\", "/", img_path)

    def start_log():
        os.startfile(os.path.join(config.basedir, "RenCommunicator.log"))

    def save_file(msg):
        path = Message.parse_path(f"images/{time.time()}{msg.log_info['format']}")
        with open(path, "wb") as f:
            f.write(msg.data)

        renpy.notify(f"文件已保存到{path}")

    def choose_file(mode):
        if mode == Message.IMAGE:
            path = _renpytfd.openFileDialog("选择图片", "", "", "")
            if not path:
                return
            if os.path.splitext(path)[1] not in [".jpg", ".png", ".jpeg", ".webp"]:
                renpy.notify("请选择正确的图片格式")
                return
            msg = Message.image(path)

        elif mode == Message.AUDIO:
            path = _renpytfd.openFileDialog("选择音频", "", "", "")
            if not path:
                return
            msg = Message.audio(path)

        elif mode == Message.MOVIE:
            path = _renpytfd.openFileDialog("选择视频", "", "", "")
            if not path:
                return
                return
            msg = Message.movie(path)
        
        send_handler(msg)

    def play_audio(audio):
        renpy.music.play(audio)