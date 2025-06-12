import flet as ft
import re

class RegistroView:
    def __init__(self, page):
        self.page = page
        self.mensaje = ft.Text(value="", size=14)

    def view(self):
        def validar_entrada(e):
            texto = e.control.value
            texto_filtrado = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]", "", texto)
            if texto_filtrado:
                texto_filtrado = texto_filtrado.title() 

            if texto != texto_filtrado:
                nombre.value = texto_filtrado
                self.page.update()

        nombre = ft.TextField(
            label="Nombre completo", border_radius=8, bgcolor="black",
            width=300, on_change=validar_entrada
        )
        usuario = ft.TextField(label="Nombre de usuario", border_radius=8, bgcolor="black", width=300)
        correo = ft.TextField(label="Correo electrónico", border_radius=8, bgcolor="black", width=300)
        contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=8, bgcolor="black", width=300)
        confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, border_radius=8, bgcolor="black", width=300)

        def on_register(e):
            if not nombre.value or not usuario.value or not correo.value or not contraseña.value or not confirmar.value:
                self.mensaje.value = "Completa todos los campos"
                self.mensaje.color = "red"
            elif "@" not in correo.value or "." not in correo.value:
                self.mensaje.value = "Falta @ o dominio"
                self.mensaje.color = "red"
            elif contraseña.value != confirmar.value:
                self.mensaje.value = "Las contraseñas no coinciden"
                self.mensaje.color = "red"
            else:
                self.mensaje.value = "¡Registro exitoso!"
                self.mensaje.color = "green"
                self.page.go("/login")
            self.page.update()

        return ft.View(
            route="/registro",
            controls=[
                ft.Container(
                    width=450,
                    padding=30,
                    bgcolor="blue",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=12, color="#6AD5FF73"),
                    content=ft.Column(
                        [
                            ft.Image(src="Printers Serigrafía_ISOLOGOTIPOS_B_Horizontal.png", width=250),
                            ft.Text("Registro de Usuario", size=26, weight="bold", color="#333"),
                            nombre, usuario, correo, contraseña, confirmar,
                            ft.ElevatedButton("Registrarse", on_click=on_register, width=300,
                                              style=ft.ButtonStyle(bgcolor="#1976d2", color="white")),
                            self.mensaje,
                            ft.Text("¿Ya tienes una cuenta?", size=12),
                            ft.TextButton("Inicia sesión aquí", on_click=lambda e: self.page.go("/login"))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    )
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
