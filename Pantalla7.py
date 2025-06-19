import flet as ft

class Pantalla7View:
    def __init__(self, page: ft.Page, documento_cliente):
        self.page = page
        self.documento_cliente = str(documento_cliente)  # Convertir a cadena de texto

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
            border_color="white"
        )

    def fila_tabla(self, *texts):
        return ft.DataRow(cells=[ft.DataCell(ft.Text(str(t), color="white")) for t in texts])

    def seccion_titulo(self, titulo):
        return ft.Text(titulo, size=26, weight="bold", color="white")

    def divisor(self):
        return ft.Container(height=20)

    def view(self):
        self.page.title = "Costo Producción"
        self.page.scroll = "auto"
        self.page.bgcolor = "#002591"

        logo = ft.Image(src="imagenes\\Printers.png", width=150, height=75, fit=ft.ImageFit.CONTAIN)
        btn_clientes = ft.ElevatedButton("Clientes", bgcolor="white")
        btn_crear = ft.ElevatedButton("Crear", bgcolor="white")
        avatar = ft.Icon(name="account_circle", size=40, color="black")

        header = ft.Row(
            controls=[logo, ft.Container(expand=True), btn_clientes, btn_crear, avatar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        contenido = ft.Container(
            content=ft.Column([
                ft.Text("Costo Producción", size=30, weight="bold", color="white"),

                ft.Row([
                    self.texto_bloque("Tipo Cambio"),
                    self.entrada("120,00", 100)
                ]),

                self.divisor(),
                self.seccion_titulo("Costo Material"),

                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Material", color="white")),
                        ft.DataColumn(ft.Text("P.E", color="white")),
                        ft.DataColumn(ft.Text("Kg ($)", color="white")),
                        ft.DataColumn(ft.Text("Peso", color="white")),
                        ft.DataColumn(ft.Text("Total Kg.", color="white")),
                        ft.DataColumn(ft.Text("Costo final", color="white")),
                    ],
                    rows=[
                        self.fila_tabla("PVC", "1,40", "18,00", "0,000", "0,000", "$0"),
                        self.fila_tabla("PET", "0,88", "0,00", "0,000", "0,000", "$0"),
                    ]
                ),

                self.divisor(),
                self.seccion_titulo("Costo Película"),

                ft.Row([
                    self.texto_bloque("Superficie"),
                    self.entrada("0", 60),
                    ft.Text("x $/m2:", color="white"),
                    self.entrada("7,00", 60),
                    ft.Text("= Costo x uni:", color="white"),
                    self.entrada("0,00", 80),
                ], spacing=10),

                self.divisor(),
                self.seccion_titulo("Costo Impresión"),

                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Tipo Impresion", color="white")),
                        ft.DataColumn(ft.Text("Cant. Color", color="white")),
                        ft.DataColumn(ft.Text("Pliegos", color="white")),
                        ft.DataColumn(ft.Text("$ x Pasada", color="white")),
                        ft.DataColumn(ft.Text("Costo Min.", color="white")),
                        ft.DataColumn(ft.Text("Costo final", color="white")),
                    ],
                    rows=[
                        self.fila_tabla("Convencional", "0", "0", "15,00", "40,00", "$0"),
                        self.fila_tabla("UV", "0", "0", "20,00", "60,00", "$0"),
                    ]
                ),

                self.divisor(),
                self.seccion_titulo("Costo Tinta"),

                ft.Row([
                    self.texto_bloque("Sup. Total"),
                    self.entrada("70", 60),
                    ft.Text("Tinta Rinde:", color="white"),
                    self.entrada("60%", 60),
                    ft.Text("Caras:", color="white"),
                    self.entrada("2", 40),
                ], spacing=10),

                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Impresión", color="white")),
                        ft.DataColumn(ft.Text("$ x Lt.", color="white")),
                        ft.DataColumn(ft.Text("Costo final", color="white")),
                    ],
                    rows=[
                        self.fila_tabla("Convencional", "33000,00", "$0"),
                        self.fila_tabla("UV", "60000,00", "$0"),
                    ]
                ),

                self.divisor(),
                self.seccion_titulo("Costo Barniz"),

                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Impresión", color="white")),
                        ft.DataColumn(ft.Text("u$S x Lt", color="white")),
                        ft.DataColumn(ft.Text("$ x Lt", color="white")),
                        ft.DataColumn(ft.Text("Costo final por cm", color="white")),
                    ],
                    rows=[
                        self.fila_tabla("Convencional", "18", "1800,00", "$0"),
                        self.fila_tabla("UV", "45", "4500,00", "$0"),
                    ]
                ),

                self.divisor(),

                ft.Row([
                    ft.ElevatedButton("Atrás", bgcolor="#ffffff", height=40, width=150, on_click=lambda e: self.page.go("/pantalla6?documento_cliente=" + self.documento_cliente)),
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