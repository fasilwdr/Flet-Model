
# Flet Model

This repository contains a simple Flet application demonstrating a basic structure and usage of the Flet framework.

## Repository Structure

```plaintext
Flet-Model/
├── assets
│   └── icon.png
├── core
│   └── base.py
├── views
│   └── main_view.py  (Add add all flet views here)
├── main.py
└── manifest.json
```

### File Descriptions

- **assets/icon.png**: Placeholder for assets like icons and images.
- **core/base.py**: Contains the core classes and logic for the application.
- **views/main_view.py**: Example view demonstrating the usage of the `Model` and `Control` classes.
- **main.py**: Entry point for the Flet application, handling routing and initial setup.
- **manifest.json**: Configuration file specifying application metadata and views.

## Main Components

### main.py

This is the entry point of the application. It loads the configuration from `manifest.json`, dynamically imports the required modules, and sets up the routing and error handling.

### core/base.py

Defines the `Control` and `Model` classes which are used to represent UI components and views in the application.

- **Control**: Wrapper for Flet controls with additional properties.
- **Model**: Base class for creating views. It handles the creation and arrangement of `Control` instances.

### views/main_view.py

An example view demonstrating how to use the `Model` and `Control` classes.

```python
#main_view
import flet as ft
from core.base import Model, Control

class MainView(Model):
    route = '/'

    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                ]
            ),
        ],
    )

    name = Control(ft.TextField(label="Name"), sequence=1)
    age = Control(ft.TextField(label="Age", keyboard_type=ft.KeyboardType.NUMBER), sequence=2)
    submit_button = Control(ft.ElevatedButton(text="Submit", on_click="on_click_submit"), sequence=3)

    def on_click_submit(self, e):
        print("Submitted")
```

## Features
- can be use for string for assign action in Control class
- 


## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/fasilwdr/Flet-Model.git
   cd Flet-Model
   ```
   - Create views under views folder and map it into manifest.json
   ```json
   {
     "name": "Flet App",
     "short_name": "Flet App",
     "version": "1.0.1",
     "views": [
       "views/main_view.py",
       "views/second_view.py"
      ]
   }
   ```

2. Install the required dependencies:
   ```bash
   pip install flet
   ```

3. Run the application:
   ```bash
   flet main.py
   ```

The application should start, and you will see a simple form with fields for Name and Age, and a Submit button.

## License

This project is licensed under the MIT License.
