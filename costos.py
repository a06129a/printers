import flet as ft
from conexion_bd import get_connection

class CostosView:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.mensaje_guardado = ft.Text(value="", color="green", weight="bold")

    def label(self, texto):
        return ft.Container(
            content=ft.Text(texto, color="white"),
            bgcolor="#0168ee",
            padding=10,
            border_radius=25,
            width=180
        )

    def view(self):
        documento_cliente = self.page.client_storage.get("documento_cliente")
        if not documento_cliente:
            documento_cliente = "Documento no disponible"
    
        crear_input = lambda: ft.TextField(width=150, border_radius=25)
        inputs = {nombre: crear_input() for nombre in [
            "varios", "material", "pelicula", "tinta", "shablon", "barniz",
            "corte", "troquel", "armado", "troquelado", "doblado", "cinta",
            "horas", "empleados"
        ]}

        mano_obra = ft.TextField(width=200, border_radius=25)
        subtotal = ft.TextField(width=100)
        margen = ft.TextField(width=100)
        total_ventas = ft.TextField(width=100)

        conn = get_connection()
        if conn and documento_cliente != "Documento no disponible":
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    Varios, Material, Valor_Pelicula, Valor_Tinta, Shablon, Barniz,
                    Vlor_Corte, Valor_Troquel, Valor_Armado, Valor_Troquelado, Valor_Doblado,
                    Aplicacion_Cinta, Cantidad_Horas, Cantidad_Empleados
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
            
                mano_obra.value = ""  
                subtotal.value = ""
                margen.value = ""
                total_ventas.value = ""
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
                            fecha_ultima_edicion = CURRENT_DATE
                        WHERE Documento = ?
                    """, (
                        datos["varios"],
                        datos["material"],
                        float(datos["pelicula"] or 0),
                        float(datos["tinta"] or 0),
                        datos["shablon"],
                        False,
                        float(datos["corte"] or 0),
                        float(datos["troquel"] or 0),
                        float(datos["armado"] or 0),
                        float(datos["troquelado"] or 0),
                        float(datos["doblado"] or 0),
                        False,
                        float(datos["horas"] or 0),
                        float(datos["empleados"] or 0),
                        documento_cliente
                    ))

                    conn.commit()
                    conn.close()

                    self.mensaje_guardado.value = "Los datos se han guardado correctamente."
                    self.page.update()

                    def limpiar_mensaje():
                        self.mensaje_guardado.value = ""
                        self.page.update()
                    self.page.timer(3, limpiar_mensaje)

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
                        ft.Row([self.label("Shablón:"), inputs["shablon"], self.label("Cant. empleados:"), inputs["empleados"]], spacing=10),
                        ft.Row([self.label("Valor Corte:"), inputs["corte"], self.label("Valor troquel:"), inputs["troquel"]], spacing=10),
                        ft.Row([self.label("Valor Armado:"), inputs["armado"], self.label("Valor troquelado:"), inputs["troquelado"]], spacing=10),
                        ft.Row([self.label("Valor Doblado:"), inputs["doblado"], self.label("Aplicacion cinta:"), inputs["cinta"]], spacing=10),
                        ft.Row([self.label("Cantidad horas:"), inputs["horas"], self.label("Barniz:"), ft.Switch(value=False)], spacing=10),

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
