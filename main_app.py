from login import LoginView
from register import RegistroView
from clientes import ClientesView
from costos import CostosView
import flet as ft

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Serigrafía"
        self.page.bgcolor = "#bedae7"
        self.page.padding = 40

    def route_change(self, e):
        self.page.views.clear()
        if self.page.route == "/login":
            self.page.views.append(LoginView(self.page).view())
        elif self.page.route == "/registro":
            self.page.views.append(RegistroView(self.page).view())
        elif self.page.route == "/clientes":
            self.page.views.append(ClientesView(self.page).view())
        elif self.page.route == "/costos":
            self.page.views.append(CostosView(self.page).view())
        else:
            self.page.go("/login")
        self.page.update()

    def run(self):
        self.page.on_route_change = self.route_change
        self.page.go("/login")
