import flet as ft
from conexion_bd import get_connection
import re

class PantallaCostos:
    def __init__(self, page: ft.Page,documento_cliente):
        self.page = page
        self.page.title = "Costos de Producción"
        self.page.scroll = ft.ScrollMode.ALWAYS
        self.page.bgcolor = "#0277bd"
        self.documento_cliente=documento_cliente
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Variables de entrada
        self.ancho = ft.TextField(label="Ancho (cm)", width=100, on_change=self.validar_y_actualizar)
        self.largo = ft.TextField(label="Largo (cm)", width=100, on_change=self.validar_y_actualizar)
        self.espesor = ft.TextField(label="Espesor (cm)", width=100, on_change=self.validar_y_actualizar)
        self.superficie = ft.Text(value="0.00 cm²", size=18, color="white")
        self.volumen = ft.Text(value="0.00 cm³", size=18, color="white")

        # Datos impresión
        self.unidades_posturas = ft.TextField(label="Unidades/Posturas", width=100, on_change=self.validar_y_actualizar)
        self.dem_impr = ft.TextField(label="Demasía (%)", width=100, on_change=self.validar_y_actualizar)
        self.pliegos = ft.Text(value="0", size=18, color="white")
        self.colores = ft.TextField(label="Cant. Colores", width=100, on_change=self.validar_y_actualizar)
        self.pasadas = ft.Text(value="0", size=18, color="white")

        # Costo Material
        self.precio_kg = ft.TextField(label="Precio kg $", width=100, on_change=self.validar_y_actualizar)
        self.peso = ft.Text(value="0.00 kg", size=18, color="white")
        self.total_kg = ft.Text(value="0.00 kg", size=18, color="white")
        self.costo_material = ft.Text(value="$0.00", size=18, color="white")

        # Costo Película
        self.precio_cm2 = ft.TextField(label="Precio cm² $", width=100, on_change=self.validar_y_actualizar)
        self.costo_pelicula = ft.Text(value="$0.00", size=18, color="white")

        # Costo Impresión
        self.precio_pasada = ft.TextField(label="Precio Pasada $", width=100, on_change=self.validar_y_actualizar)
        self.costo_min = ft.TextField(label="Costo Mínimo $", width=100, on_change=self.validar_y_actualizar)
        self.costo_impresion = ft.Text(value="$0.00", size=18, color="white")

        # Costo Tinta
        self.tinta_rinde = ft.TextField(label="Tinta Rinde (m²/L)", width=100, on_change=self.validar_y_actualizar)
        self.tinta_porcentaje = ft.TextField(label="%", width=100, on_change=self.validar_y_actualizar)
        self.tinta_caras = ft.TextField(label="Caras", width=100, on_change=self.validar_y_actualizar)
        self.precio_tinta_litro = ft.TextField(label="Precio Litro $", width=100, on_change=self.validar_y_actualizar)
        self.litros_necesarios = ft.Text(value="0.00 L", size=18, color="white")
        self.costo_tinta = ft.Text(value="$0.00", size=18, color="white")

        # Mano de Obra
        self.personal = ft.TextField(label="Cantidad Personal", width=100, on_change=self.validar_y_actualizar)
        self.jornal = ft.TextField(label="Jornal $", width=100, on_change=self.validar_y_actualizar)
        self.dias = ft.TextField(label="Días", width=100, on_change=self.validar_y_actualizar)
        self.costo_mano_obra = ft.Text(value="$0.00", size=18, color="white")

        # Cinta
        self.largo_rollo = ft.TextField(label="Largo Rollo (cm)", width=100, on_change=self.validar_y_actualizar)
        self.precio_rollo = ft.TextField(label="Precio Rollo $", width=100, on_change=self.validar_y_actualizar)
        self.costo_cinta = ft.Text(value="$0.00", size=18, color="white")

        # Costo Barniz
        self.tinta_rinde_barniz = ft.TextField(label="Tinta Rinde Barniz (m²/L)", width=100, on_change=self.validar_y_actualizar)
        self.tinta_porcentaje_barniz = ft.TextField(label="%", width=100, on_change=self.validar_y_actualizar)
        self.tinta_caras_barniz = ft.TextField(label="Caras", width=100, on_change=self.validar_y_actualizar)
        self.precio_barniz_litro = ft.TextField(label="Precio Litro $", width=100, on_change=self.validar_y_actualizar)
        self.litros_necesarios_barniz = ft.Text(value="0.00 L", size=18, color="white")
        self.costo_barniz = ft.Text(value="$0.00", size=18, color="white")

        self.page.add(self.view())
        self.cargar_datos()
    def mandar_datos(self, e):
        try:
            self.cursor.execute("""INSERT OR REPLACE Pliegues (Pliego_Ancho, Unidad_Largo, Cinta_Espesor, Unidad_Superficie, Cinta_Volumen, Pliego_Posturas, Impre_Pliegos, Impre_Pasadas, Impre_Cant_Color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",(
                self.ancho.value,
                self.largo.value,
                self.espesor.value,
                self.superficie.value,
                self.volumen.value,
                self.unidades_posturas.value,
                self.pliegos.value,
                self.pasadas.value,
                self.colores.value
            ))
    def cargar_datos(self):
        try:
            self.cursor.execute("""SELECT Pliego_Ancho, Unidad_Largo, Cinta_Espesor, Unidad_Superficie, Cinta_Volumen, Pliego_Posturas, Impre_Pliegos, Impre_Pasadas, Impre_Cant_Color FROM Pliegues WHERE Documento = ?""", (self.documento_cliente,))
            resultado = self.cursor.fetchone()
            if resultado:
                self.ancho.value = str(resultado[0])
                self.largo.value = str(resultado[1])
                self.espesor.value = str(resultado[2])
                self.superficie.value = f"{float(resultado[3]):.2f} cm²"
                self.volumen.value = f"{float(resultado[4]):.2f} cm³"
                self.unidades_posturas.value = str(resultado[5])
                self.pliegos.value = str(resultado[6])
                self.pasadas.value = str(resultado[7])
                self.colores.value = str(resultado[8])

                self.page.update()
            else:
                print("No se encontraron datos para este cliente")
        except Exception as ex:
            print("Error al cargar datos:", ex)
        try:
            self.cursor.execute("""SELECT Costo_impresion_Demasia_Imp, Costo_material_Peso, Costo_material_Total_Kg, Costo_material_PeCm, Costo_material_Pe, Costo_impresion_Precioxpasada, Costo_impresion_Costo_Min, Costo_impresion_Costo_Final, Costo_tinta_Tinta_Rinde, Costo_tinta_Porciento, Costo_tinta_Precioxlt, Costo_tinta_Lts_Necesarios, Costo_tinta_Costo_final, Costo_de_mano_obra_Cantpersonal, Costo_de_mano_obra_Jornal, Costo_de_mano_obra_Dias, Costo_mano_de_obra, Costo_cinta_Largo, Costo_cinta_Precio, Costo_cinta_Costo, Costo_barniz_Tinta_Rinde, Costo_barniz_Porciento, Costo_barniz_Caras, Costo_barniz_Usxlt, Costo_barniz_Lts, Costo_barniz_Costo_Finalxcm  FROM Materiales WHERE Documento = ?""", (self.documento_cliente,))
            resultado = self.cursor.fetchone()
            if resultado:
                self.dem_impr.value = str(resultado[0])
                self.precio_kg.value = str(resultado[1])
                self.total_kg.value = str(resultado[2])
                self.precio_cm2.value = str(resultado[3])
                self.costo_pelicula.value = str(resultado[4])
                self.precio_pasada.value = str(resultado[5])
                self.costo_min.value = str(resultado[6])
                self.costo_impresion.value = str(resultado[7])
                self.tinta_rinde.value = str(resultado[8])
                self.tinta_porcentaje.value = str(resultado[9])
                self.tinta_caras.value = str(resultado[10])
                self.precio_tinta_litro.value = str(resultado[11])
                self.litros_necesarios.value = str(resultado[12])
                self.costo_tinta.value = str(resultado[13])
                self.personal.value = str(resultado[14])
                self.jornal.value = str(resultado[15])
                self.dias.value = str(resultado[16])
                self.costo_mano_obra.value = str(resultado[17])
                self.largo_rollo.value = str(resultado[18])
                self.precio_rollo.value = str(resultado[19])
                self.costo_cinta.value = str(resultado[20])
                self.tinta_rinde_barniz.value = str(resultado[21])
                self.tinta_porcentaje_barniz.value = str(resultado[22])
                self.tinta_caras_barniz.value = str(resultado[23])
                self.precio_barniz_litro.value = str(resultado[24])
                self.litros_necesarios_barniz.value = str(resultado[25])
                self.costo_barniz.value = str(resultado[26])


                self.page.update()
            else:
                print("No se encontraron datos para este cliente")
        except Exception as ex:
            print("Error al cargar datos:", ex)

    def actualizar(self, e):
        try:
            ancho = float(self.ancho.value or 0)
            largo = float(self.largo.value or 0)
            espesor = float(self.espesor.value or 0)
            unidades = float(self.unidades_posturas.value or 0)
            demasia = float(self.dem_impr.value or 0) / 100
            colores = float(self.colores.value or 0)
            precio_kg = float(self.precio_kg.value or 0)
            precio_cm2 = float(self.precio_cm2.value or 0)
            precio_pasada = float(self.precio_pasada.value or 0)
            costo_min = float(self.costo_min.value or 0)
            tinta_rinde = float(self.tinta_rinde.value or 1)
            tinta_pct = float(self.tinta_porcentaje.value or 100) / 100
            tinta_caras = float(self.tinta_caras.value or 1)
            precio_tinta_litro = float(self.precio_tinta_litro.value or 0)
            personal = float(self.personal.value or 0)
            jornal = float(self.jornal.value or 0)
            dias = float(self.dias.value or 0)
            largo_rollo = float(self.largo_rollo.value or 1)
            precio_rollo = float(self.precio_rollo.value or 0)
            tinta_rinde_b = float(self.tinta_rinde_barniz.value or 1)
            tinta_pct_b = float(self.tinta_porcentaje_barniz.value or 100) / 100
            tinta_caras_b = float(self.tinta_caras_barniz.value or 1)
            precio_barniz_litro = float(self.precio_barniz_litro.value or 0)

            superficie = (ancho * largo) / 10000
            volumen = ancho * largo * espesor
            pliegos = (unidades + (unidades * demasia))
            pasadas = colores * pliegos

            peso = (volumen * 1.4) / 1000
            total_kg = peso * pliegos
            costo_material = precio_kg * total_kg

            costo_pelicula = superficie * precio_cm2

            costo_impresion = max(pliegos * colores * precio_pasada, costo_min)

            sup_total = superficie * pliegos
            litros_necesarios = sup_total / (tinta_rinde * tinta_pct * tinta_caras)
            costo_tinta = precio_tinta_litro * litros_necesarios

            costo_mano_obra = personal * jornal * dias

            costo_cinta = precio_rollo / (largo_rollo * 100)

            litros_barniz = sup_total / (tinta_rinde_b * tinta_pct_b * tinta_caras_b)
            costo_barniz = precio_barniz_litro * litros_barniz

            self.superficie.value = f"{superficie:.2f} cm²"
            self.volumen.value = f"{volumen:.2f} cm³"
            self.pliegos.value = f"{pliegos:.0f}"
            self.pasadas.value = f"{pasadas:.0f}"
            self.peso.value = f"{peso:.3f} kg"
            self.total_kg.value = f"{total_kg:.3f} kg"
            self.costo_material.value = f"${costo_material:.2f}"
            self.costo_pelicula.value = f"${costo_pelicula:.2f}"
            self.costo_impresion.value = f"${costo_impresion:.2f}"
            self.litros_necesarios.value = f"{litros_necesarios:.2f} L"
            self.costo_tinta.value = f"${costo_tinta:.2f}"
            self.costo_mano_obra.value = f"${costo_mano_obra:.2f}"
            self.costo_cinta.value = f"${costo_cinta:.2f}"
            self.litros_necesarios_barniz.value = f"{litros_barniz:.2f} L"
            self.costo_barniz.value = f"${costo_barniz:.2f}"

            self.page.update()

        except Exception as ex:
            print("Error de cálculo:", ex)

    def validar_numeros(self, e):
        valor_original = e.control.value
        valor_limpio = re.sub(r"[^0-9,\.]", "", valor_original)
        valor_limpio = valor_limpio.replace(",", ".")

        partes = valor_limpio.split(".")
        if len(partes) > 2:
            valor_limpio = partes[0] + "." + "".join(partes[1:])

        if valor_original != valor_limpio:
            e.control.value = valor_limpio
            e.control.update()  # 👈 Importante: actualiza ese campo específico

    def validar_y_actualizar(self, e):
        self.validar_numeros(e)
        self.actualizar()

    def view(self):
        return ft.View(
            route="/costos",
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row([
                    ft.Image(src="imagenes\\Printers.png", width=150),
                    ft.ElevatedButton("Clientes", on_click=lambda e: self.page.go("/clientes")),
                    ft.ElevatedButton("Crear", on_click=lambda e: print("Guardar"))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Column([
                    ft.Text("Superficie y Volumen", size=24, weight="bold", color="white"),
                    ft.Row([self.ancho, self.largo, self.espesor]),
                    self.superficie,
                    self.volumen,
                    ft.Divider(),
                    ft.Text("Datos de Impresión", size=24, weight="bold", color="white"),
                    ft.Row([self.unidades_posturas, self.dem_impr, self.colores]),
                    self.pliegos,
                    self.pasadas,
                    ft.Divider(),
                    ft.Text("Costo Material", size=24, weight="bold", color="white"),
                    ft.Row([self.precio_kg]),
                    self.peso,
                    self.total_kg,
                    self.costo_material,
                    ft.Divider(),
                    ft.Text("Costo Película", size=24, weight="bold", color="white"),
                    ft.Row([self.precio_cm2]),
                    self.costo_pelicula,
                    ft.Divider(),
                    ft.Text("Costo Impresión", size=24, weight="bold", color="white"),
                    ft.Row([self.precio_pasada, self.costo_min]),
                    self.costo_impresion,
                    ft.Divider(),
                    ft.Text("Costo Tinta", size=24, weight="bold", color="white"),
                    ft.Row([self.tinta_rinde, self.tinta_porcentaje, self.tinta_caras, self.precio_tinta_litro]),
                    self.litros_necesarios,
                    self.costo_tinta,
                    ft.Divider(),
                    ft.Text("Costo Mano de Obra", size=24, weight="bold", color="white"),
                    ft.Row([self.personal, self.jornal, self.dias]),
                    self.costo_mano_obra,
                    ft.Divider(),
                    ft.Text("Tipos de Cinta", size=24, weight="bold", color="white"),
                    ft.Row([self.largo_rollo, self.precio_rollo]),
                    self.costo_cinta,
                    ft.Divider(),
                    ft.Text("Costo Barniz", size=24, weight="bold", color="white"),
                    ft.Row([self.tinta_rinde_barniz, self.tinta_porcentaje_barniz, self.tinta_caras_barniz, self.precio_barniz_litro]),
                    self.litros_necesarios_barniz,
                    self.costo_barniz,
                    ft.Divider(),
                    ft.Row([
                        ft.ElevatedButton("Atrás", on_click=lambda e: self.page.go("/pantalla6")),
                        ft.ElevatedButton("Siguiente", on_click=lambda e: self.page.go("/costos"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=15)
            ]
        )
