import flet as ft


class Control:
    """
    A class to represent a control in a Flet application.

    Attributes:
        flet_control: The actual Flet control instance.
        visible (bool): Whether the control is visible.
        overlay (bool): Whether the control is an overlay.
        dialog (bool): Whether the control is a dialog.
        sequence (int): The sequence number for ordering controls.
    """
    def __init__(self, flet_control, visible: bool = True, overlay: bool = False, dialog: bool = False, sequence: int = 1):
        self.flet_control = flet_control
        self.visible = visible
        self.overlay = overlay
        self.dialog = dialog
        self.sequence = sequence

    def __getattr__(self, item):
        # Delegate attribute access to the actual Flet control
        return getattr(self.flet_control, item)

    def __setattr__(self, key, value):
        if key in ["flet_control", "visible", "overlay", "dialog", "sequence"]:  # Avoid infinite recursion for internal attributes
            super().__setattr__(key, value)
        else:
            setattr(self.flet_control, key, value)


class Model:
    route = None
    back_route = None
    appbar = None
    bottom_appbar = None
    auto_scroll = None
    bgcolor = None
    drawer = None
    end_drawer = None
    fullscreen_dialog = False
    floating_action_button = None
    navigation_bar = None
    horizontal_alignment = ft.CrossAxisAlignment.START
    on_scroll_interval = 10
    on_keyboard_event = None
    padding = 10
    scroll = None
    on_scroll = None
    spacing = 10
    vertical_alignment = ft.MainAxisAlignment.START

    def __init__(self, page):
        self.page = page

    def __post_init__(self):
        self.post_init()

    def on_view_pop(self, e):
        self.page.go(self.back_route)

    def init(self):
        # self.bgcolor = ft.colors.PRIMARY
        pass

    def post_init(self):
        pass

    def create_view(self):
        controls = []
        # Collect all Control instances
        control_instances = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Control):
                control_instances.append(attr)

        # Sort the controls based on their sequence
        sorted_controls = sorted(control_instances, key=lambda x: x.sequence)

        # Add sorted controls to the view
        for control in sorted_controls:
            actual_flet_control = control.flet_control
            for event in ['on_click', 'on_hover', 'on_long_press', 'on_change', 'on_dismiss']:
                if hasattr(actual_flet_control, event):
                    callback_name = getattr(actual_flet_control, event)
                    if isinstance(callback_name, str):
                        method = getattr(self, callback_name, None)
                        if method:
                            setattr(actual_flet_control, event, method)
            if control.visible and not control.overlay and not control.dialog:
                controls.append(actual_flet_control)
            if control.overlay:
                self.page.overlay.append(actual_flet_control)
            if control.dialog:
                self.page.dialog = actual_flet_control
        if self.appbar and self.back_route:
            self.page.on_view_pop = self.on_view_pop
            self.appbar.leading = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: self.page.go(self.back_route))
        if self.on_keyboard_event:
            self.page.on_keyboard_event = None
            self.page.on_keyboard_event = self.on_keyboard_event

        self.init()
        return ft.View(
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
            horizontal_alignment=self.horizontal_alignment,
            on_scroll_interval=self.on_scroll_interval,
            padding=self.padding,
            scroll=self.scroll,
            spacing=self.spacing,
            vertical_alignment=self.vertical_alignment,
            navigation_bar=self.navigation_bar,
            on_scroll=self.on_scroll
        )


def view_model(page):
    # Scan through subclasses of Model to find a matching route
    for cls in Model.__subclasses__():
        if cls.route == page.route:
            return cls(page).create_view()  # Pass the page object to the class
    # If no matching class is found
    raise ValueError("No view available for the given route")