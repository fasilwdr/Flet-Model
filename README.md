# Flet Model

A Model-based router for Flet applications that simplifies the creation of multi-page applications with built-in state management and navigation.

## Installation

```bash
pip install flet-model
```

## Core Features

- Model-based view architecture
- Automatic route handling and nested routes
- Event binding with caching for improved performance
- Built-in view state management
- Navigation handling (drawers, bottom bar, FAB)
- Thread-safe initialization hooks
- Support for keyboard and scroll events
- View caching system

## Basic Usage

```python
import flet as ft
from flet_model import Model, Router


class HomeModel(Model):
    route = 'home'

    # Layout configuration
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER
    padding = 20
    spacing = 10

    # UI Components
    appbar = ft.AppBar(
        title=ft.Text("Home"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
    )

    controls = [
        ft.Text("Welcome to Home Page", size=24),
        ft.ElevatedButton("Go to Profile", on_click="navigate_to_profile")
    ]

    def navigate_to_profile(self, e):
        self.page.go('/home/profile')


class ProfileModel(Model):
    route = 'profile'

    # Layout configuration
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER
    padding = 20
    spacing = 10

    # UI Components
    appbar = ft.AppBar(
        title=ft.Text("Profile"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
    )

    controls = [
        ft.Text("Welcome to Profile Page", size=24),
    ]


def main(page: ft.Page):
    page.title = "Flet Model Demo"
    Router(
        {'home': HomeModel(page)},
        {'profile': ProfileModel(page)},
    )
    page.go(page.route)


ft.app(target=main)
```

## Advanced Features

### 1. Route Data Passing

```python
# Navigate with data
self.page.go('/products#id=123&category=electronics')

class ProductModel(Model):
    def init(self):
        # Access route data
        product_id = self.route_data.get('id')
        category = self.route_data.get('category')
```

### 2. Navigation Drawers

```python
class DrawerModel(Model):
    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.HOME,
                label="Home",
                selected_icon=ft.Icons.HOME_OUTLINED
            )
        ]
    )

    end_drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SETTINGS,
                label="Settings"
            )
        ]
    )

    controls = [
        ft.ElevatedButton('Open Drawer', on_click=lambda e: e.control.page.open(e.control.data), data=drawer),
        ft.ElevatedButton('Open End Drawer', on_click=lambda e: e.control.page.open(e.control.data), data=end_drawer)
    ]
```

### 3. Event Handlers and Lifecycle Hooks

```python
class EventModel(Model):
    def init(self):
        # Called before view creation
        self.load_data()
    
    def post_init(self):
        # Called after view creation
        self.setup_listeners()
    
    def on_keyboard_event(self, e: ft.KeyboardEvent):
        if e.key == "Enter":
            self.handle_enter()
    
    def on_scroll(self, e: ft.OnScrollEvent):
        if e.pixels >= e.max_scroll_extent - 100:
            self.load_more_data()
```

### 4. Floating Action Button

```python
class FABModel(Model):
    floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click="add_item"
    )
    floating_action_button_location = ft.FloatingActionButtonLocation.END_DOCKED
```

### 5. Bottom Navigation

```python
class NavigationModel(Model):
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.Icons.PERSON, label="Profile")
        ],
        on_change="handle_navigation"
    )
```

### 6. Overlay Controls

```python
class OverlayModel(Model):
    overlay_controls = [
        ft.Banner(
            open=True,
            content=ft.Text("Important message!"),
            actions=[
                ft.TextButton("Dismiss", on_click="dismiss_banner")
            ]
        )
    ]

    def dismiss_banner(self, e):
        self.page.close(e.control.parent)
```

### 7. Fullscreen Dialogs

```python
class DialogModel(Model):
    route = "dialog"
    fullscreen_dialog = True

    controls = [
        ft.Text("Dialog Content"),
        ft.ElevatedButton("Close", on_click="close_dialog")
    ]

    def close_dialog(self, e):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)
```

## Real-world Example

Here's a complete example of a todo application using Flet Model:

```python
import flet as ft
from flet_model import Model, Router
from typing import List


class TodoItem:
    def __init__(self, title: str, completed: bool = False):
        self.title = title
        self.completed = completed


class TodoModel(Model):
    route = "todo"
    todos: List[TodoItem] = []

    appbar = ft.AppBar(
        title=ft.Text("Todo List"),
        center_title=True
    )

    def get_controls(self):
        return [
            ft.TextField(
                hint_text="Add new todo",
                on_submit="add_todo",
                autofocus=True
            ),
            ft.Column(controls=self.get_todo_control())
        ]

    def get_todo_control(self):
        return [
            ft.Checkbox(
                label=todo.title,
                value=todo.completed,
                on_change=lambda e, t=todo: self.toggle_todo(e, t)
            ) for todo in self.todos
        ]

    controls = [
            ft.TextField(
                hint_text="Add new todo",
                on_submit="add_todo",
                autofocus=True
            ),
            ft.Column()
        ]

    def add_todo(self, e):
        if e.control.value:
            self.todos.append(TodoItem(e.control.value))
            e.control.value = ""
            self.controls[-1].controls = self.get_todo_control()
            self.update()
            e.control.focus()

    def toggle_todo(self, e, todo):
        todo.completed = e.control.value
        self.update()


def main(page: ft.Page):
    Router(
        {'todo': TodoModel(page)}
    )
    page.go('todo')


ft.app(target=main)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.