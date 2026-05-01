from conexion_bd import get_connection

class UtilidadesBaseDatos:
    """Utilidades para manejo de base de datos del sistema de serigrafía"""
    
    @staticmethod
    def crear_todas_las_tablas():
        """Crear todas las tablas necesarias para el sistema"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Tabla de órdenes de pedido (ya creada en orden_pedido_mejorado.py)
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
            
            # Tabla de costos detallados
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS costos_detallados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento_cliente TEXT UNIQUE,
                    varios REAL DEFAULT 0,
                    material REAL DEFAULT 0,
                    valor_pelicula REAL DEFAULT 0,
                    valor_tinta REAL DEFAULT 0,
                    shablon REAL DEFAULT 0,
                    barniz REAL DEFAULT 0,
                    valor_corte REAL DEFAULT 0,
                    valor_troquel REAL DEFAULT 0,
                    valor_armado REAL DEFAULT 0,
                    valor_troquelado REAL DEFAULT 0,
                    valor_doblado REAL DEFAULT 0,
                    aplicacion_cinta REAL DEFAULT 0,
                    cantidad_horas REAL DEFAULT 0,
                    cantidad_empleados INTEGER DEFAULT 0,
                    costo_mano_obra REAL DEFAULT 0,
                    subtotal REAL DEFAULT 0,
                    margen_porcentaje REAL DEFAULT 0,
                    total_ventas REAL DEFAULT 0,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (documento_cliente) REFERENCES clientes(Documento)
                )
            """)
            
            # Tabla de historial de cambios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial_cambios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento_cliente TEXT,
                    tabla_afectada TEXT,
                    tipo_cambio TEXT, -- INSERT, UPDATE, DELETE
                    datos_anteriores TEXT,
                    datos_nuevos TEXT,
                    usuario TEXT,
                    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (documento_cliente) REFERENCES clientes(Documento)
                )
            """)
            
            conn.commit()
            conn.close()
            print("Todas las tablas creadas/verificadas exitosamente")
            
        except Exception as ex:
            print("Error al crear tablas:", ex)

    @staticmethod
    def obtener_datos_completos_cliente(documento_cliente):
        """Obtener todos los datos de un cliente de todas las tablas"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            datos_completos = {}
            
            # Datos básicos del cliente
            cursor.execute("SELECT * FROM clientes WHERE Documento = ?", (documento_cliente,))
            cliente = cursor.fetchone()
            if cliente:
                datos_completos['cliente'] = dict(zip([col[0] for col in cursor.description], cliente))
            
            # Datos de pliegues
            cursor.execute("SELECT * FROM Pliegues WHERE Documento = ?", (documento_cliente,))
            pliegues = cursor.fetchone()
            if pliegues:
                datos_completos['pliegues'] = dict(zip([col[0] for col in cursor.description], pliegues))
            
            # Datos de materiales
            cursor.execute("SELECT * FROM Materiales WHERE Documento = ?", (documento_cliente,))
            materiales = cursor.fetchone()
            if materiales:
                datos_completos['materiales'] = dict(zip([col[0] for col in cursor.description], materiales))
            
            # Datos de costos detallados
            cursor.execute("SELECT * FROM costos_detallados WHERE documento_cliente = ?", (documento_cliente,))
            costos = cursor.fetchone()
            if costos:
                datos_completos['costos_detallados'] = dict(zip([col[0] for col in cursor.description], costos))
            
            # Órdenes de pedido
            cursor.execute("SELECT * FROM ordenes_pedido WHERE documento_cliente = ? ORDER BY fecha_creacion DESC", (documento_cliente,))
            ordenes = cursor.fetchall()
            if ordenes:
                datos_completos['ordenes_pedido'] = [dict(zip([col[0] for col in cursor.description], orden)) for orden in ordenes]
            
            conn.close()
            return datos_completos
            
        except Exception as ex:
            print("Error al obtener datos completos del cliente:", ex)
            return None

    @staticmethod
    def eliminar_datos_cliente(documento_cliente):
        """Eliminar todos los datos de un cliente de todas las tablas"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Eliminar en orden para evitar problemas de foreign key
            tablas = ['historial_cambios', 'ordenes_pedido', 'costos_detallados', 'Materiales', 'Pliegues', 'clientes']
            
            for tabla in tablas:
                if tabla == 'clientes':
                    cursor.execute(f"DELETE FROM {tabla} WHERE Documento = ?", (documento_cliente,))
                else:
                    cursor.execute(f"DELETE FROM {tabla} WHERE documento_cliente = ?", (documento_cliente,))
            
            conn.commit()
            conn.close()
            print(f"Todos los datos del cliente {documento_cliente} eliminados exitosamente")
            return True
            
        except Exception as ex:
            print("Error al eliminar datos del cliente:", ex)
            return False

    @staticmethod
    def exportar_datos_cliente(documento_cliente):
        """Exportar todos los datos de un cliente a un diccionario"""
        datos = UtilidadesBaseDatos.obtener_datos_completos_cliente(documento_cliente)
        if datos:
            return {
                'documento': documento_cliente,
                'fecha_exportacion': 'CURRENT_TIMESTAMP',
                'datos': datos
            }
        return None

    @staticmethod
    def verificar_integridad_datos():
        """Verificar la integridad de los datos en la base de datos"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            problemas = []
            
            # Verificar clientes sin datos en otras tablas
            cursor.execute("""
                SELECT c.Documento, c.nombre 
                FROM clientes c 
                LEFT JOIN Pliegues p ON c.Documento = p.Documento 
                WHERE p.Documento IS NULL
            """)
            clientes_sin_pliegues = cursor.fetchall()
            if clientes_sin_pliegues:
                problemas.append(f"Clientes sin datos de pliegues: {len(clientes_sin_pliegues)}")
            
            # Verificar datos huérfanos
            cursor.execute("""
                SELECT p.Documento 
                FROM Pliegues p 
                LEFT JOIN clientes c ON p.Documento = c.Documento 
                WHERE c.Documento IS NULL
            """)
            pliegues_huerfanos = cursor.fetchall()
            if pliegues_huerfanos:
                problemas.append(f"Datos de pliegues huérfanos: {len(pliegues_huerfanos)}")
            
            conn.close()
            
            if problemas:
                return {'integridad': False, 'problemas': problemas}
            else:
                return {'integridad': True, 'mensaje': 'Base de datos íntegra'}
                
        except Exception as ex:
            return {'integridad': False, 'error': str(ex)}
