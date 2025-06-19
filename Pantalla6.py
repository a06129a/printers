import flet as ft
import re
import os
import sys
from conexion_bd import get_connection
from Pantalla7 import Pantalla7View

class Pantalla6View:
    def __init__(self, page: ft.Page, documento_cliente):
        self.page = page
        self.documento_cliente = documento_cliente
        self.page.bgcolor = "#002591"
        self.page.scroll = ft.ScrollMode.AUTO
        self.contenedor_pagina = ft.Container()  # Inicializar el atributo aquí
        self.crear_controles()
        self.armar_vista()

    def view(self):
        return ft.View(
            route="/pantalla6",
            controls=[
                self.contenedor_pagina  # asegurate que este atributo esté definido
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor="#002591"
        )

    def crear_controles(self):
        self.unidades_input = ft.TextField(width=200, on_change=self.validar_numeros)
        self.cinta_input = ft.TextField(width=200, on_change=self.validar_numeros)
        self.espesor_input = ft.TextField(width=200, on_change=self.ajustar_y_actualizar)
        self.postura_input = ft.TextField(width=200, on_change=self.validar_numeros)
        self.superficie_input = ft.TextField(width=200, read_only=True, bgcolor="#a3c9f1")
        self.ancho_input = ft.TextField(width=200, on_change=self.ajustar_y_actualizar)
        self.largo_input = ft.TextField(width=200, on_change=self.ajustar_y_actualizar)
        self.volumen_input = ft.TextField(width=200, read_only=True, bgcolor="#a3c9f1")

        self.cant_colores_input = ft.TextField(width=200, on_change=self.validar_numeros)
        self.colores_input = ft.TextField(width=200)
        self.pasadas_input = ft.TextField(width=200, on_change=self.validar_numeros)
        self.barniz_dropdown = ft.Dropdown(width=200, options=[ft.dropdown.Option("Si"), ft.dropdown.Option("No")], bgcolor="#ffffff")
        self.pliegos_dropdown = ft.Dropdown(width=200, options=[ft.dropdown.Option("Si"), ft.dropdown.Option("No")], bgcolor="#ffffff")

    def validar_numeros(self, e):
        valor = e.control.value
        e.control.value = re.sub(r"[^0-9.]", "", valor)
        self.page.update()

    def ajustar_y_actualizar(self, e):
        self.validar_numeros(e)
        self.actualizar()

    def actualizar(self):
        try:
            ancho = float(self.ancho_input.value or 0)
            largo = float(self.largo_input.value or 0)
            espesor = float(self.espesor_input.value or 0)
            superficie = ancho * largo
            volumen = superficie * espesor
            self.superficie_input.value = f"{superficie:.2f}"
            self.volumen_input.value = f"{volumen:.2f}"
            self.page.update()
        except:
            pass

    def guardar_datos(self, e):
        self.actualizar()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO Pliegues (
                    Documento, Pliego_Ancho, Unidad_Largo, Unidad_Superficie,
                    Cinta_Espesor, Cinta_Volumen, Pliego_Posturas, Cinta_CM,
                    Impre_Cant_Color, Impre_Colores, Impre_Pliegos,
                    Impre_Pasadas, Impre_Barniz
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.documento_cliente,
                float(self.ancho_input.value or 0),
                float(self.largo_input.value or 0),
                float(self.superficie_input.value or 0),
                float(self.espesor_input.value or 0),
                float(self.volumen_input.value or 0),
                int(self.postura_input.value or 0),
                float(self.cinta_input.value or 0),
                int(self.cant_colores_input.value or 0),
                self.colores_input.value or "",
                1 if self.pliegos_dropdown.value == "Si" else 0,
                int(self.pasadas_input.value or 0),
                1 if self.barniz_dropdown.value == "Si" else 0
            ))
            conn.commit()
            conn.close()
            self.page.go("/pantalla7?documento_cliente=" + self.documento_cliente)
        except Exception as ex:
            print("Error al guardar presupuesto:", ex)

    def volver_atras(self, e):
        self.page.go("/clientes")

    def armar_vista(self):
        logo = ft.Image(src=self.resource_path("imagen/Printers_Serigrafía_ISOLOGOTIPOS_B_Horizontal.png"), width=150, height=75, fit=ft.ImageFit.CONTAIN)
        btn_clientes = ft.ElevatedButton("Clientes", bgcolor="white")
        btn_crear = ft.ElevatedButton("Crear", bgcolor="white")
        avatar = ft.Icon(name="account_circle", size=40, color="black")

        header = ft.Row(
            controls=[logo, ft.Container(expand=True), btn_clientes, btn_crear, avatar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        datos_pliego = ft.Container(
            content=ft.Column([
                ft.Text("Datos de pliego", weight="bold", italic=True, color="white", size=18),
                ft.Row([
                    ft.Column([
                        ft.Row([self.texto_bloque("Unidades"), self.unidades_input]),
                        ft.Row([self.texto_bloque("Cinta CM"), self.cinta_input]),
                        ft.Row([self.texto_bloque("Espesor"), self.espesor_input]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Postura"), self.postura_input]),
                        ft.Row([self.texto_bloque("Superficie"), self.superficie_input]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Ancho (cm)"), self.ancho_input]),
                        ft.Row([self.texto_bloque("Largo (cm)"), self.largo_input]),
                        ft.Row([self.texto_bloque("Volumen"), self.volumen_input]),
                    ]),
                ], spacing=30)
            ])
        )

        impresion = ft.Container(
            content=ft.Column([
                ft.Text("Impresión", weight="bold", italic=True, color="white", size=18),
                ft.Row([
                    ft.Column([
                        ft.Row([self.texto_bloque("Cant. Colores"), self.cant_colores_input]),
                        ft.Row([self.texto_bloque("Pliegos"), self.pliegos_dropdown]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Colores"), self.colores_input]),
                        ft.Row([self.texto_bloque("Pasadas"), self.pasadas_input]),
                    ]),
                    ft.Column([
                        ft.Row([self.texto_bloque("Barniz"), self.barniz_dropdown]),
                    ])
                ], spacing=30)
            ])
        )

        botones = ft.Row([
            ft.ElevatedButton("Anterior", bgcolor="white", height=40, width=150, on_click=self.volver_atras),
            ft.ElevatedButton("Siguiente", bgcolor="white", height=40, width=150, on_click=self.guardar_datos)
        ], alignment=ft.MainAxisAlignment.END)

        self.contenedor_pagina.content = ft.Column([
            header,
            ft.Divider(color="white"),
            datos_pliego,
            ft.Divider(color="white"),
            impresion,
            ft.Container(content=botones, padding=ft.padding.only(top=120))
        ])

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