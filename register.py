import flet as ft
import re
from conexion_bd import get_connection

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
            if not nombre.value.strip() or not usuario.value.strip() or not correo.value.strip() or not contraseña.value.strip() or not confirmar.value.strip():
                self.mensaje.value = "Completa todos los campos"
                self.mensaje.color = "red"
            elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", correo.value.strip()):
                self.mensaje.value = "Correo inválido"
                self.mensaje.color = "red"
            elif contraseña.value != confirmar.value:
                self.mensaje.value = "Las contraseñas no coinciden"
                self.mensaje.color = "red"
            else:
                try:
                    conexion = get_connection()
                    cursor = conexion.cursor()

                    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ?", (usuario.value,))
                    resultado = cursor.fetchone()

                    if resultado:
                        self.mensaje.value = "El nombre de usuario ya está registrado"
                        self.mensaje.color = "red"
                    else:
                        cursor.execute(
                            "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)",
                            (usuario.value, contraseña.value)
                        )
                        conexion.commit()
                        self.mensaje.value = "¡Registro exitoso!"
                        self.mensaje.color = "green"
                        self.page.go("/login")

                    conexion.close()

                except Exception as error:
                    print("Error en el registro:", error)
                    self.mensaje.value = "Error en el registro"
                    self.mensaje.color = "red"

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
