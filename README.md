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
from flet_model import Model, Router


class First(Model):
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
        self.page.go('/first/second')


class Second(Model):
    route = 'second'
    title = "Test"
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


def main(page: ft.Page):
    page.title = "Title"
    page.theme_mode = "light"
    # Initialize router with route mappings
    Router(
        {'first': First(page)},
        {'second': Second(page)}
    )

    page.go(page.route)


ft.app(target=main)
```

## Features

- Model-based view definition
- Automatic route handling
- Event binding
- Support for nested routes
- Easy navigation between views
- View caching for improved performance
- Comprehensive UI component configuration (AppBar, BottomAppBar, FAB, etc.)
- Auto-binding of event handlers with caching
- Thread-safe initialization hooks (init and post_init)
- Support for overlay controls
- Customizable layout properties (alignment, padding, spacing)
- Keyboard event handling
- Scroll event handling
- Flexible control definition (static list or callable)
- Built-in view state management
- Navigation drawer support (both start and end)
- Built-in support for fullscreen dialogs

## License

This project is licensed under the MIT License.