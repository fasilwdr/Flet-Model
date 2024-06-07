# core/base.py
import flet as ft
import inspect


class Model:
    route = None
    controls = []
    back_route = None
    appbar = None
    bottom_appbar = None
    auto_scroll = None
    bgcolor = None
    drawer = None
    end_drawer = None
    fullscreen_dialog = None
    floating_action_button = None
    floating_action_button_location = None
    navigation_bar = None
    horizontal_alignment = ft.CrossAxisAlignment.START
    on_scroll_interval = 10
    on_keyboard_event = None
    padding = 10
    scroll = None
    on_scroll = None
    spacing = 10
    vertical_alignment = ft.MainAxisAlignment.START
    overlay_controls = []

    def __init__(self, page):
        self.page = page

    def on_view_pop(self, e):
        self.page.go(self.back_route)

    def init(self):
        pass

    def post_init(self):
        pass

    def create_view(self):
        controls = self.controls
        if self.overlay_controls:
            for overlay in self.overlay_controls:
                self.page.overlay.append(overlay)
        if self.back_route:
            self.page.on_view_pop = self.on_view_pop
        if self.on_keyboard_event:
            self.page.on_keyboard_event = self.on_keyboard_event

        self.init()

        #Add Overlay Controls to bind event handlers
        controls_to_bind = controls + self.overlay_controls
        # Dynamically bind event handlers
        self.bind_event_handlers(controls_to_bind)

        view = ft.View(
            route=self.route,
            controls=controls,
            appbar=self.appbar,
            bottom_appbar=self.bottom_appbar,
            auto_scroll=self.auto_scroll,
            bgcolor=self.bgcolor,
            drawer=self.drawer,
            end_drawer=self.end_drawer,
            fullscreen_dialog=self.fullscreen_dialog,
            floating_action_button=self.floating_action_button,
            floating_action_button_location=self.floating_action_button_location,
            horizontal_alignment=self.horizontal_alignment,
            on_scroll_interval=self.on_scroll_interval,
            padding=self.padding,
            scroll=self.scroll,
            spacing=self.spacing,
            vertical_alignment=self.vertical_alignment,
            navigation_bar=self.navigation_bar,
            on_scroll=self.on_scroll,
        )
        self.post_init()
        return view

    def bind_event_handlers(self, controls):
        # Event handler attributes to look for
        event_attrs = ['on_click', 'on_hover', 'on_long_press', 'on_change', 'on_dismiss']

        for control in controls:
            for attr in event_attrs:
                if hasattr(control, attr):
                    handler = getattr(control, attr)
                    if isinstance(handler, str) and hasattr(self, handler):
                        # Bind the event handler
                        setattr(control, attr, getattr(self, handler))

            # If the control has nested controls, bind their event handlers too
            if hasattr(control, 'controls'):
                self.bind_event_handlers(control.controls)


def view_model(page):
    # Scan through subclasses of Model to find a matching route
    for cls in Model.__subclasses__():
        if cls.route == page.route:
            return cls(page).create_view()  # Pass the page object to the class
    # If no matching class is found
    raise ValueError("No view available for the given route")
