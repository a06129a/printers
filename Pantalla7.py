import flet as ft
import sqlite3
from conexion_bd import get_connection

DENSIDADES = {
    "PVC": 1.40,
    "PAI": 1.10,
    "PET": 0.98,
    "Polipropileno": 1.00
}

class Pantalla7View:
    def __init__(self, page: ft.Page, documento_cliente):
        self.page = page
        self.documento_cliente = documento_cliente

        # Traer volumen y superficie desde storage
        self.volumen = float(self.page.client_storage.get("cinta_volumen") or 0)
        self.superficie = float(self.page.client_storage.get("unidad_superficie") or 0)

        # Conexión BD
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Inputs para cada material
        self.input_precio_pvc = self.entrada("18.00", 120)
        self.input_precio_pai = self.entrada("0.00", 120)
        self.input_precio_pet = self.entrada("0.00", 120)
        self.input_precio_pp = self.entrada("0.00", 120)

        self.tabla_materiales = self.crear_tabla_materiales()

    def texto_bloque(self, label):
        return ft.Container(
            content=ft.Text(label, color="white", size=14, weight="bold"),
            padding=10,
            bgcolor="#1d4fe0",
            border_radius=ft.BorderRadius(top_left=20, top_right=0, bottom_left=20, bottom_right=0)
        )

    def entrada(self, valor, ancho):
        return ft.TextField(
            value=valor,
            width=ancho,
            text_align="right",
            color="white",
            bgcolor="#1e3a8a",
            border_color="white",
            on_change=self.actualizar_costos
        )

    def fila_tabla(self, material, pe, input_precio):
        peso_total = self.volumen * DENSIDADES[material]
        precio_kg = float(input_precio.value.replace(",", ".") or 0)
        costo_final = peso_total * precio_kg

        return ft.DataRow(cells=[
            ft.DataCell(ft.Text(material, color="white")),
            ft.DataCell(ft.Text(f"{DENSIDADES[material]:.2f}", color="white")),
            ft.DataCell(input_precio),
            ft.DataCell(ft.Text(f"{peso_total:.3f} kg", color="white")),
            ft.DataCell(ft.Text(f"{peso_total:.3f} kg", color="white")),
            ft.DataCell(ft.Text(f"${costo_final:.2f}", color="white"))
        ])

    def actualizar_costos(self, e):
        # reconstruir la tabla con nuevos valores
        self.tabla_materiales = self.crear_tabla_materiales()
        # la tabla está en controls[2] de contenido
        self.page.views[-1].controls[2].content.controls[2] = self.tabla_materiales
        self.page.update()

    def crear_tabla_materiales(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Material", color="white")),
                ft.DataColumn(ft.Text("P.E", color="white")),
                ft.DataColumn(ft.Text("Kg ($)", color="white")),
                ft.DataColumn(ft.Text("Peso", color="white")),
                ft.DataColumn(ft.Text("Total Kg.", color="white")),
                ft.DataColumn(ft.Text("Costo final", color="white")),
            ],
            rows=[
                self.fila_tabla("PVC", DENSIDADES["PVC"], self.input_precio_pvc),
                self.fila_tabla("PAI", DENSIDADES["PAI"], self.input_precio_pai),
                self.fila_tabla("PET", DENSIDADES["PET"], self.input_precio_pet),
                self.fila_tabla("Polipropileno", DENSIDADES["Polipropileno"], self.input_precio_pp)
            ]
        )

    def guardar_en_bd(self, e):
        try:
            for material, input_precio in [
                ("PVC", self.input_precio_pvc),
                ("PAI", self.input_precio_pai),
                ("PET", self.input_precio_pet),
                ("Polipropileno", self.input_precio_pp)
            ]:
                precio_kg = float(input_precio.value.replace(",", ".") or 0)
                densidad = DENSIDADES[material]
                peso_total = self.volumen * densidad
                precio_total = peso_total * precio_kg

                if precio_kg > 0:  # Guardar solo si se ingresó precio
                    self.cursor.execute("""
                        INSERT INTO Materiales (documento_cliente, material, volumen, superficie, densidad, peso_total, precio_kg, precio_total)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        self.documento_cliente,
                        material,
                        self.volumen,
                        self.superficie,
                        densidad,
                        peso_total,
                        precio_kg,
                        precio_total
                    ))

            self.conn.commit()
            print("Datos guardados en Materiales.")

        except Exception as ex:
            print("Error al guardar en BD:", ex)

    def view(self):
        self.page.title = "Costo Producción"
        self.page.scroll = "auto"
        self.page.bgcolor = "#002591"

        logo = ft.Image(src="imagenes\\Printers.png", width=150, height=75, fit=ft.ImageFit.CONTAIN)

        header = ft.Row(
            controls=[
                logo,
                ft.Container(expand=True),
                ft.ElevatedButton("Clientes", bgcolor="white", on_click=lambda e: self.page.go("/clientes")),
                ft.ElevatedButton("Crear", bgcolor="white", on_click=self.guardar_en_bd),
                ft.Icon(name="account_circle", size=40, color="black")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        contenido = ft.Container(
            content=ft.Column([
                ft.Text("Costo Producción", size=30, weight="bold", color="white"),

                ft.Row([
                    self.texto_bloque("Tipo Cambio"),
                    self.entrada("120,00", 100)
                ]),

                self.seccion_titulo("Costo Material"),

                self.tabla_materiales,

                ft.Row([
                    ft.ElevatedButton("Atrás", bgcolor="#ffffff", height=40, width=150, on_click=lambda e: self.page.go("/pantalla6")),
                    ft.ElevatedButton("Siguiente", bgcolor="#ffffff", height=40, width=150, on_click=lambda e: self.page.go("/costos")),
                ], alignment=ft.MainAxisAlignment.END)

            ]),
            padding=20
        )

        return ft.View(
            route="/pantalla7",
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                header,
                ft.Divider(color="white"),
                contenido
            ]
        )

    def seccion_titulo(self, titulo):
        return ft.Text(titulo, size=26, weight="bold", color="white")
