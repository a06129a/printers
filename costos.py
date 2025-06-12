import flet as ft

class CostosView:
    def __init__(self, page: ft.Page):
        self.page = page

    def label(self, texto):
        return ft.Container(
            content=ft.Text(texto, color="white"),
            bgcolor="#0168ee",
            padding=10,
            border_radius=25,
            width=180
        )

    def view(self):
        # Campos
        varios = lambda: ft.TextField(width=150, border_radius=25)
        inputs = {name: varios() for name in [
            "varios", "material", "pelicula", "tinta", "shablon", "barniz",
            "corte", "troquel", "armado", "troquelado", "doblado", "cinta",
            "horas", "empleados"
        ]}
        mano_obra = ft.TextField(width=200, border_radius=25)
        subtotal = ft.TextField(width=100)
        margen = ft.TextField(width=100)
        total_ventas = ft.TextField(width=100)

        def guardar_datos(e):
            datos = {k: v.value for k, v in inputs.items()}
            datos.update({
                "mano_obra": mano_obra.value,
                "subtotal": subtotal.value,
                "margen": margen.value,
                "total_ventas": total_ventas.value
            })
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Los datos se han guardado correctamente."),
                bgcolor="green",
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

        return ft.View(
            route="/costos",
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Container(
                    padding=20,
                    bgcolor="#51d3f3ea",
                    expand=True,
                    content=ft.Column([
                        ft.Image(src="Printers Serigrafía_ISOLOGOTIPOS_B_Horizontal.png", width=250),
                        ft.Container(
                            bgcolor="#3c6b83", padding=10,
                            content=ft.Text("Costos", size=32, weight="bold", color="black",
                                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))
                        ),
                        ft.Row([self.label("Varios:"), inputs["varios"], self.label("Material:"), inputs["material"]], spacing=10),
                        ft.Row([self.label("Valor Película:"), inputs["pelicula"], self.label("Valor Tinta:"), inputs["tinta"]], spacing=10),
                        ft.Row([self.label("Shablón:"), inputs["shablon"], self.label("Barniz:"), ft.Switch(value=False)], spacing=10),
                        ft.Row([self.label("Valor Corte:"), inputs["corte"], self.label("Valor troquel:"), inputs["troquel"]], spacing=10),
                        ft.Row([self.label("Valor Armado:"), inputs["armado"], self.label("Valor troquelado:"), inputs["troquelado"]], spacing=10),
                        ft.Row([self.label("Valor Doblado:"), inputs["doblado"], self.label("Aplicacion cinta:"), inputs["cinta"]], spacing=10),
                        ft.Row([self.label("Cantidad horas:"), inputs["horas"], self.label("Cant. empleados:"), inputs["empleados"]], spacing=10),
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Valor total de Mano de obra:", color="white", weight="bold"),
                                bgcolor="#1536f1", padding=10, border_radius=25, width=250
                            ), mano_obra
                        ], spacing=10),
                        ft.Divider(),
                        ft.Row([ft.Text("Sub total"), subtotal, ft.Text("(...) c/u"),
                                ft.Text("Margen %"), margen, ft.Text("(...) %")], spacing=10),
                        ft.Row([ft.Text("Total ventas"), total_ventas, ft.Text("(...) c/u")], spacing=10),
                        ft.Row([
                            ft.ElevatedButton("Guardar datos (TEMP)", on_click=guardar_datos),
                            ft.ElevatedButton("Orden pedido", bgcolor="#2e7d78", color="white")
                        ], alignment=ft.MainAxisAlignment.END, spacing=20),
                        ft.Row([
                            ft.ElevatedButton("Atrás", on_click=lambda e: self.page.go("/clientes"),
                                              bgcolor="white", color="black")
                        ], alignment=ft.MainAxisAlignment.START)
                    ], spacing=15)
                )
            ]
        )
