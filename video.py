import glob
import os
import datetime
import math
import cv2
import base64
from ftplib import FTP
import flet as ft


class VideoPlayer(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):

        # プレイリスト定義
        self.play_list = []
        self.play_list_table = ft.Column()

        # ファイルのインポート
        files = glob.glob(r"D:\video\その他\*.mp4")

        # ファイルリストからプレイリストを作成
        for i, file in enumerate(files):
            # プレイリストにファイルを追加
            self.play_list.append(ft.VideoMedia(file))
            # ファイルの再生時間を取得
            cap = cv2.VideoCapture(file)
            sec = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
            time = datetime.timedelta(seconds=round(sec))
            # ファイルのサイズを取得
            size = self.convert_size(os.path.getsize(file))
            #サムネイル
            _, img = cap.read()
            width, height = img.shape[1], img.shape[0]
            newWidth = 100
            newHeiight = int(height * newWidth / width)
            img = cv2.resize(img, (newWidth, newHeiight))
            _, encode = cv2.imencode(".jpg", img)
            img_base64 = base64.b64encode(encode).decode("ascii")
            # ファイル情報をプレイリストに追加
            self.play_list_table.controls.append(
                ft.CupertinoListTile(
                    additional_info=ft.Text(str(time)),
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    trailing=ft.IconButton(icon=ft.cupertino_icons.PLAY, on_click=self.on_click_icon),
                    title=ft.Text(f"{i + 1}. {self.path_to_name(file)}"),
                    subtitle=ft.Text(size),
                    leading=ft.Image(src_base64=img_base64),
                    leading_size=80,
                    padding=0
                )
            )
            cap.release()

        # 動画タイトル
        self.video_title = ft.Text(size=24, weight=ft.FontWeight.BOLD)
        # 動画更新日時
        self.updt_dt = ft.Text()
        # 動画サイズ
        self.video_size = ft.Text()
        # 再生中インデックス
        self.curr_index = 0

        # 動画プレイヤー
        self.video_player = ft.Video(
            expand=True,
            playlist=self.play_list,
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.BLACK26,
            aspect_ratio=1920/1080,
            volume=10,
            autoplay=False,
            filter_quality=ft.FilterQuality.HIGH,
            muted=False,
            on_loaded=self.on_loaded,
            on_track_changed=self.on_track_changed,
            on_error=self.on_error
        )

        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            width=960,
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[self.video_title]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Row(
                            width=910,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                self.updt_dt,
                                self.video_size
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.IconButton(
                                    icon=ft.cupertino_icons.CLOUD_DOWNLOAD,
                                    on_click=self.on_click_download
                                )
                            ]
                        )
                    ]
                ),
                self.video_player,
                ft.Container(padding=15),
                self.play_list_table
            ]
        )

    def on_click_icon(self, e):
        """
        プレイリストアイコン押下処理
        """
        index = int(e.control.key)
        if e.control.data:
            self.video_player.play_or_pause()
            if self.video_player.is_playing():
                self.play_list_table.controls[index].trailing.icon = ft.cupertino_icons.PAUSE
            else:
                self.play_list_table.controls[index].trailing.icon = ft.cupertino_icons.PLAY_FILL
        else:
            self.video_player.jump_to(index)
        self.update()

    def on_loaded(self, e):
        """
        動画読込完了処理1
        """
        self.video_change(0)

    def on_track_changed(self, e):
        """
        トラック変更処理
        """
        self.curr_index = int(e.data)
        self.video_change(int(e.data))

    def video_change(self, index):
        """
        動画変更処理
        """
        # プレイリストから再生中のファイルを取得
        now_file = self.video_player.playlist[index].resource
        # プレイリストテーブルを初期化
        for i, v in enumerate(self.play_list_table.controls):
            v.trailing.icon = ft.cupertino_icons.PLAY
            v.trailing.key = i
            v.trailing.data = False
            v.title.size = ""
            v.title.weight = ""
            v.title.color = ""
            v.bgcolor = ""
        # プレイリストテーブルの再生中リストアイテムを更新
        now_list = self.play_list_table.controls[index]
        now_list.trailing.icon = ft.cupertino_icons.PAUSE
        now_list.trailing.data = True
        now_list.title.size = 18
        now_list.title.weight = ft.FontWeight.BOLD
        now_list.title.color = ft.colors.BLUE_GREY
        now_list.bgcolor = ft.colors.SURFACE_VARIANT
        # 再生中動画情報を更新
        self.video_title.value = self.path_to_name(now_file)
        self.updt_dt.value = f"更新日時：{datetime.datetime.fromtimestamp(os.path.getatime(now_file))}"
        self.video_size.value = f"サイズ：{self.convert_size(os.path.getsize(now_file))}"
        # 表示を更新
        self.update()

    def on_error(self, e):
        """
        エラーハンドラ
        """
        print("error occured.")
        print(e)

    def on_click_download(self, e):
        file = self.path_to_name(self.play_list[self.curr_index].resource)
        print(file)
        host = '172.19.16.1'
        user = "user"
        password = "8107"
        FTP.encoding = "utf-8"
        ftp = FTP(host)
        ftp.set_pasv('true')
        ftp.login(user, password)
        print('ログインしました')
        ftp.cwd('X')
        print(ftp.pwd())
        with open(file, 'wb') as fp:
            print('読み込み')
            print(fp.name)
            ftp.retrbinary('RETR output.mp4', fp.write)
        ftp.close()

    def convert_size(self, byte):
        """
        バイトサイズ変換
        """
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
        i = math.floor(math.log(byte, 1024)) if byte > 0 else 0
        size = round(byte / 1024 ** i, 2)
        return f"{size} {units[i]}"
    
    def path_to_name(self, path):
        """
        ファイル名変換
        """
        return os.path.splitext(os.path.basename(path))[0]