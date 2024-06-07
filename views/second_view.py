#main_view
import flet as ft
from core.base import Model


class SecondView(Model):
    route = '/second'
    back_route = '/'

    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # def init(self):
    #     print("init")

    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("Second View"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT)

    controls = [
        ft.Text("Second Page"),
        ft.ElevatedButton("Go Home", on_click=lambda e: e.control.page.go('/'))
    ]

