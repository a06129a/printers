import flet as ft
from conexion_bd import get_connection

class OrdenPedidoView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.documento_cliente = self.page.client_storage.get("documento_cliente")
        
        # Inicializar todos los campos como atributos de la clase
        self.init_fields()

    def init_fields(self):
        """Inicializar todos los campos de entrada"""
        self.cantidad_pedidos = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        self.cliente_field = ft.TextField(label="Cliente", bgcolor="#ffffff")
        self.publicidad_field = ft.TextField(label="Publicidad", bgcolor="#ffffff")
        self.trabajo_field = ft.TextField(label="Trabajo", bgcolor="#ffffff")
        self.cantidad_unidades = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        self.cantidad_colores = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        
        # Campos de detalles (6 campos)
        self.detalles = [ft.TextField(label=f"{i+1}-", bgcolor="#ffffff", width=450) for i in range(6)]
        
        self.impresion_field = ft.TextField(bgcolor="#ffffff", width=320)
        self.termoformar_switch = ft.Switch(value=False)
        
        self.material_dropdown = ft.Dropdown(
            label="Selecciona una opción",
            width=200,
            label_style=ft.TextStyle(color="white"),
            options=[
                ft.dropdown.Option("Cartón"),
                ft.dropdown.Option("Plástico"),
                ft.dropdown.Option("Papel")
            ]
        )
        
        self.cant_material = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        self.ancho_pliego = ft.TextField(label="Ancho-cm", bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        self.alto_pliego = ft.TextField(label="Alto-cm", bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        self.espesor_field = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros, width=120)
        
        # Switches para procesos
        self.troquelado_switch = ft.Switch(value=False)
        self.doblado_switch = ft.Switch(value=False)
        self.corte_switch = ft.Switch(value=False)
        
        self.cinta_bifaz_dropdown = ft.Dropdown(
            label="Selecciona una opción", 
            width=200, 
            label_style=ft.TextStyle(color="white"), 
            options=[
                ft.dropdown.Option("3M"),
                ft.dropdown.Option("Scotch"),
                ft.dropdown.Option("Genérica")
            ]
        )
        
        self.observaciones_field = ft.TextField(
            bgcolor="#ffffff", 
            multiline=True, 
            max_lines=4, 
            hint_text="Escribe aquí todos los detalles..."
        )
        
        self.fecha_recepcion = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros_y_barra, width=120)
        self.fecha_entrega = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros_y_barra, width=120)
        self.imprimio_field = ft.TextField(bgcolor="#ffffff", width=200)
        self.cant_impresa = ft.TextField(bgcolor="#ffffff", on_change=self.solo_numeros, width=120)

    def cargar_datos_orden(self):
        """Cargar datos existentes de la orden de pedido"""
        if not self.documento_cliente:
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ordenes_pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento_cliente TEXT,
                    cliente TEXT,
                    publicidad TEXT,
                    trabajo TEXT,
                    cantidad_pedidos INTEGER,
                    cantidad_unidades INTEGER,
                    cantidad_colores INTEGER,
                    detalle_1 TEXT,
                    detalle_2 TEXT,
                    detalle_3 TEXT,
                    detalle_4 TEXT,
                    detalle_5 TEXT,
                    detalle_6 TEXT,
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
            
            # Buscar datos existentes
            cursor.execute("""
                SELECT * FROM ordenes_pedido 
                WHERE documento_cliente = ? 
                ORDER BY fecha_creacion DESC 
                LIMIT 1
            """, (self.documento_cliente,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                # Cargar datos en los campos
                self.cliente_field.value = resultado[2] or ""
                self.publicidad_field.value = resultado[3] or ""
                self.trabajo_field.value = resultado[4] or ""
                self.cantidad_pedidos.value = str(resultado[5] or "")
                self.cantidad_unidades.value = str(resultado[6] or "")
                self.cantidad_colores.value = str(resultado[7] or "")
                
                # Cargar detalles
                for i in range(6):
                    self.detalles[i].value = resultado[8 + i] or ""
                
                self.impresion_field.value = resultado[14] or ""
                self.termoformar_switch.value = bool(resultado[15])
                self.material_dropdown.value = resultado[16] or ""
                self.cant_material.value = str(resultado[17] or "")
                self.ancho_pliego.value = str(resultado[18] or "")
                self.alto_pliego.value = str(resultado[19] or "")
                self.espesor_field.value = str(resultado[20] or "")
                self.troquelado_switch.value = bool(resultado[21])
                self.doblado_switch.value = bool(resultado[22])
                self.corte_switch.value = bool(resultado[23])
                self.cinta_bifaz_dropdown.value = resultado[24] or ""
                self.observaciones_field.value = resultado[25] or ""
                self.fecha_recepcion.value = resultado[26] or ""
                self.fecha_entrega.value = resultado[27] or ""
                self.imprimio_field.value = resultado[28] or ""
                self.cant_impresa.value = str(resultado[29] or "")
                
                print("Datos de orden cargados exitosamente")
            
            conn.close()
            self.page.update()
            
        except Exception as ex:
            print("Error al cargar datos de orden:", ex)

    def guardar_orden_pedido(self, e):
        """Guardar datos de la orden de pedido"""
        if not self.documento_cliente:
            print("No hay documento de cliente")
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Insertar o actualizar datos
            cursor.execute("""
                INSERT OR REPLACE INTO ordenes_pedido (
                    documento_cliente, cliente, publicidad, trabajo,
                    cantidad_pedidos, cantidad_unidades, cantidad_colores,
                    detalle_1, detalle_2, detalle_3, detalle_4, detalle_5, detalle_6,
                    impresion, termoformar, material, cant_material,
                    ancho_pliego, alto_pliego, espesor,
                    troquelado, doblado, corte, cinta_bifaz,
                    observaciones, fecha_recepcion, fecha_entrega,
                    imprimio, cant_impresa
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.documento_cliente,
                self.cliente_field.value or "",
                self.publicidad_field.value or "",
                self.trabajo_field.value or "",
                int(self.cantidad_pedidos.value or 0),
                int(self.cantidad_unidades.value or 0),
                int(self.cantidad_colores.value or 0),
                self.detalles[0].value or "",
                self.detalles[1].value or "",
                self.detalles[2].value or "",
                self.detalles[3].value or "",
                self.detalles[4].value or "",
                self.detalles[5].value or "",
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
            
            # Mostrar mensaje de éxito
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Orden de pedido guardada exitosamente"),
                bgcolor="green"
            )
            self.page.snack_bar.open = True
            self.page.update()
            
            print("Orden de pedido guardada exitosamente")
            
        except Exception as ex:
            print("Error al guardar orden de pedido:", ex)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al guardar: {ex}"),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def solo_numeros(self, e):
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
        self.page.update()

    def solo_numeros_y_barra(self, e):
        campo = e.control
        campo.value = "".join(c for c in campo.value if c.isdigit() or c == "/")
        self.page.update()

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
        
        # Cargar datos existentes al crear la vista
        self.cargar_datos_orden()

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
            self.texto_bloque("Impresion", padding_left=60),
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
            ft.ElevatedButton("Guardar Pedido", on_click=self.guardar_orden_pedido, bgcolor="green", color="white"),
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
