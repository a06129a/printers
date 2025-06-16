from conexion_bd import get_connection
import flet as ft
import re
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
        self.page.go("/costos")

    def view(self):
        self.nombre_input = ft.TextField(label="Nombre", width=200, on_change=self.capitalizar_nombre)
        self.documento_input = ft.TextField(label="Documento", width=200, on_change=self.validar_documento)

        self.dia_dropdown = ft.Dropdown(label="Día", width=100)
        self.mes_dropdown = ft.Dropdown(label="Mes", width=130, on_change=self.actualizar_dias)
        self.anio_dropdown = ft.Dropdown(label="Año", width=120)

        self.dia_dropdown.options = [ft.dropdown.Option(str(d)) for d in range(1, 32)]
        self.mes_dropdown.options = [ft.dropdown.Option(str(m)) for m in range(1, 13)]
        self.anio_dropdown.options = [ft.dropdown.Option(str(a)) for a in range(2025, 2031)]

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
                self.lista_clientes.controls.append(
                    ft.Row([
                        ft.Text(c["nombre"], weight="bold", color="white"),
                        ft.Text(f"Doc: {c['Documento']}", color="white"),
                        ft.Text(f"Entrega: {c['fecha_ultima_edicion']}", color="white"),
                        ft.ElevatedButton("Modificar", on_click=lambda e, doc=c["Documento"]: self.ir_a_costos(doc)),
                        ft.ElevatedButton("Borrar", on_click=lambda e, id=c["id_cliente"]: borrar_cliente(id),
                                          bgcolor="red", color="white")
                    ])
                )
            self.page.update()

        def agregar_cliente(e):
            if not all([self.nombre_input.value, self.documento_input.value,
                        self.dia_dropdown.value, self.mes_dropdown.value, self.anio_dropdown.value]):
                self.mensaje.value = "Completa todos los campos"
                self.mensaje.color = "red"
                self.page.update()
                return

            dia = self.dia_dropdown.value.zfill(2)
            mes = self.mes_dropdown.value.zfill(2)
            anio = self.anio_dropdown.value[-2:]
            fecha = f"{dia}/{mes}/{anio}"

            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE Documento = ?", (self.documento_input.value,))
                if cursor.fetchone()[0] > 0:
                    self.mensaje.value = "Documento ya registrado"
                    self.mensaje.color = "red"
                    self.page.update()
                    return

                cursor.execute(
                    "INSERT INTO clientes (nombre, Documento, fecha_ultima_edicion) VALUES (?, ?, ?)",
                    (self.nombre_input.value, self.documento_input.value, fecha)
                )
                conn.commit()
                conn.close()

            self.nombre_input.value = ""
            self.documento_input.value = ""
            self.dia_dropdown.value = None
            self.mes_dropdown.value = None
            self.anio_dropdown.value = None
            self.mensaje.value = "Cliente agregado"
            self.mensaje.color = "green"
            self.cargar_clientes()
            self.page.update()

        def cambiar_lista(e):
            self.orden_filtro = (self.orden_filtro + 1) % 3
            self.cargar_clientes()

        def buscar_clientes(e):
            self.cargar_clientes()

        self.cargar_clientes = lambda: render_clientes(self.obtener_clientes_desde_bd())
        self.cargar_clientes()

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
                            self.nombre_input,
                            self.documento_input,
                            self.dia_dropdown,
                            self.mes_dropdown,
                            self.anio_dropdown,
                            ft.ElevatedButton("Agregar", on_click=agregar_cliente),
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
                            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/login")),
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
        capitalizado = texto.capitalize()
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
