import flet as ft
from main_app import MainApp

def main(page: ft.Page):
    app = MainApp(page)
    app.run()

ft.app(target=main)
