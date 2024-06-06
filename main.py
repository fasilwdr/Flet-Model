import flet as ft
from core.base import view_model
import json

pattern = r'^[A-Z0-9!@#$%^&*()-_=+\\\[\]{}|;:\'",.<>/?]*$'

# Load and parse the config.json
with open('manifest.json', 'r') as file:
    manifest = json.load(file)

# Dynamically import the module
for addon_path in manifest['views']:
    module_name = addon_path.split('.')[0].replace('/', '.')
    __import__(module_name)


def main(page: ft.Page):
    def on_error_page(e):
        if page.route != '/':
            page.go('/')
        else:
            page.client_storage.clear()
            page.update()
            page.go('/')

    def on_route_change(e):
        page.views.clear()
        # Use view_model from the dynamically imported modules
        page.views.append(view_model(page))
        page.update()
    page.data = {
        'manifest': manifest
    }
    page.title = manifest.get('name', False) or 'Flet App'
    page.on_route_change = on_route_change
    # page.on_error = on_error_page
    if manifest.get('default_theme_mode'):
        page.theme_mode = manifest.get('default_theme_mode')
    if manifest.get('color_scheme_seed'):
        page.theme = ft.theme.Theme(color_scheme_seed=manifest.get('color_scheme_seed'))
    page.scroll = ft.ScrollMode.AUTO
    if not page.client_storage.get("manifest"):
        page.route = '/login'
    page.go(page.route)


ft.app(target=main, assets_dir='assets')
