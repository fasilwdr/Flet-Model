#main_view
import flet as ft
from core.base import Model, Control
from core.controls import UserError, UserInfo, UserWarning
import datetime


class MainView(Model):
    route = '/'
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # def init(self):
    #     print("init")

    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("Main View"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT)

    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Explore",
            ),
        ]
    )
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )

    #DatePicker
    def change_date(self, e):
        print(f"Date picker changed, value is {self.date_picker.value}")

    def date_picker_dismissed(self, e):
        print(f"Date picker dismissed, value is {self.date_picker.value}")

    date_picker = Control(
        ft.DatePicker(
            on_change="change_date",
            on_dismiss="date_picker_dismissed",
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        ),
        overlay=True
    )

    #Banner
    def close_banner(e):
        e.control.page.close_banner()
        print("banner closed")

    banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Oops, there were some errors while trying to delete the file. What would you like me to do?"
        ),
        actions=[
            ft.TextButton("Retry", on_click=close_banner),
            ft.TextButton("Ignore", on_click=close_banner),
            ft.TextButton("Cancel", on_click=close_banner),
        ],
    )

    #AlertDialog
    dlg = Control(ft.AlertDialog(
        title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
    ), dialog=True)

    dlg_modal = Control(ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: e.control.page.close_dialog()),
            ft.TextButton("No", on_click=lambda e: e.control.page.close_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    ))

    #BottomSheet
    bottom_sheet = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("This is sheet's content!"),
                    ft.ElevatedButton("Close bottom sheet", on_click=lambda e: e.control.page.close_bottom_sheet()),
                ],
                tight=True,
            ),
            padding=10,
        ),
        open=True,
        on_dismiss=lambda e: print("Bottom Sheet dismissed!"),
    )

    actions = ft.Dropdown(
        options=[
            ft.dropdown.Option("Open Drawer"),
            ft.dropdown.Option("Show Banner"),
            ft.dropdown.Option("Open DatePicker"),
            ft.dropdown.Option("Show Dialog"),
            ft.dropdown.Option("Show Dialog Modal"),
            ft.dropdown.Option("Show BottomSheet"),
            ft.dropdown.Option("Check UserError (SnackBar)"),
            ft.dropdown.Option("Check UserInfo (SnackBar)"),
            ft.dropdown.Option("Check UserWarning (SnackBar)"),
            ft.dropdown.Option("Go to Second Page"),
        ],
    )
    text = ft.TextField(label="Text")
    sample = Control(
        ft.ResponsiveRow(
            controls=[
                ft.Text("Check how to perform the flet controls in this Flet-Model", size=15, text_align="center", color=ft.colors.PRIMARY),
                actions,
                text
            ]
        ),
        sequence=1
    )
    check_button = Control(ft.ElevatedButton(text="Check", on_click="on_click_check_button"), sequence=2)

    def on_click_check_button(self, e):
        if self.actions.value == 'Check UserError (SnackBar)':
            return UserError(self.page, "Error Message")
        elif self.actions.value == 'Check UserInfo (SnackBar)':
            return UserInfo(self.page, "Info Message")
        elif self.actions.value == 'Check UserWarning (SnackBar)':
            return UserWarning(self.page, "Warning Message")
        elif self.actions.value == 'Open Drawer':
            self.page.show_drawer(self.drawer)
        elif self.actions.value == 'Go to Second Page':
            self.page.go('/second')
        elif self.actions.value == 'Open DatePicker':
            self.date_picker.pick_date()
        elif self.actions.value == 'Show Banner':
            self.page.show_banner(self.banner)
        elif self.actions.value == 'Show Dialog':
            self.page.show_dialog(self.dlg)
        elif self.actions.value == 'Show Dialog Modal':
            self.page.show_dialog(self.dlg_modal)
        elif self.actions.value == 'Show BottomSheet':
            self.page.show_bottom_sheet(self.bottom_sheet)


