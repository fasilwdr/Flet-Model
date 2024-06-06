#main_view
import flet as ft
from core.base import Model, Control


class SecondView(Model):
    route = '/second'
    back_route = '/'

    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("Second View"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT)
    go_button = Control(ft.ElevatedButton(text="Go Main View", on_click="on_click_go_button"), sequence=1)

    def on_click_go_button(self, e):
        self.page.go('/')


