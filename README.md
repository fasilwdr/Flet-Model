# Flet Model

A Model-based router for Flet applications that simplifies the creation of multi-page applications.

## Installation

```bash
pip install flet-model
```

## Usage

Here's a simple example of how to use Flet Model:

```python
import flet as ft
from flet_model import main, Model

class FirstView(Model):
    route = 'first'
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER

    appbar = ft.AppBar(
        title=ft.Text("First View"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE)
    controls = [
        ft.ElevatedButton("Go to Second Page", on_click="go_second")
    ]

    def go_second(self, e):
        self.page.go('first/second')

class SecondView(Model):
    route = 'second'
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER

    appbar = ft.AppBar(
        title=ft.Text("Second View"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE)
    controls = [
        ft.ElevatedButton("Go to First", on_click="go_first")
    ]

    def go_first(self, e):
        self.page.go('first')

# Run the Flet app
ft.app(target=main)
```

## Features

- Model-based view definition
- Automatic route handling
- Event binding
- Support for nested routes
- Easy navigation between views

## License

This project is licensed under the MIT License.