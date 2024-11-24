import pytest
import flet as ft
from flet_model import Model


def test_model_initialization():
    page = ft.Page()

    class TestModel(Model):
        route = "test"
        controls = [ft.Text("Test")]

    model = TestModel(page)
    assert model.route == "test"
    assert len(model.controls) == 1


def test_model_view_creation():
    page = ft.Page()

    class TestModel(Model):
        route = "test"
        controls = [ft.Text("Test")]
        appbar = ft.AppBar(title=ft.Text("Test"))

    model = TestModel(page)
    view = model.create_view()

    assert view.route == "test"
    assert len(view.controls) == 1
    assert isinstance(view.appbar, ft.AppBar)