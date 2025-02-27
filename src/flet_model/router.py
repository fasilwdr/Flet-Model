from typing import Dict, Optional, Type, Any, Callable, TypeVar, List, Tuple
import urllib.parse
import flet as ft
from .model import Model

# Type variable for decorator return type annotation
T = TypeVar('T', bound=Type[Model])

# Global storage for route registrations
_pending_registrations: List[Tuple[str, Type[Model]]] = []


def route(route_path: str) -> Callable[[T], T]:
    """
    Decorator for registering a model class with a specific route.

    Example:
        @route('todo')
        class TodoModel(Model):
            # model implementation

    Args:
        route_path: The route path to register

    Returns:
        The decorated model class
    """

    def decorator(model_class: T) -> T:
        if not issubclass(model_class, Model):
            raise TypeError(f"Class {model_class.__name__} must inherit from Model")

        # Store the route in the class for reference
        model_class.route = route_path

        # Save for deferred registration
        _pending_registrations.append((route_path, model_class))
        return model_class

    return decorator


class Router:
    """Router class for handling navigation in Flet applications."""

    _instance: Optional['Router'] = None
    _routes: Dict[str, Model] = {}
    _page: Optional[ft.Page] = None
    _view_cache: Dict[str, ft.View] = {}
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Router, cls).__new__(cls)
        return cls._instance

    def __init__(self, *route_maps: Dict[str, Model]):
        if self._initialized:
            return

        self._routes = {}

        # Add any routes from explicit dictionaries
        for route_map in route_maps:
            self._routes.update(route_map)

        # If we have routes and a page from dict-based initialization
        if route_maps and list(route_maps[0].values()):
            first_model = list(route_maps[0].values())[0]
            self._page = first_model.page
            self._setup_routing()
            self._initialized = True

    def _parse_route_and_hash(self, route: str) -> tuple[list[str], dict[str, dict]]:
        parts = route.split('/')
        route_parts = []
        hash_data = {}

        for part in parts:
            if not part:
                continue
            if '#' in part:
                route_part, hash_part = part.split('#', 1)
                route_parts.append(route_part)
                # Parse hash data (e.g., "id=3" becomes {"id": "3"})
                params = urllib.parse.parse_qs(hash_part)
                hash_data[route_part] = {k: v[0] for k, v in params.items()}
            else:
                route_parts.append(part)

        return route_parts, hash_data

    def _setup_routing(self) -> None:
        """Set up route handling and initialize default route."""
        if not self._page:
            return

        self._page.on_route_change = self._handle_route_change
        self._page.on_view_pop = self._handle_view_pop

    def _handle_route_change(self, e: ft.RouteChangeEvent) -> None:
        route_parts, hash_data = self._parse_route_and_hash(self._page.route.lstrip('/'))
        self._page.views.clear()
        current_route = ''

        for part in route_parts:
            if part in self._routes:
                current_route = f"{current_route}/{part}" if current_route else part
                model = self._routes[part]

                # Set route data if available
                model.route_data = hash_data.get(part, {})

                if part not in self._view_cache:
                    self._view_cache[part] = model.create_view()
                self._page.views.append(self._view_cache[part])

        self._page.update()

    def _handle_view_pop(self, e: ft.ViewPopEvent) -> None:
        if len(self._page.views) > 1:
            self._page.views.pop()
            route_parts = self._page.route.split('/')
            route_parts.pop()
            self._page.go('/'.join(route_parts))
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

    # Auto-initialize with the page when app starts
    @classmethod
    def initialize(cls, page: ft.Page) -> None:
        """
        Initialize the router with a page and register any pending routes.
        This also sets up the route handlers.

        Args:
            page: The flet Page instance
        """
        global _pending_registrations

        # Create instance if it doesn't exist
        if not cls._instance:
            cls._instance = cls()

        cls._instance._page = page
        cls._instance._initialized = True

        # Register any routes that were decorated
        for route_path, model_class in _pending_registrations:
            model_instance = model_class(page)
            cls._instance._routes[route_path] = model_instance

        # Clear pending registrations
        _pending_registrations = []

        # Setup routing
        cls._instance._setup_routing()

        # Return the instance for method chaining if needed
        return cls._instance

    @classmethod
    def navigate(cls, route: str) -> None:
        """
        Navigate to a specific route, ensuring the router is initialized first.

        Args:
            route: The route to navigate to
        """
        if cls._instance and cls._instance._page:
            cls._instance._page.go(route)


# Modify flet.Page to inject our router
def enhanced_page_go(self, route, *args, **kwargs):
    """Enhanced go method that ensures router is initialized before navigation"""
    # Initialize router if there are pending routes
    if _pending_registrations and not Router._instance:
        Router.initialize(self)
    # Call the original go method
    original_go(self, route, *args, **kwargs)


# Store original method and apply patch
original_go = ft.Page.go
ft.Page.go = enhanced_page_go