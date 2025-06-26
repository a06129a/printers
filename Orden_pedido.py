import flet as ft

class OrdenPedidoView:
    def __init__(self, page: ft.Page, documento_cliente):
        self.page = page
        self.documento_cliente=documento_cliente

    def view(self):
        self.page.title = "Orden de pedido"
        self.page.bgcolor = "#1976d2"
        self.page.scroll = "auto"
        self.page.padding = 0

        def texto_bloque(texto, padding_left=60, padding_top=15, margin=None):
            return ft.Container(
                ft.Text(texto, size=17, color="#ffffff"),
                margin=margin if margin else ft.margin.only(left=20),
                padding=ft.padding.only(left=padding_left, top=padding_top),
                width=240,
                height=50,
                bgcolor="#1d4fe0",
                border_radius=ft.BorderRadius(top_left=30, top_right=0, bottom_left=30, bottom_right=0)
            )

        def solo_numeros(e):
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
            self.page.update()

        def solo_numeros_y_barra(e):
            campo = e.control
            campo.value = "".join(c for c in campo.value if c.isdigit() or c == "/")
            self.page.update()

        contenedor = ft.Container(
            content=ft.Text("Orden pedido", color="#ffffff", font_family="Times New Roman", size=30),
            padding=15,
            width=250,
            height=70,
            bgcolor="#122ecc",
            border_radius=ft.BorderRadius(0, 0, 0, 60)
        )

        dato = ft.TextField(bgcolor="#ffffff", on_change=solo_numeros, width=120)
        dato1 = ft.TextField(label="Cliente", bgcolor="#ffffff")
        dato2 = ft.TextField(label="Publicidad", bgcolor="#ffffff")
        dato3 = ft.TextField(label="Trabajo", bgcolor="#ffffff")

        Datos_columnas = ft.Column([
            contenedor,
            ft.Container(content=dato1, width=340, margin=ft.margin.only(left=30)),
            ft.Container(content=dato2, width=340, margin=ft.margin.only(left=30)),
            ft.Container(content=dato3, width=340, margin=ft.margin.only(left=30))
        ], spacing=30)

        columna = ft.Column([
            ft.Row([texto_bloque("Cantidad de pedidos"), dato]),
            ft.Row([texto_bloque("Cantidad Unidad/es"), ft.TextField(bgcolor="#ffffff", on_change=solo_numeros, width=120)])
        ], spacing=20)

        datos_fila = ft.Row([Datos_columnas, columna], spacing=100)

        entry_fila2 = ft.Row([
            texto_bloque("Cantidad de colores", padding_left=14),
            ft.Container(ft.TextField(bgcolor="#ffffff", on_change=solo_numeros, width=120))
        ])

        lista2 = ft.Column([
            texto_bloque("Detalles:", padding_left=60),
            *[ft.Container(ft.TextField(label=f"{i+1}-", bgcolor="#ffffff", width=450), margin=ft.margin.only(left=120)) for i in range(6)]
        ], spacing=10)

        lista3 = ft.Row([
            texto_bloque("Imprecion", padding_left=60),
            ft.Container(ft.TextField(bgcolor="#ffffff", width=320))
        ])

        switch_opcion = ft.Container(
            content=ft.Row([
                ft.Text("Termoformar/Doblar", size=18, color="#ffffff"),
                ft.Switch(value=False),
            ], alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=10
        )

        dropdown = ft.Dropdown(
            label="Selecciona una opción",
            width=200,
            label_style=ft.TextStyle(color="white"),
            options=[ft.dropdown.Option(f"Opción {i+1}") for i in range(3)]
        )

        lista4 = ft.Row([
            texto_bloque("Material", padding_left=60),
            dropdown,
            texto_bloque("Cant. Material", padding_left=40, margin=ft.margin.only(left=400)),
            ft.Container(ft.TextField(bgcolor="#ffffff", on_change=solo_numeros, width=120))
        ])

        lista5 = ft.Row([
            texto_bloque("Med. pliego", padding_left=40),
            ft.Container(ft.TextField(label="Ancho-cm", bgcolor="#ffffff", on_change=solo_numeros, width=120)),
            ft.Container(ft.TextField(label="Alto-cm", bgcolor="#ffffff", on_change=solo_numeros, width=120)),
            texto_bloque("Espesor", padding_left=70, margin=ft.margin.only(left=350)),
            ft.Container(ft.TextField(bgcolor="#ffffff", on_change=solo_numeros, width=120))
        ])

        lista6 = ft.Row([
            *[
                ft.Container(ft.Row([
                    ft.Text(texto, size=18, color="#ffffff"),
                    ft.Switch(value=False)
                ]), padding=10) for texto in ["Troquelado", "Doblado", "Corte"]
            ],
            ft.Row([
                texto_bloque("Cinta bifaz", padding_left=60),
                ft.Dropdown(label="Selecciona una opción", width=200, label_style=ft.TextStyle(color="white"), options=[ft.dropdown.Option(f"Opción {i+1}") for i in range(3)])
            ])
        ], spacing=80)

        datos_fila2 = ft.Row([
            texto_bloque("Observaciones", padding_left=40),
            ft.Container(ft.TextField(bgcolor="#ffffff", multiline=True, max_lines=4, hint_text="Escribe aquí todos los detalles..."), width=600)
        ], alignment=ft.MainAxisAlignment.CENTER)

        lista7 = ft.Row([
            ft.Row([texto_bloque("Fecha recepcion", padding_left=40), ft.Container(ft.TextField(bgcolor="#ffffff", on_change=solo_numeros_y_barra, width=120))]),
            ft.Row([texto_bloque("Fecha entrega", padding_left=50), ft.Container(ft.TextField(bgcolor="#ffffff", on_change=solo_numeros_y_barra, width=120))])
        ], spacing=500)

        lista8 = ft.Row([
            texto_bloque("Firma", padding_left=60, margin=ft.margin.only(bottom=40)),
            ft.Container(
                bgcolor="#1976d2",
                content=ft.Row([
                    texto_bloque("Imprimio", padding_left=50, margin=ft.margin.only(bottom=40)),
                    ft.Container(ft.TextField(bgcolor="#ffffff", width=200), margin=ft.margin.only(bottom=40))
                ]),
            ),
            ft.Container(
                bgcolor="#1976d2",
                content=ft.Row([
                    texto_bloque("Cant. Impresa", padding_left=40, margin=ft.margin.only(bottom=40)),
                    ft.Container(ft.TextField(bgcolor="#ffffff", on_change=solo_numeros, width=120), margin=ft.margin.only(bottom=40))
                ])
            ),
        ], spacing=110)

        botones_finales = ft.Row([
            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/costos"), bgcolor="white"),
            ft.ElevatedButton("Guardar Pedido", bgcolor="green", color="white"),
            ft.ElevatedButton("Cancelar", on_click=lambda e: self.page.go("/clientes"), bgcolor="red", color="white"),
        ], alignment=ft.MainAxisAlignment.END)

        separador = ft.Divider(color=ft.Colors.BLUE_GREY_200)

        return ft.View(
            route="/orden_pedido",
            scroll=ft.ScrollMode.ALWAYS,
            bgcolor="#1976d2",
            controls=[
                ft.Column([
                    datos_fila, separador, entry_fila2, lista2, lista3, switch_opcion,
                    separador, lista4, lista5, lista6, datos_fila2, separador,
                    lista7, lista8, botones_finales
                ])
            ]
        )
