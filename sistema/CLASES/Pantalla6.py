import flet as ft
import os
import sys
from conexion_bd import get_connection

class Pantalla6View:
    def __init__(self, page: ft.Page):
        self.page = page

    def texto_bloque(self, texto, padding_left=14):
        return ft.Container(
            content=ft.Text(value=texto, color="white", size=16),
            padding=ft.padding.only(left=padding_left, top=10),
            width=180,
            height=40,
            bgcolor="#1d4fe0",
            border_radius=ft.BorderRadius(top_left=20, top_right=0, bottom_left=20, bottom_right=0)
        )

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def view(self):
        logo = ft.Image(src=self.resource_path("imagen/Printers_Serigrafía_ISOLOGOTIPOS_B_Horizontal.png"), width=150, height=75, fit=ft.ImageFit.CONTAIN)
        header = ft.Row([
            logo,
            ft.Container(expand=True),
            ft.ElevatedButton("Clientes", bgcolor="white"),
            ft.ElevatedButton("Crear", bgcolor="white"),
            ft.Icon(name="account_circle", size=40, color="black"),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        datos_pliego = ft.Container(
            content=ft.Column([
                ft.Text("Datos de pliego", weight="bold", italic=True, color="white", size=18),
                ft.Row([
                    ft.Column([
                        ft.Row([self.texto_bloque("Unidades"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Cinta CM"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Espesor"), ft.TextField(width=200)]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Postura"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Superficie"), ft.TextField(width=200)]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Ancho (cm)"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Largo (cm)"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Volumen"), ft.TextField(width=200)]),
                    ]),
                ], spacing=30)
            ])
        )

        impresion = ft.Container(
            content=ft.Column([
                ft.Text("Impresión", weight="bold", italic=True, color="white", size=18),
                ft.Row([
                    ft.Column([
                        ft.Row([self.texto_bloque("Cant. Colores"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Pliegos"), ft.Dropdown(width=200, options=[])]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Colores"), ft.TextField(width=200)]),
                        ft.Row([self.texto_bloque("Pasadas"), ft.TextField(width=200)]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Barniz"), ft.Dropdown(width=200, options=[])]),
                    ])
                ], spacing=30)
            ])
        )

        return ft.View(
            route="/pantalla6",
            controls=[
                header,
                ft.Divider(color="white"),
                datos_pliego,
                ft.Divider(color="white"),
                impresion,
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton("Anterior", bgcolor="white", height=40, width=150, on_click=lambda e: self.page.go("/clientes")),
                        ft.ElevatedButton("Siguiente", bgcolor="white", height=40, width=150, on_click=lambda e: self.page.go("/pantalla7")),
                    ], alignment=ft.MainAxisAlignment.END),
                    padding=ft.padding.only(top=120),
                )
            ],
            bgcolor="#002591"
        )
