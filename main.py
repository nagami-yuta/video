import flet as ft
from video import VideoPlayer


def main(page: ft.Page):
    """
    アプリのウィンドウに関する定義
    """
    page.title = "VIDEO PLAYER"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 40

    # ヘッダー
    def toggle_icon(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        toggle_dark_light_icon.selected = not toggle_dark_light_icon.selected
        page.update()

    toggle_dark_light_icon = ft.IconButton(
        icon="light_mode",
        selected_icon="dark_mode",
        tooltip=f"switch light / dark mode",
        on_click=toggle_icon
    )

    page.appbar = ft.AppBar(
        leading=ft.Icon(name=ft.cupertino_icons.PLAY_RECTANGLE_FILL, size=40),
        leading_width=100,
        title=ft.Text(value="MOVIE PLAYER", size=32, text_align=ft.TextAlign.CENTER),
        center_title=True,
        toolbar_height=60,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.Row(
                    [toggle_dark_light_icon],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                margin=ft.margin.only(left=50, right=25)
            )
        ]
    )

    video_player = VideoPlayer()
    page.add(video_player)
    page.update()


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)