import flet as ft
from datetime import datetime, date


def UserError(page, text):
    snackbar = ft.SnackBar(content=ft.Text(text, color=ft.colors.WHITE, text_align="center"), open=True, bgcolor=ft.colors.RED)
    page.show_snack_bar(snackbar)


def UserInfo(page, text):
    snackbar = ft.SnackBar(content=ft.Text(text, color=ft.colors.WHITE, text_align="center"), open=True, bgcolor=ft.colors.BLUE)
    page.show_snack_bar(snackbar)


def UserWarning(page, text):
    snackbar = ft.SnackBar(content=ft.Text(text, color=ft.colors.BLACK, text_align="center"), open=True, bgcolor=ft.colors.YELLOW)
    page.show_snack_bar(snackbar)


def get_formated_date(date_string, format):
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = date_object.strftime(format)
    return formatted_date


class DateField(ft.Container):
    def __init__(self, label, value='', col=None, format='%d-%m-%Y'):
        super().__init__()
        self.value = value
        self.format = format
        self.date_picker = ft.DatePicker(
            on_change=self.change_date,
            current_date=datetime.strptime(self.value, '%d-%m-%Y').date() if self.value else None,
            first_date=date(2023, 10, 1),
        )
        self.content = ft.Row(controls=[
            ft.Text(label),
            ft.IconButton(ft.icons.DATE_RANGE, on_click=self.pick_date),
            ft.Text(self.value)
        ])
        self.col = col
        # self.border = ft.InputBorder.NONE
        self.padding = 5
        self.bgcolor = ft.colors.SURFACE

    def pick_date(self, e):
        self.page.overlay.append(self.date_picker)
        self.page.update()
        self.date_picker.pick_date()
    def change_date(self, e):
        self.value = get_formated_date(e.data, self.format)
        self.content.controls[-1].value = self.value
        self.content.controls[-1].update()