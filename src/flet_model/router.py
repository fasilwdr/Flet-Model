from typing import Dict, Optional, Type
import flet as ft
from .model import Model


class Router:
    """Router class for handling navigation in Flet applications."""

    _instance: Optional['Router'] = None
    _routes: Dict[str, Model] = {}
    _page: Optional[ft.Page] = None
    _view_cache: Dict[str, ft.View] = {}  # Cache for views

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Router, cls).__new__(cls)
        return cls._instance

    def __init__(self, *route_maps: Dict[str, Model]):
        """Initialize the router with route mappings."""
        if not self._routes:
            self._routes = {}
            for route_map in route_maps:
                self._routes.update(route_map)

            if route_maps and list(route_maps[0].values()):
                first_model = list(route_maps[0].values())[0]
                self._page = first_model.page
                self._setup_routing()

    def _setup_routing(self) -> None:
        """Set up route handling and initialize default route."""
        if not self._page:
            return

        self._page.on_route_change = self._handle_route_change
        self._page.on_view_pop = self._handle_view_pop

        if not self._page.route or self._page.route == '/':
            default_route = next(iter(self._routes.keys()))
            self._page.route = default_route
            self._page.go(default_route)

    def _handle_route_change(self, e: ft.RouteChangeEvent) -> None:
        """Handle route changes and update view stack with caching."""
        route_parts = self._page.route.lstrip('/').split('/')
        self._page.views.clear()
        current_route = ''

        for part in route_parts:
            if part:
                current_route = f"{current_route}/{part}" if current_route else part
                if part in self._routes:
                    # Check view cache first
                    if part not in self._view_cache:
                        self._view_cache[part] = self._routes[part].create_view()
                    self._page.views.append(self._view_cache[part])

        self._page.update()

    def _handle_view_pop(self, e: ft.ViewPopEvent) -> None:
        """Handle back navigation."""
        if len(self._page.views) > 1:
            self._page.views.pop()
            routes = self._page.route.split('/')
            routes.pop()
            self._page.go('/'.join(routes))
        self._page.update()

    @classmethod
    def register_route(cls, route: str, model_class: Type[Model]) -> None:
        """Register a new route with its corresponding model class."""
        if cls._instance and cls._instance._page:
            cls._instance._routes[route] = model_class(cls._instance._page)
            # Clear view cache for this route
            if route in cls._instance._view_cache:
                del cls._instance._view_cache[route]

    @classmethod
    def get_current_model(cls) -> Optional[Model]:
        """Get the model instance for the current route."""
        if not (cls._instance and cls._instance._page and cls._instance._page.route):
            return None

        current_route = cls._instance._page.route.split('/')[-1]
        return cls._instance._routes.get(current_route)