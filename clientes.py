import flet as ft

class ClientesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.clientes = [
            {"nombre": "Pablo Nievas", "documento": "12345678", "fecha": "17/6/25"},
            {"nombre": "Juliana Rodriguez", "documento": "23456789", "fecha": "17/6/25"},
            {"nombre": "Roberto Mariano", "documento": "34567890", "fecha": "17/6/25"}
        ]
        self.lista_clientes = ft.Column(scroll=ft.ScrollMode.ALWAYS)
        self.mensaje = ft.Text(value="", color="green", size=14)

    def view(self):
        nombre_input = ft.TextField(label="Nombre", width=200)
        documento_input = ft.TextField(label="Documento", width=200)
        fecha_input = ft.TextField(label="Fecha de entrega (dd/mm/yy)", width=200)

        def render_clientes():
            self.lista_clientes.controls.clear()
            for c in self.clientes:
                self.lista_clientes.controls.append(
                    ft.Row([
                        ft.Text(c["nombre"], weight="bold", color="white"),
                        ft.Text(f"Doc: {c['documento']}", color="white"),
                        ft.Text(f"Entrega: {c['fecha']}", color="white"),
                        ft.ElevatedButton("Modificar", on_click=lambda e: self.page.go("/costos"))
                    ])
                )
            self.page.update()

        def agregar_cliente(e):
            if nombre_input.value and documento_input.value and fecha_input.value:
                self.clientes.append({
                    "nombre": nombre_input.value,
                    "documento": documento_input.value,
                    "fecha": fecha_input.value
                })
                nombre_input.value = ""
                documento_input.value = ""
                fecha_input.value = ""
                self.mensaje.value = "Cliente agregado"
                self.mensaje.color = "green"
                render_clientes()
            else:
                self.mensaje.value = "Completa todos los campos"
                self.mensaje.color = "red"
            self.page.update()

        render_clientes()

        return ft.View(
            route="/clientes",
            bgcolor="#0d47a1",
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Image(src="Printers Serigrafía_ISOLOGOTIPOS_B_Horizontal.png", width=250),
                        ft.Text("Gestión de Clientes", size=28, weight="bold", color="white"),
                        ft.Row([
                            nombre_input, documento_input, fecha_input,
                            ft.ElevatedButton("Agregar", on_click=agregar_cliente),
                            ft.ElevatedButton("Borrar", on_click=lambda e: print("Borrar cliente"), bgcolor="red", color="white")
                        ], spacing=10),
                        self.mensaje,
                        ft.Divider(color="white"),
                        self.lista_clientes,
                        ft.Divider(),
                        ft.Row([
                            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/login"))
                        ], alignment=ft.MainAxisAlignment.END, spacing=20)
                    ])
                )
            ]
        )
