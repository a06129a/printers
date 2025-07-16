import flet as ft
from conexion_bd import get_connection
import re
from costos import CostosView
class PantallaCostos:
    def __init__(self, page: ft.Page,documento_cliente):
        self.page = page
        self.page.title = "Costos de Producción"
        self.page.scroll = ft.ScrollMode.ALWAYS
        self.page.bgcolor = "#0039e6"
        self.documento_cliente=documento_cliente

        # Variable  s de entrada
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

    def ir_a_costos(self, e):
        self.mandar_datos(e)
        self.mandar_datos_materiales(e)
        self.page.client_storage.set("documento_cliente", self.documento_cliente)  # Guardar documento
        self.page.go("/costos")  # Cambiás de vista

    def mandar_datos(self, e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO Pliegues (
                Documento, Unidades, Pliegue, Pliego_Ancho, Pliego_Posturas,
                Unidad_Largo, Unidad_Superficie, Cinta_Espesor, Cinta_Volumen,
                Cinta_CM, Impre_Cant_Color, Impre_Pliegos, Impre_Pasadas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            self.documento_cliente,
            0,  # Unidades
            0,  # Pliegue
            float(self.ancho.value or 0),
            float(self.unidades_posturas.value or 0),
            float(self.largo.value or 0),
            float(self.superficie.value.replace(" cm²", "") or 0),
            float(self.espesor.value or 0),
            float(self.volumen.value.replace(" cm³", "") or 0),
            0,  # Cinta_CM
            int(self.colores.value or 0),
            int(self.pliegos.value or 0),
            int(self.pasadas.value or 0)
            ))
            conn.commit()
            conn.close()
            print("Datos guardados exitosamente")
        except Exception as ex:
            print("Error al guardar los datos", ex)
    def cargar_datos(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT Pliego_Ancho, Unidad_Largo, Cinta_Espesor, Unidad_Superficie, Cinta_Volumen, Pliego_Posturas, Impre_Pliegos, Impre_Pasadas, Impre_Cant_Color FROM Pliegues WHERE Documento = ?""", (self.documento_cliente,))
            resultado = cursor.fetchone()
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
                conn.close()
            else:
                print("No se encontraron datos para este cliente")
        except Exception as ex:
            print("Error al cargar datos:", ex)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT Costo_impresion_Demasia_Imp, Costo_material_Peso, Costo_material_Total_Kg, Costo_material_PeCm, Costo_material_Pe, Costo_impresion_Precioxpasada, Costo_impresion_Costo_Min, Costo_impresion_Costo_Final, Costo_tinta_Tinta_Rinde, Costo_tinta_Porciento, Costo_tinta_Caras , Costo_tinta_Precioxlt, Costo_tinta_Lts_Necesarios, Costo_tinta_Costo_final, Costo_de_mano_obra_Cantpersonal, Costo_de_mano_obra_Jornal, Costo_de_mano_obra_Dias, Costo_mano_de_obra, Costo_cinta_Largo, Costo_cinta_Precio, Costo_cinta_Costo, Costo_barniz_Tinta_Rinde, Costo_barniz_Porciento, Costo_barniz_Caras, Costo_barniz_Usxlt, Costo_barniz_Lts, Costo_barniz_Costo_Finalxcm  FROM Materiales WHERE Documento = ?""", (self.documento_cliente,))
            resultado = cursor.fetchone()
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
                conn.close()
            else:
                print("No se encontraron datos para este cliente")
        except Exception as ex:
            print("Error al cargar datos:", ex)

    def mandar_datos_materiales(self, e):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO Materiales (
                    Documento,
                    Costo_impresion_Demasia_Imp,
                    Costo_material_Peso,
                    Costo_material_Total_Kg,
                    Costo_material_PeCm,
                    Costo_material_Pe,
                    Costo_impresion_Precioxpasada,
                    Costo_impresion_Costo_Min,
                    Costo_impresion_Costo_Final,
                    Costo_tinta_Tinta_Rinde,
                    Costo_tinta_Porciento,
                    Costo_tinta_Caras,
                    Costo_tinta_Precioxlt,
                    Costo_tinta_Lts_Necesarios,
                    Costo_tinta_Costo_final,
                    Costo_de_mano_obra_Cantpersonal,
                    Costo_de_mano_obra_Jornal,
                    Costo_de_mano_obra_Dias,
                    Costo_mano_de_obra,
                    Costo_cinta_Largo,
                    Costo_cinta_Precio,
                    Costo_cinta_Costo,
                    Costo_barniz_Tinta_Rinde,
                    Costo_barniz_Porciento,
                    Costo_barniz_Caras,
                    Costo_barniz_Usxlt,
                    Costo_barniz_Lts,
                    Costo_barniz_Costo_Finalxcm
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.documento_cliente,
                self.dem_impr.value,
                self.peso.value,
                self.total_kg.value,
                self.precio_cm2.value,
                self.costo_pelicula.value,
                self.precio_pasada.value,
                self.costo_min.value,
                self.costo_impresion.value,
                self.tinta_rinde.value,
                self.tinta_porcentaje.value,
                self.tinta_caras.value,
                self.precio_tinta_litro.value,
                self.litros_necesarios.value,
                self.costo_tinta.value,
                self.personal.value,
                self.jornal.value,
                self.dias.value,
                self.costo_mano_obra.value,
                self.largo_rollo.value,
                self.precio_rollo.value,
                self.costo_cinta.value,
                self.tinta_rinde_barniz.value,
                self.tinta_porcentaje_barniz.value,
                self.tinta_caras_barniz.value,
                self.precio_barniz_litro.value,
                self.litros_necesarios_barniz.value,
                self.costo_barniz.value
            ))

            # Guardar los cambios
            conn.commit()
            conn.close()
        except Exception as ex:
            print("Error al guardar datos de materiales:", ex)

    def actualizar(self, e):
        try:
            ancho = limpiar_valor(self.ancho.value)
            largo = limpiar_valor(self.largo.value)
            espesor = limpiar_valor(self.espesor.value)
            unidades = limpiar_valor(self.unidades_posturas.value)
            demasia = limpiar_valor(self.dem_impr.value) / 100
            colores = limpiar_valor(self.colores.value)
            precio_kg = limpiar_valor(self.precio_kg.value)
            precio_cm2 = limpiar_valor(self.precio_cm2.value)
            precio_pasada = limpiar_valor(self.precio_pasada.value)
            costo_min = limpiar_valor(self.costo_min.value)
            tinta_rinde = limpiar_valor(self.tinta_rinde.value)
            tinta_pct = limpiar_valor(self.tinta_porcentaje.value) / 100
            tinta_caras = limpiar_valor(self.tinta_caras.value)
            precio_tinta_litro = limpiar_valor(self.precio_tinta_litro.value)
            personal = limpiar_valor(self.personal.value)
            jornal = limpiar_valor(self.jornal.value)
            dias = limpiar_valor(self.dias.value)
            largo_rollo = limpiar_valor(self.largo_rollo.value)
            precio_rollo = limpiar_valor(self.precio_rollo.value)
            tinta_rinde_b = limpiar_valor(self.tinta_rinde_barniz.value)
            tinta_pct_b = limpiar_valor(self.tinta_porcentaje_barniz.value) / 100
            tinta_caras_b = limpiar_valor(self.tinta_caras_barniz.value)
            precio_barniz_litro = limpiar_valor(self.precio_barniz_litro.value)

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

        # 🚫 Evitar valores que empiezan con punto (como .8453), forzamos a que empiece con 0
        if valor_limpio.startswith("."):
            valor_limpio = "0" + valor_limpio

        if valor_original != valor_limpio:
            e.control.value = valor_limpio
            e.control.update()


    def validar_y_actualizar(self, e):
        self.validar_numeros(e)
        self.actualizar(e)

    def view(self):
        return ft.View(
            route="/costos",
            scroll=ft.ScrollMode.ALWAYS,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            bgcolor="#1976d2",   # ocupa todo el ancho
            controls=[
                ft.Container(
                    bgcolor="#1976d2",   # Fondo azul más oscuro, por ejemplo
                    padding=10,          # Espaciado interno
                    border_radius=0, 
                    content=ft.Row([
                        ft.Image(src="imagen/Printers.png", width=150),
                        ft.ElevatedButton("Clientes", on_click=lambda e: self.page.go("/clientes")),
                        ft.ElevatedButton("Crear", on_click=lambda e: print("Guardar"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ),  
                ft.Divider(),
                ft.Container(
                    bgcolor="#1976d2",  # Color de fondo del bloque
                    padding=10,         # Espacio interno
                    border_radius=0,   # Bordes redondeados (opcional)
                    content=ft.Column([
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
                        ft.Row([self.tinta_rinde_barniz, self.tinta_porcentaje_barniz, self.    tinta_caras_barniz, self.precio_barniz_litro]),
                        self.litros_necesarios_barniz,
                        self.costo_barniz,
                        ft.Divider(),
                        ft.Row([
                            ft.ElevatedButton("Atrás", on_click=lambda e: self.page.go("/pantalla6")),
                            ft.ElevatedButton("Siguiente", on_click=lambda e: self.ir_a_costos(e))
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=15)
                )
                 
        ],
    )
def limpiar_valor(valor):
    if valor is None:
        return 0.0
    # Eliminar cualquier carácter que no sea un dígito o un punto decimal
    valor_limpio = re.sub(r"[^0-9.]", "", valor)
    try:
        return float(valor_limpio)
    except ValueError:
        return 0.0