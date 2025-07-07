from conexion_bd import get_connection
import flet as ft
import re
import os
import sys
from functools import partial

class ClientesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.lista_clientes = ft.Column(scroll=ft.ScrollMode.ALWAYS)
        self.mensaje = ft.Text(value="", color="green", size=14)
        self.orden_filtro = 0
        self.buscador_input = ft.TextField(hint_text="Buscar por nombre...", expand=True)

    def ir_a_costos(self, documento):
        self.page.client_storage.set("documento_cliente", documento)
        self.page.go("/pantalla6")
    def solo_letras_espacios_comas(self, e):
        texto = e.control.value
        texto_filtrado = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ ,]", "", texto)
        texto_formateado = " ".join(p.capitalize() for p in texto_filtrado.split(" "))
        e.control.value = texto_formateado
        e.control.update()

    def view(self):
        self.nombre_input = ft.TextField(label="Nombre", width=200, on_change=self.solo_letras_espacios_comas)
        self.documento_input = ft.TextField(label="Documento", width=200, on_change=self.validar_documento)

        self.dia_dropdown = ft.Dropdown(label="Día", width=100)
        self.mes_dropdown = ft.Dropdown(label="Mes", width=130, on_change=self.actualizar_dias)
        self.anio_dropdown = ft.Dropdown(label="Año", width=120)

        self.dia_dropdown.options = [ft.dropdown.Option(str(d)) for d in range(1, 32)]
        self.mes_dropdown.options = [ft.dropdown.Option(str(m)) for m in range(1, 13)]
        self.anio_dropdown.options = [ft.dropdown.Option(str(a)) for a in range(2025, 2031)]

        def resource_path(relative_path):
            """ Obtener la ruta absoluta a un recurso, funciona tanto en dev como en ejecutable """
            try:
                base_path = sys._MEIPASS  # cuando está empaquetado con PyInstaller
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        def borrar_cliente(cliente_id):
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (cliente_id,))
                conn.commit()
                conn.close()
            self.cargar_clientes()

        def render_clientes(clientes):
            self.lista_clientes.controls.clear()

            for c in clientes:
                def on_hover_handler(e):
                    e.control.bgcolor = "#1565c0" if e.data == "true" else None
                    e.control.update()

                cliente_container = ft.Container(
                    content=ft.Row([
                        ft.Text(c["nombre"], weight="bold", color="white"),
                        ft.Text(f"Doc: {c['Documento']}", color="white"),
                        ft.Text(f"Entrega: {c['fecha_ultima_edicion']}", color="white"),
                        ft.Container(expand=True),  # 👉 Esto agrega espacio entre los textos y los botones
                        ft.ElevatedButton(
                            "Modificar",
                            on_click=lambda e, doc=c["Documento"]: self.ir_a_costos(doc)
                        ),
                        ft.ElevatedButton(
                            "Borrar",
                            on_click=lambda e, id=c["id_cliente"]: borrar_cliente(id),
                            bgcolor="red",
                            color="white"
                        )
                    ],
                    alignment="start",  # 👉 Alineación como en el segundo código
                    vertical_alignment="center"  # 👉 Alineación vertical como en el segundo código
                    ),
                    bgcolor=None,
                    padding=10,
                    border_radius=5,
                    on_hover=on_hover_handler
                )

                self.lista_clientes.controls.append(cliente_container)

            self.page.update()


        def agregar_cliente(e):
            # Verificar que todos los campos estén completos
            # Verificar que todos los campos estén completos
            if not all([self.nombre_input.value, self.documento_input.value,
                        self.dia_dropdown.value, self.mes_dropdown.value, self.anio_dropdown.value]):
                self.mensaje.value = "Completa todos los campos"
                self.mensaje.color = "red"
                self.page.update()
                return

            # Verificar que el documento tenga exactamente 8 números
            if len(self.documento_input.value) != 8 or not self.documento_input.value.isdigit():
                self.mensaje.value = "El documento debe tener exactamente 8 números"
                self.mensaje.color = "red"
                self.page.update()
                return


            # Preparar la fecha
            dia = self.dia_dropdown.value.zfill(2)
            mes = self.mes_dropdown.value.zfill(2)
            anio = self.anio_dropdown.value[-2:]
            fecha = f"{dia}/{mes}/{anio}"

            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE Documento = ?", (self.documento_input.value,))
                if cursor.fetchone()[0] > 0:
                    # Documento ya existe
                    self.mensaje.value = "Documento ya registrado"
                    self.mensaje.color = "red"
                    self.page.update()
                    conn.close()
                    return  # 👈 No continúa

                # Insertar el cliente
                cursor.execute(
                    "INSERT INTO clientes (nombre, Documento, fecha_ultima_edicion) VALUES (?, ?, ?)",
                    (self.nombre_input.value, self.documento_input.value, fecha)
                )

                conn.commit()
                conn.close()

            # Si todo salió bien, limpiar los campos
            documento_agregado = self.documento_input.value  # 👉 Guardamos el documento antes de limpiar
            self.nombre_input.value = ""
            self.documento_input.value = ""
            self.dia_dropdown.value = None
            self.mes_dropdown.value = None
            self.anio_dropdown.value = None
            self.mensaje.value = "Cliente agregado"
            self.mensaje.color = "green"
            self.cargar_clientes()
            self.page.update()

            # 👉 Navegar a costos
            self.ir_a_costos(documento_agregado)


        def cambiar_lista(e):
            self.orden_filtro = (self.orden_filtro + 1) % 3
            self.cargar_clientes()

        def buscar_clientes(e):
            self.cargar_clientes()

        self.cargar_clientes = lambda: render_clientes(self.obtener_clientes_desde_bd())
        self.cargar_clientes()

        return ft.View(
            route="/clientes",
            bgcolor="#1976d2",
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Row([ft.ElevatedButton("Cerrar sesion",on_click=lambda e: self.page.go("/login"),bgcolor="red",color="white")]),
                        ft.Image(src=resource_path("imagen/Printers.png"), width=250),
                        ft.Text("Gestión de Clientes", size=28, weight="bold", color="white"),
                        ft.Row([
                            self.nombre_input,
                            self.documento_input,
                            self.dia_dropdown,
                            self.mes_dropdown,
                            self.anio_dropdown,
                            ft.ElevatedButton("Agregar", on_click=agregar_cliente, ),
                        ], spacing=10),
                        self.mensaje,
                        ft.Row([
                            self.buscador_input,
                            ft.ElevatedButton("Buscar", on_click=buscar_clientes),
                            ft.ElevatedButton("Cambiar orden", on_click=cambiar_lista)
                        ], spacing=10),
                        ft.Divider(color="white"),
                        self.lista_clientes,
                        ft.Divider(),
                        ft.Row([

                        ], alignment=ft.MainAxisAlignment.END, spacing=20)
                    ])
                )
            ]
        )

    def obtener_clientes_desde_bd(self):
        orden_sql = {
            0: "ORDER BY nombre ASC",
            1: "ORDER BY fecha_ultima_edicion DESC",
            2: "ORDER BY fecha_ultima_edicion ASC"
        }
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            query = f"""
                SELECT id_cliente, nombre, Documento, fecha_ultima_edicion 
                FROM clientes 
                WHERE nombre LIKE ?
                {orden_sql[self.orden_filtro]}
            """
            filtro = f"%{self.buscador_input.value.strip()}%"
            cursor.execute(query, (filtro,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(zip(["id_cliente", "nombre", "Documento", "fecha_ultima_edicion"], row)) for row in rows]
        return []

    def capitalizar_nombre(self, e):
        texto = e.control.value
        capitalizado = texto.title()
        if texto != capitalizado:
            self.nombre_input.value = capitalizado
            self.page.update()

    def validar_documento(self, e):
        texto = re.sub(r"[^\d]", "", e.control.value)[:8]
        if e.control.value != texto:
            self.documento_input.value = texto
            self.page.update()

    def actualizar_dias(self, e):
        mes = int(self.mes_dropdown.value or 1)
        dias_31 = [1, 3, 5, 7, 8, 10, 12]
        dias_30 = [4, 6, 9, 11]
        if mes in dias_31:
            max_dia = 31
        elif mes in dias_30:
            max_dia = 30
        else:
            max_dia = 29 
        self.dia_dropdown.options = [ft.dropdown.Option(str(d)) for d in range(1, max_dia + 1)]
        if int(self.dia_dropdown.value or 0) > max_dia:
            self.dia_dropdown.value = None
        self.page.update()