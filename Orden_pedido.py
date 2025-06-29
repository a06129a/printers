import flet as ft
from conexion_bd import get_connection
import re

class OrdenPedidoView:
    def __init__(self, page: ft.Page, documento_cliente):
        self.page = page
        self.documento_cliente = documento_cliente
        
        # Initialize form fields as instance variables for database operations
        self.cantidad_pedidos = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros, 
            width=120
        )
        self.cantidad_unidades = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros, 
            width=120
        )
        self.cliente_field = ft.TextField(
            label="Cliente", 
            bgcolor="#ffffff",
            color="#000000",  # Texto negro
            label_style=ft.TextStyle(color="#666666"),  # Color del label
            on_change=self.solo_letras_espacios_comas
        )
        self.publicidad_field = ft.TextField(
            label="Publicidad", 
            bgcolor="#ffffff",
            color="#000000",  # Texto negro
            label_style=ft.TextStyle(color="#666666"), # Color del label
            on_change=self.solo_letras_espacios_comas 
        )
        self.trabajo_field = ft.TextField(
            label="Trabajo", 
            bgcolor="#ffffff",
            color="#000000",  # Texto negro
            label_style=ft.TextStyle(color="#666666"),# Color del label
            on_change=self.solo_letras_espacios_comas  
        )
        self.cantidad_colores = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros, 
            width=120
        )
        
        # Detail fields
        self.detalles = [
            ft.TextField(
                label=f"{i+1}-", 
                bgcolor="#ffffff", 
                color="#000000",  # Texto negro
                label_style=ft.TextStyle(color="#666666"),  # Color del label
                width=450
            ) for i in range(6)
        ]
        
        self.impresion_field = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            width=320
        )
        self.termoformar_switch = ft.Switch(value=False)
        self.material_dropdown = ft.Dropdown(
            label="Selecciona una opción",
            width=200,
            label_style=ft.TextStyle(color="white"),
            text_style=ft.TextStyle(color="#000000"),  # Texto negro en dropdown
            options=[ft.dropdown.Option(f"Opción {i+1}") for i in range(3)]
        )
        self.cant_material = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros, 
            width=120
        )
        
        # Measurements
        self.ancho_pliego = ft.TextField(
            label="Ancho-cm", 
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            label_style=ft.TextStyle(color="#666666"),  # Color del label
            on_change=self.solo_numeros, 
            width=120
        )
        self.alto_pliego = ft.TextField(
            label="Alto-cm", 
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            label_style=ft.TextStyle(color="#666666"),  # Color del label
            on_change=self.solo_numeros, 
            width=120
        )
        self.espesor_field = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros, 
            width=120
        )
        
        # Process switches
        self.troquelado_switch = ft.Switch(value=False)
        self.doblado_switch = ft.Switch(value=False)
        self.corte_switch = ft.Switch(value=False)
        
        self.cinta_bifaz_dropdown = ft.Dropdown(
            label="Selecciona una opción", 
            width=200, 
            label_style=ft.TextStyle(color="white"),
            text_style=ft.TextStyle(color="#000000"),  # Texto negro en dropdown
            options=[ft.dropdown.Option(f"Opción {i+1}") for i in range(3)]
        )
        
        self.observaciones_field = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            multiline=True, 
            max_lines=4, 
            hint_text="Escribe aquí todos los detalles...",
            hint_style=ft.TextStyle(color="#888888")  # Color del hint text
        )
        
        # Dates
        self.fecha_recepcion = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros_y_barra, 
            width=120
        )
        self.fecha_entrega = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros_y_barra, 
            width=120
        )
        
        # Final fields
        self.imprimio_field = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            width=200
        )
        self.cant_impresa = ft.TextField(
            bgcolor="#ffffff", 
            color="#000000",  # Texto negro
            on_change=self.solo_numeros, 
            width=120
        )
        
        # Load existing data if available
        self.cargar_datos()

    def solo_letras_espacios_comas(self, e):
        texto = e.control.value

        # Filtrar: solo letras, espacios y comas
        texto_filtrado = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ ,]", "", texto)

        # Aplicar formato según el campo
        if e.control == self.cliente_field:
            # Capitaliza cada palabra
            texto_formateado = " ".join(p.capitalize() for p in texto_filtrado.split(" "))
        else:
            # Solo la primera letra en mayúscula, el resto en minúscula
            texto_formateado = texto_filtrado.strip().capitalize()

        e.control.value = texto_formateado
        e.control.update()

    def solo_numeros(self, e):
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
        self.page.update()

    def solo_numeros_y_barra(self, e):
        campo = e.control
        campo.value = "".join(c for c in campo.value if c.isdigit() or c == "/")
        self.page.update()

    def cargar_datos(self):
        """Load existing order data from database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if order exists
            cursor.execute("""
                SELECT * FROM OrdenPedido WHERE documento_cliente = ?
            """, (self.documento_cliente,))
            
            resultado = cursor.fetchone()
            if resultado:
                # Load data into form fields
                self.cantidad_pedidos.value = str(resultado[1] or "")
                self.cantidad_unidades.value = str(resultado[2] or "")
                self.cliente_field.value = str(resultado[3] or "")
                self.publicidad_field.value = str(resultado[4] or "")
                self.trabajo_field.value = str(resultado[5] or "")
                self.cantidad_colores.value = str(resultado[6] or "")
                
                # Load details (assuming they're stored as comma-separated values)
                detalles_str = resultado[7] or ""
                detalles_list = detalles_str.split("|||") if detalles_str else [""] * 6
                for i, detalle in enumerate(detalles_list[:6]):
                    if i < len(self.detalles):
                        self.detalles[i].value = detalle
                
                self.impresion_field.value = str(resultado[8] or "")
                self.termoformar_switch.value = bool(resultado[9])
                self.material_dropdown.value = str(resultado[10] or "")
                self.cant_material.value = str(resultado[11] or "")
                self.ancho_pliego.value = str(resultado[12] or "")
                self.alto_pliego.value = str(resultado[13] or "")
                self.espesor_field.value = str(resultado[14] or "")
                self.troquelado_switch.value = bool(resultado[15])
                self.doblado_switch.value = bool(resultado[16])
                self.corte_switch.value = bool(resultado[17])
                self.cinta_bifaz_dropdown.value = str(resultado[18] or "")
                self.observaciones_field.value = str(resultado[19] or "")
                self.fecha_recepcion.value = str(resultado[20] or "")
                self.fecha_entrega.value = str(resultado[21] or "")
                self.imprimio_field.value = str(resultado[22] or "")
                self.cant_impresa.value = str(resultado[23] or "")
                
                self.page.update()
                print("Datos cargados exitosamente")
            
            conn.close()
            
        except Exception as ex:
            print(f"Error al cargar datos: {ex}")

    def guardar_pedido(self, e):
        """Save order data to database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS OrdenPedido (
                    documento_cliente TEXT PRIMARY KEY,
                    cantidad_pedidos INTEGER,
                    cantidad_unidades INTEGER,
                    cliente TEXT,
                    publicidad TEXT,
                    trabajo TEXT,
                    cantidad_colores INTEGER,
                    detalles TEXT,
                    impresion TEXT,
                    termoformar BOOLEAN,
                    material TEXT,
                    cant_material INTEGER,
                    ancho_pliego REAL,
                    alto_pliego REAL,
                    espesor REAL,
                    troquelado BOOLEAN,
                    doblado BOOLEAN,
                    corte BOOLEAN,
                    cinta_bifaz TEXT,
                    observaciones TEXT,
                    fecha_recepcion TEXT,
                    fecha_entrega TEXT,
                    imprimio TEXT,
                    cant_impresa INTEGER,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Prepare details as concatenated string
            detalles_str = "|||".join([detalle.value or "" for detalle in self.detalles])
            
            # Insert or replace order data
            cursor.execute("""
                INSERT OR REPLACE INTO OrdenPedido (
                    documento_cliente, cantidad_pedidos, cantidad_unidades, cliente, 
                    publicidad, trabajo, cantidad_colores, detalles, impresion, 
                    termoformar, material, cant_material, ancho_pliego, alto_pliego, 
                    espesor, troquelado, doblado, corte, cinta_bifaz, observaciones, 
                    fecha_recepcion, fecha_entrega, imprimio, cant_impresa
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.documento_cliente,
                int(self.cantidad_pedidos.value or 0),
                int(self.cantidad_unidades.value or 0),
                self.cliente_field.value or "",
                self.publicidad_field.value or "",
                self.trabajo_field.value or "",
                int(self.cantidad_colores.value or 0),
                detalles_str,
                self.impresion_field.value or "",
                self.termoformar_switch.value,
                self.material_dropdown.value or "",
                int(self.cant_material.value or 0),
                float(self.ancho_pliego.value or 0),
                float(self.alto_pliego.value or 0),
                float(self.espesor_field.value or 0),
                self.troquelado_switch.value,
                self.doblado_switch.value,
                self.corte_switch.value,
                self.cinta_bifaz_dropdown.value or "",
                self.observaciones_field.value or "",
                self.fecha_recepcion.value or "",
                self.fecha_entrega.value or "",
                self.imprimio_field.value or "",
                int(self.cant_impresa.value or 0)
            ))
            
            conn.commit()
            conn.close()
            
            # Show success message
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Pedido guardado exitosamente"),
                    bgcolor=ft.colors.GREEN
                )
            )
            print("Pedido guardado exitosamente")
            
        except Exception as ex:
            print(f"Error al guardar pedido: {ex}")
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Error al guardar: {ex}"),
                    bgcolor=ft.colors.RED
                )
            )

    def texto_bloque(self, texto, padding_left=60, padding_top=15, margin=None):
        return ft.Container(
            ft.Text(texto, size=17, color="#ffffff"),
            margin=margin if margin else ft.margin.only(left=20),
            padding=ft.padding.only(left=padding_left, top=padding_top),
            width=240,
            height=50,
            bgcolor="#1d4fe0",
            border_radius=ft.BorderRadius(top_left=30, top_right=0, bottom_left=30, bottom_right=0)
        )

    def view(self):
        self.page.title = "Orden de pedido"
        self.page.bgcolor = "#1976d2"
        self.page.scroll = "auto"
        self.page.padding = 0

        contenedor = ft.Container(
            content=ft.Text("Orden pedido", color="#ffffff", font_family="Times New Roman", size=30),
            padding=15,
            width=250,
            height=70,
            bgcolor="#122ecc",
            border_radius=ft.BorderRadius(0, 0, 0, 60)
        )

        Datos_columnas = ft.Column([
            contenedor,
            ft.Container(content=self.cliente_field, width=340, margin=ft.margin.only(left=30)),
            ft.Container(content=self.publicidad_field, width=340, margin=ft.margin.only(left=30)),
            ft.Container(content=self.trabajo_field, width=340, margin=ft.margin.only(left=30))
        ], spacing=30)

        columna = ft.Column([
            ft.Row([self.texto_bloque("Cantidad de pedidos"), self.cantidad_pedidos]),
            ft.Row([self.texto_bloque("Cantidad Unidad/es"), self.cantidad_unidades])
        ], spacing=20)

        datos_fila = ft.Row([Datos_columnas, columna], spacing=100)

        entry_fila2 = ft.Row([
            self.texto_bloque("Cantidad de colores", padding_left=14),
            ft.Container(self.cantidad_colores)
        ])

        lista2 = ft.Column([
            self.texto_bloque("Detalles:", padding_left=60),
            *[ft.Container(detalle, margin=ft.margin.only(left=120)) for detalle in self.detalles]
        ], spacing=10)

        lista3 = ft.Row([
            self.texto_bloque("Imprecion", padding_left=60),
            ft.Container(self.impresion_field)
        ])

        switch_opcion = ft.Container(
            content=ft.Row([
                ft.Text("Termoformar/Doblar", size=18, color="#ffffff"),
                self.termoformar_switch,
            ], alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=10
        )

        lista4 = ft.Row([
            self.texto_bloque("Material", padding_left=60),
            self.material_dropdown,
            self.texto_bloque("Cant. Material", padding_left=40, margin=ft.margin.only(left=400)),
            ft.Container(self.cant_material)
        ])

        lista5 = ft.Row([
            self.texto_bloque("Med. pliego", padding_left=40),
            ft.Container(self.ancho_pliego),
            ft.Container(self.alto_pliego),
            self.texto_bloque("Espesor", padding_left=70, margin=ft.margin.only(left=350)),
            ft.Container(self.espesor_field)
        ])

        lista6 = ft.Row([
            *[
                ft.Container(ft.Row([
                    ft.Text(texto, size=18, color="#ffffff"),
                    switch
                ]), padding=10) for texto, switch in [
                    ("Troquelado", self.troquelado_switch), 
                    ("Doblado", self.doblado_switch), 
                    ("Corte", self.corte_switch)
                ]
            ],
            ft.Row([
                self.texto_bloque("Cinta bifaz", padding_left=60),
                self.cinta_bifaz_dropdown
            ])
        ], spacing=80)

        datos_fila2 = ft.Row([
            self.texto_bloque("Observaciones", padding_left=40),
            ft.Container(self.observaciones_field, width=600)
        ], alignment=ft.MainAxisAlignment.CENTER)

        lista7 = ft.Row([
            ft.Row([self.texto_bloque("Fecha recepcion", padding_left=40), ft.Container(self.fecha_recepcion)]),
            ft.Row([self.texto_bloque("Fecha entrega", padding_left=50), ft.Container(self.fecha_entrega)])
        ], spacing=500)

        lista8 = ft.Row([
            self.texto_bloque("Firma", padding_left=60, margin=ft.margin.only(bottom=40)),
            ft.Container(
                bgcolor="#1976d2",
                content=ft.Row([
                    self.texto_bloque("Imprimio", padding_left=50, margin=ft.margin.only(bottom=40)),
                    ft.Container(self.imprimio_field, margin=ft.margin.only(bottom=40))
                ]),
            ),
            ft.Container(
                bgcolor="#1976d2",
                content=ft.Row([
                    self.texto_bloque("Cant. Impresa", padding_left=40, margin=ft.margin.only(bottom=40)),
                    ft.Container(self.cant_impresa, margin=ft.margin.only(bottom=40))
                ])
            ),
        ], spacing=110)

        botones_finales = ft.Row([
            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/costos"), bgcolor="white"),
            ft.ElevatedButton("Guardar Pedido", on_click=self.guardar_pedido, bgcolor="green", color="white"),
            ft.ElevatedButton("Cancelar", on_click=lambda e: self.page.go("/clientes"), bgcolor="red", color="white"),
        ], alignment=ft.MainAxisAlignment.END)

        separador = ft.Divider(color=ft.Colors.BLUE_GREY_200)

        return ft.View(
            route="/orden_pedido",
            scroll=ft.ScrollMode.ALWAYS,
            bgcolor="#1976d2",
            controls=[
                ft.Column([
                    datos_fila, separador, entry_fila2, lista2, lista3, switch_opcion,
                    separador, lista4, lista5, lista6, datos_fila2, separador,
                    lista7, lista8, botones_finales
                ])
            ]
        )

