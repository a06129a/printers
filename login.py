import flet as ft

class LoginView:
    def __init__(self, page):
        self.page = page
        self.mensaje = ft.Text(value="", size=14)

    def view(self):
        usuario = ft.TextField(label="Usuario", border_radius=8, bgcolor="black", width=300)
        contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=8, bgcolor="black", width=300)

        def on_login(e):
            if not usuario.value.strip() and not contraseña.value.strip():
                self.mensaje.value = "No introdujiste el usuario ni la contraseña"
                self.mensaje.color = "red"
            elif not usuario.value.strip():
                self.mensaje.value = "No introdujiste el usuario"
                self.mensaje.color = "red"
            elif not contraseña.value.strip():
                self.mensaje.value = "No introdujiste la contraseña"
                self.mensaje.color = "red"
            else:
                self.page.go("/clientes")
                return  
            self.page.update()

        return ft.View(
            route="/login",
            controls=[
                ft.Container(
                    width=400,
                    padding=30,
                    bgcolor="blue",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=12, color="#6590EC68"),
                    content=ft.Column(
                        [
                            ft.Image(src="Printers Serigrafía_ISOLOGOTIPOS_B_Horizontal.png", width=250),
                            ft.Text("Iniciar Sesión", size=26, weight="bold", color="#333"),
                            usuario,
                            contraseña,
                            ft.ElevatedButton("Ingresar", on_click=on_login, width=300,
                                              style=ft.ButtonStyle(bgcolor="#1976d2", color="white")),
                            self.mensaje,
                            ft.Text("¿No tienes una cuenta?", size=12),
                            ft.TextButton("Regístrate aquí", on_click=lambda e: self.page.go("/registro"))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    )
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
