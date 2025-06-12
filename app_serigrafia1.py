import flet as ft

def costos_view(page):
    def input_fila(label1, label2):
        return ft.Row([
            ft.Container(
                content=ft.Text(label1, color="white"),
                bgcolor="#0168ee",
                padding=10,
                border_radius=25,
                width=180
            ),
            ft.TextField(width=150, border_radius=25),
            ft.Container(
                content=ft.Text(label2, color="white"),
                bgcolor="#0061f1",
                padding=10,
                border_radius=25,
                width=180
            ),
            ft.TextField(width=150, border_radius=25)
        ], spacing=10)

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
                        bgcolor="#3c6b83",
                        padding=10,
                        content=ft.Text(
                            "Costos",
                            size=32,
                            weight="bold",
                            color="black",
                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                        )
                    ),
                    input_fila("Varios:", "Material:"),
                    input_fila("Valor Película:", "Valor Tinta:"),
                    input_fila("Shablón:", "Barniz:"),
                    input_fila("Valor Corte:", "Valor troquel:"),
                    input_fila("Valor Armado:", "Valor troquelado:"),
                    input_fila("Valor Doblado:", "Aplicacion cinta:"),
                    input_fila("Cantidad horas:", "Cant. empleados:"),
                    ft.Row([
                        ft.Container(
                            content=ft.Text("Valor total de Mano de obra:", color="white", weight="bold"),
                            bgcolor="#1536f1",
                            padding=10,
                            border_radius=25,
                            width=250
                        ),
                        ft.TextField(width=200, border_radius=25)
                    ], spacing=10),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("Sub total"),
                        ft.TextField(width=100),
                        ft.Text("(...) c/u"),
                        ft.Text("Margen %"),
                        ft.TextField(width=100),
                        ft.Text("(...) %"),
                    ], spacing=10),
                    ft.Row([
                        ft.Text("Total ventas"),
                        ft.TextField(width=100),
                        ft.Text("(...) c/u"),
                    ], spacing=10),
                    ft.Container(
                        padding=10,
                        content=ft.Row([
                            ft.ElevatedButton("Atras", on_click=lambda e: page.go("/clientes"), bgcolor="white", color="black"),
                            ft.ElevatedButton("Orden pedido", bgcolor="#2e7d78", color="white")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=40)
                    )
                ], spacing=15)
            )
        ]
    )


def main(page: ft.Page):
    page.title = "Sistema de Serigrafía"
    page.bgcolor = "#bedae7"
    page.padding = 40

    mensaje = ft.Text(value="", size=14)

    def route_change(e):
        page.views.clear()
        print(f"Ruta actual: {page.route}")
        if page.route == "/registro":
            page.views.append(registro_view())
        elif page.route == "/clientes":
            page.views.append(clientes_view(page))
        elif page.route == "/costos":
            page.views.append(costos_view(page))
        else:
            page.views.append(login_view())
        page.update()


    def login_view():
        usuario = ft.TextField(label="Usuario", border_radius=8, bgcolor="black", width=300)
        contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=8, bgcolor="black", width=300)

        def on_login(e):
            if not usuario.value.strip() and not contraseña.value.strip():
                mensaje.value = "No introdujiste el usuario ni la contraseña"
                mensaje.color = "red"
            elif not usuario.value.strip():
                mensaje.value = "No introdujiste el usuario"
                mensaje.color = "red"
            elif not contraseña.value.strip():
                mensaje.value = "No introdujiste la contraseña"
                mensaje.color = "red"
            else:
                page.go("/clientes")
                return  # Salimos para no actualizar el mensaje
            page.update()


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
                            mensaje,
                            ft.Text("¿No tienes una cuenta?", size=12),
                            ft.TextButton("Regístrate aquí", on_click=lambda e: page.go("/registro"))
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

    def registro_view():
        nombre = ft.TextField(label="Nombre completo", border_radius=8, bgcolor="black", width=300)
        usuario = ft.TextField(label="Nombre de usuario", border_radius=8, bgcolor="black", width=300)
        correo = ft.TextField(label="Correo electrónico", border_radius=8, bgcolor="black", width=300)
        contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=8, bgcolor="black", width=300)
        confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, border_radius=8, bgcolor="black", width=300)

        def on_register(e):
            if not nombre.value or not usuario.value or not correo.value or not contraseña.value or not confirmar.value:
                mensaje.value = "Completa todos los campos"
                mensaje.color = "red"
            elif "@" not in correo.value or "." not in correo.value:
                mensaje.value = "Falta @ o dominio"
                mensaje.color = "red"
            elif contraseña.value != confirmar.value:
                mensaje.value = "Las contraseñas no coinciden"
                mensaje.color = "red"
            else:
                mensaje.value = "¡Registro exitoso!"
                mensaje.color = "green"
                page.go("/login")
            page.update()

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
                            mensaje,
                            ft.Text("¿Ya tienes una cuenta?", size=12),
                            ft.TextButton("Inicia sesión aquí", on_click=lambda e: page.go("/login"))
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

    def clientes_view(page):
        clientes = [
    {"nombre": "Pablo Nievas", "documento": "12345678", "fecha": "17/6/25"},
    {"nombre": "Juliana Rodriguez", "documento": "23456789", "fecha": "17/6/25"},
    {"nombre": "Roberto Mariano", "documento": "34567890", "fecha": "17/6/25"},
    {"nombre": "Rodrigo Culasso", "documento": "45678901", "fecha": "17/6/25"},
    {"nombre": "Belenger Hernandez", "documento": "56789012", "fecha": "17/6/25"},
    {"nombre": "Matias Gauto", "documento": "67890123", "fecha": "17/6/25"}
]


        nombre_input = ft.TextField(label="Nombre", width=200)
        documento_input = ft.TextField(label="Documento", width=200)
        fecha_input = ft.TextField(label="Fecha de entrega (dd/mm/yy)", width=200)
        mensaje = ft.Text(value="", color="green", size=14)

        lista_clientes = ft.Column(scroll=ft.ScrollMode.ALWAYS)

        def render_clientes():
            lista_clientes.controls.clear()
            for c in clientes:
                lista_clientes.controls.append(
                    ft.Row([
                        ft.Text(c["nombre"], weight="bold", color="white"),
                        ft.Text(f"Doc: {c['documento']}", color="white"),
                        ft.Text(f"Entrega: {c['fecha']}", color="white")
                    ])
                )
            page.update()

        def agregar_cliente(e):
            if nombre_input.value and documento_input.value and fecha_input.value:
                clientes.append({
                    "nombre": nombre_input.value,
                    "documento": documento_input.value,
                    "fecha": fecha_input.value
                })
                nombre_input.value = ""
                documento_input.value = ""
                fecha_input.value = ""
                mensaje.value = "Cliente agregado"
                mensaje.color = "green"
                render_clientes()
            else:
                mensaje.value = "Completa todos los campos"
                mensaje.color = "red"
            page.update()

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
    nombre_input,
    documento_input,
    fecha_input,
    ft.ElevatedButton("Agregar", on_click=agregar_cliente),
    ft.ElevatedButton("Modificar", on_click=lambda e: print("Modificar cliente")),
    ft.ElevatedButton("Borrar", on_click=lambda e: print("Borrar cliente"), bgcolor="red", color="white"),
], spacing=10),
                    

                        mensaje,
                        ft.Divider(color="white"),
                        lista_clientes,
                        ft.Divider(),
                        ft.Row([
                            ft.ElevatedButton("Volver", on_click=lambda e: page.go("/login")),
                            ft.ElevatedButton("Crear", on_click=lambda e: page.go("/costos")),
                        ], alignment=ft.MainAxisAlignment.END, spacing=20)
                    ])
                )
            ]
        )


    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main)