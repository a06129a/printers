from login import LoginView
from register import RegistroView
from clientes import ClientesView
from costos import CostosView
from Pantalla6 import Pantalla6View
from Pantalla7 import PantallaCostos
from Orden_pedido import OrdenPedidoView
import flet as ft

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Serigrafía"
        self.page.bgcolor = "#bedae7"
        self.page.padding = 40

    async def route_change(self, e):
        if self.page.route == "/login":
            nueva_vista = LoginView(self.page).view()
        elif self.page.route == "/registro":
            nueva_vista = RegistroView(self.page).view()
        elif self.page.route == "/clientes":
            nueva_vista = ClientesView(self.page).view()
        elif self.page.route == "/pantalla6":
            documento = await self.page.shared_preferences.get("documento_cliente")
            nueva_vista = Pantalla6View(self.page, documento).view()
        elif self.page.route == "/pantalla7":
            documento = await self.page.shared_preferences.get("documento_cliente")
            nueva_vista = PantallaCostos(self.page, documento).view()
        elif self.page.route == "/costos":
            documento = await self.page.shared_preferences.get("documento_cliente")
            nueva_vista = CostosView(self.page, documento).view()
        elif self.page.route == "/orden_pedido":
            documento = await self.page.shared_preferences.get("documento_cliente")
            nueva_vista = OrdenPedidoView(self.page, documento).view()
        else:
            self.page.go("/login")
            return

        self.page.views.clear()
        self.page.views.append(nueva_vista)
        self.page.update()

    def run(self):
        self.page.on_route_change = self.route_change
        self.page.go("/login")
