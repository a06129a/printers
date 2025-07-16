import flet as ft
import os
import sys
from conexion_bd import get_connection
import threading
import re

class CostosView:

    def __init__(self, page: ft.Page, documento_cliente):
        self.page = page
        self.documento_cliente = documento_cliente
        self.mensaje_guardado = ft.Text(value="", color="green", weight="bold")
        self.switch_barniz = ft.Switch(value=False)
        self.switch_cinta = ft.Switch(value=False)
    def label(self, texto):
        return ft.Container(
            content=ft.Text(texto, color="white"),
            bgcolor="#0039e6",
            padding=10,
            border_radius=25,
            width=180
        )

    def view(self):
        documento_cliente = self.page.client_storage.get("documento_cliente")
        if not documento_cliente:
            documento_cliente = "Documento no disponible"

        subtotal = ft.TextField(width=100, read_only=True, keyboard_type=ft.KeyboardType.NUMBER)
        margen = ft.TextField(width=100, keyboard_type=ft.KeyboardType.NUMBER)
        total_ventas = ft.TextField(width=100, read_only=True, keyboard_type=ft.KeyboardType.NUMBER)

        def validar_numerico(e):
            valor = e.control.value.strip()

            # Solo permitimos dígitos, puntos y comas
            valor = re.sub(r"[^0-9.,]", "", valor)

            # Reemplazamos coma por punto
            valor = valor.replace(",", ".")

            # Bloqueamos si empieza con punto
            if valor.startswith("."):
                valor = ""

            # Permitimos solo un punto decimal (el primero)
            partes = valor.split(".")
            if len(partes) > 2:
                valor = partes[0] + "." + "".join(partes[1:])

            # Validamos que el punto (si existe) esté precedido por al menos un dígito
            if "." in valor and not re.match(r"^\d+\.\d*$", valor):
                # El punto no está en lugar válido, lo eliminamos todo
                valor = re.sub(r"\.", "", valor)

            if e.control.value != valor:
                e.control.value = valor
                e.control.update()

        def actualizar_total_ventas(e=None):
            try:
                s = float(subtotal.value or 0)
                m = float(margen.value or 0)
                total = s + (m / 100 * s)
                total_ventas.value = str(round(total, 2))
            except ValueError:
                total_ventas.value = ""
            self.page.update()

        def actualizar_subtotal(e=None):
            subtotal_valor = 0
            campos_a_sumar = [
                "varios", "material", "pelicula", "tinta", "shablon",
                "corte", "troquel", "armado", "troquelado", "doblado",
                "horas", "empleados"
            ]
            for campo in campos_a_sumar:
                try:
                    subtotal_valor += float(inputs[campo].value or 0)
                except ValueError:
                    pass
            try:
                subtotal_valor += float(mano_obra.value or 0)
            except ValueError:
                pass
            if self.switch_barniz.value:
                subtotal_valor += 1
            if self.switch_cinta.value:
                subtotal_valor += 1
            subtotal.value = str(round(subtotal_valor, 2))
            actualizar_total_ventas()

        def crear_input_numerico():
            return ft.TextField(
                width=150,
                border_radius=25,
                keyboard_type=ft.KeyboardType.NUMBER,
                on_change=lambda e: (validar_numerico(e), actualizar_subtotal())
            )

        inputs = {nombre: crear_input_numerico() for nombre in [
            "varios", "material", "pelicula", "tinta", "shablon", "barniz",
            "corte", "troquel", "armado", "troquelado", "doblado", "cinta",
            "horas", "empleados"
        ]}

        mano_obra = ft.TextField(width=200, border_radius=25, keyboard_type=ft.KeyboardType.NUMBER,on_change=lambda e: (validar_numerico(e), actualizar_subtotal()))
        margen.on_change = lambda e: (validar_numerico(e), actualizar_total_ventas())
        self.switch_barniz.on_change = actualizar_subtotal
        self.switch_cinta.on_change = actualizar_subtotal

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        conn = get_connection()
        if conn and documento_cliente != "Documento no disponible":
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    Varios, Material, Valor_Pelicula, Valor_Tinta, Shablon, Barniz,
                    Vlor_Corte, Valor_Troquel, Valor_Armado, Valor_Troquelado, Valor_Doblado,
                    Aplicacion_Cinta, Cantidad_Horas, Cantidad_Empleados,
                    Mano_Obra, Subtotal, Margen, Total_Ventas
                FROM clientes
                WHERE Documento = ?
            """, (documento_cliente,))
            fila = cursor.fetchone()
            conn.close()

            if fila:
                columnas = [
                    "varios", "material", "pelicula", "tinta", "shablon", "barniz",
                    "corte", "troquel", "armado", "troquelado", "doblado", "cinta",
                    "horas", "empleados"
                ]
                for i, col in enumerate(columnas):
                    if fila[i] is not None:
                        inputs[col].value = str(fila[i])
                self.switch_barniz.value = bool(fila[5])
                self.switch_cinta.value = bool(fila[11])
                mano_obra.value = str(fila[14] or "")
                subtotal.value = str(fila[15] or "")
                margen.value = str(fila[16] or "")
                total_ventas.value = str(fila[17] or "")

        conn = get_connection()
        if conn and documento_cliente != "Documento no disponible":
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    Varios, Material, Valor_Pelicula, Valor_Tinta, Shablon, Barniz,
                    Vlor_Corte, Valor_Troquel, Valor_Armado, Valor_Troquelado, Valor_Doblado,
                    Aplicacion_Cinta, Cantidad_Horas, Cantidad_Empleados,
                    Mano_Obra, Subtotal, Margen, Total_Ventas
                FROM clientes
                WHERE Documento = ?
            """, (documento_cliente,))
            fila = cursor.fetchone()
            conn.close()

            if fila:
                columnas = [
                    "varios", "material", "pelicula", "tinta", "shablon", "barniz",
                    "corte", "troquel", "armado", "troquelado", "doblado", "cinta",
                    "horas", "empleados"
                ]
                for i, col in enumerate(columnas):
                    if fila[i] is not None:
                        inputs[col].value = str(fila[i])
                self.switch_barniz.value = bool(fila[5])
                self.switch_cinta.value = bool(fila[11])
                mano_obra.value = str(fila[14] or "")
                subtotal.value = str(fila[15] or "")
                margen.value = str(fila[16] or "")
                total_ventas.value = str(fila[17] or "")
        def guardar_datos(e):
            datos = {k: v.value for k, v in inputs.items()}
            datos.update({
                "mano_obra": mano_obra.value,
                "subtotal": subtotal.value,
                "margen": margen.value,
                "total_ventas": total_ventas.value
            })

            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                documento_cliente = self.page.client_storage.get("documento_cliente")
                if documento_cliente:
                    cursor.execute("""
                        UPDATE clientes SET
                            Varios = ?,
                            Material = ?,
                            Valor_Pelicula = ?,
                            Valor_Tinta = ?,
                            Shablon = ?,
                            Barniz = ?,
                            Vlor_Corte = ?,
                            Valor_Troquel = ?,
                            Valor_Armado = ?,
                            Valor_Troquelado = ?,
                            Valor_Doblado = ?,
                            Aplicacion_Cinta = ?,
                            Cantidad_Horas = ?,
                            Cantidad_Empleados = ?,
                            Mano_Obra = ?,
                            Subtotal = ?,
                            Margen = ?,
                            Total_Ventas = ?,
                            fecha_ultima_edicion = CURRENT_DATE
                        WHERE Documento = ?
                    """, (
                        datos["varios"],
                        datos["material"],
                        float(datos["pelicula"] or 0),
                        float(datos["tinta"] or 0),
                        datos["shablon"],
                        self.switch_barniz.value,
                        float(datos["corte"] or 0),
                        float(datos["troquel"] or 0),
                        float(datos["armado"] or 0),
                        float(datos["troquelado"] or 0),
                        float(datos["doblado"] or 0),
                        self.switch_cinta.value,
                        float(datos["horas"] or 0),
                        float(datos["empleados"] or 0),
                        float(datos["mano_obra"] or 0),
                        float(datos["subtotal"] or 0),
                        float(datos["margen"] or 0),
                        float(datos["total_ventas"] or 0),
                        documento_cliente
                    ))
                    conn.commit()
                    conn.close()

                    self.mensaje_guardado.value = "Los datos se han guardado correctamente."
                    self.page.update()

                    def limpiar_mensaje():
                        self.mensaje_guardado.value = ""
                        self.page.update()

                    threading.Timer(3, limpiar_mensaje).start()
        def ir_a_orden_pedido(e):
            guardar_datos
            self.page.client_storage.set("documento_cliente", self.documento_cliente)  # Guardar documento
            self.page.go("/orden_pedido")  # Cambiás de vista
        actualizar_subtotal()

        return ft.View(
            route="/costos",
            scroll=ft.ScrollMode.ALWAYS,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            bgcolor="#1976d2",
            controls=[
                ft.Container(
                    padding=20,
                    bgcolor="#1976d2",
                    expand=True,
                    content=ft.Column([
                        ft.Image(src=resource_path("imagen/Printers.png"), width=250),
                        ft.Container(
                            bgcolor="#1976d2", padding=10,
                            content=ft.Text("Costos", size=32, weight="bold", color="white",
                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))
                        ),
                        ft.Row([self.label("Varios:"), inputs["varios"], self.label("Material:"), inputs["material"]], spacing=10),
                        ft.Row([self.label("Valor Película:"), inputs["pelicula"], self.label("Valor Tinta:"), inputs["tinta"]], spacing=10),
                        ft.Row([self.label("Shablón:"), inputs["shablon"], self.label("Cant. empleados:"), inputs["empleados"]], spacing=10),
                        ft.Row([self.label("Valor Corte:"), inputs["corte"], self.label("Valor troquel:"), inputs["troquel"]], spacing=10),
                        ft.Row([self.label("Valor Armado:"), inputs["armado"], self.label("Valor troquelado:"), inputs["troquelado"]], spacing=10),
                        ft.Row([self.label("Valor Doblado:"), inputs["doblado"], self.label("Aplicacion cinta:"), self.switch_cinta], spacing=10),
                        ft.Row([self.label("Cantidad horas:"), inputs["horas"], self.label("Barniz:"), self.switch_barniz], spacing=10),
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Mano de Obra:", color="white", weight="bold"),
                                bgcolor="#1536f1", padding=10, border_radius=25, width=250
                            ),
                            mano_obra
                        ], spacing=10),
                        ft.Divider(),
                        self.mensaje_guardado,
                        ft.Row([
                            ft.Text("Sub total"), subtotal,
                            ft.Text("(...) c/u"),
                            ft.Text("Margen %"), margen,
                            ft.Text("(...) %")
                        ], spacing=10),
                        ft.Row([
                            ft.Text("Total ventas"), total_ventas,
                            ft.Text("(...) c/u")
                        ], spacing=10),
                        ft.Row([
                            ft.ElevatedButton("Guardar datos (TEMP)", on_click=guardar_datos),
                            ft.ElevatedButton("Orden pedido", bgcolor="#1536f1", color="white", on_click=lambda e: ir_a_orden_pedido(e))
                        ], alignment=ft.MainAxisAlignment.END, spacing=20),
                        ft.Row([
                            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/pantalla7"),
                                    bgcolor="white", color="black")
                        ], alignment=ft.MainAxisAlignment.START)
                    ], spacing=15)
                )
            ]
        )
