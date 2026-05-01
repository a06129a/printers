import flet as ft
from conexion_bd import get_connection
import re

class FuncionesCostos:
    """Funciones auxiliares para manejo de datos de costos"""
    
    @staticmethod
    def crear_tabla_costos_detallados():
        """Crear tabla para costos más detallados si no existe"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS costos_detallados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento_cliente TEXT UNIQUE,
                    
                    -- Costos básicos
                    varios REAL DEFAULT 0,
                    material REAL DEFAULT 0,
                    valor_pelicula REAL DEFAULT 0,
                    valor_tinta REAL DEFAULT 0,
                    shablon REAL DEFAULT 0,
                    barniz REAL DEFAULT 0,
                    
                    -- Procesos
                    valor_corte REAL DEFAULT 0,
                    valor_troquel REAL DEFAULT 0,
                    valor_armado REAL DEFAULT 0,
                    valor_troquelado REAL DEFAULT 0,
                    valor_doblado REAL DEFAULT 0,
                    aplicacion_cinta REAL DEFAULT 0,
                    
                    -- Mano de obra
                    cantidad_horas REAL DEFAULT 0,
                    cantidad_empleados INTEGER DEFAULT 0,
                    costo_mano_obra REAL DEFAULT 0,
                    
                    -- Totales
                    subtotal REAL DEFAULT 0,
                    margen_porcentaje REAL DEFAULT 0,
                    total_ventas REAL DEFAULT 0,
                    
                    -- Metadatos
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (documento_cliente) REFERENCES clientes(Documento)
                )
            """)
            
            conn.commit()
            conn.close()
            print("Tabla costos_detallados creada/verificada exitosamente")
            
        except Exception as ex:
            print("Error al crear tabla costos_detallados:", ex)

    @staticmethod
    def cargar_costos_completos(documento_cliente):
        """Cargar todos los costos de un cliente"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Primero intentar cargar de costos_detallados
            cursor.execute("""
                SELECT * FROM costos_detallados WHERE documento_cliente = ?
            """, (documento_cliente,))
            
            resultado_detallado = cursor.fetchone()
            
            if resultado_detallado:
                conn.close()
                return {
                    'varios': resultado_detallado[2],
                    'material': resultado_detallado[3],
                    'valor_pelicula': resultado_detallado[4],
                    'valor_tinta': resultado_detallado[5],
                    'shablon': resultado_detallado[6],
                    'barniz': resultado_detallado[7],
                    'valor_corte': resultado_detallado[8],
                    'valor_troquel': resultado_detallado[9],
                    'valor_armado': resultado_detallado[10],
                    'valor_troquelado': resultado_detallado[11],
                    'valor_doblado': resultado_detallado[12],
                    'aplicacion_cinta': resultado_detallado[13],
                    'cantidad_horas': resultado_detallado[14],
                    'cantidad_empleados': resultado_detallado[15],
                    'costo_mano_obra': resultado_detallado[16],
                    'subtotal': resultado_detallado[17],
                    'margen_porcentaje': resultado_detallado[18],
                    'total_ventas': resultado_detallado[19]
                }
            
            # Si no existe en costos_detallados, cargar de clientes
            cursor.execute("""
                SELECT 
                    Varios, Material, Valor_Pelicula, Valor_Tinta, Shablon, Barniz,
                    Vlor_Corte, Valor_Troquel, Valor_Armado, Valor_Troquelado, 
                    Valor_Doblado, Aplicacion_Cinta, Cantidad_Horas, Cantidad_Empleados
                FROM clientes
                WHERE Documento = ?
            """, (documento_cliente,))
            
            resultado_basico = cursor.fetchone()
            conn.close()
            
            if resultado_basico:
                return {
                    'varios': resultado_basico[0] or 0,
                    'material': resultado_basico[1] or 0,
                    'valor_pelicula': resultado_basico[2] or 0,
                    'valor_tinta': resultado_basico[3] or 0,
                    'shablon': resultado_basico[4] or 0,
                    'barniz': resultado_basico[5] or 0,
                    'valor_corte': resultado_basico[6] or 0,
                    'valor_troquel': resultado_basico[7] or 0,
                    'valor_armado': resultado_basico[8] or 0,
                    'valor_troquelado': resultado_basico[9] or 0,
                    'valor_doblado': resultado_basico[10] or 0,
                    'aplicacion_cinta': resultado_basico[11] or 0,
                    'cantidad_horas': resultado_basico[12] or 0,
                    'cantidad_empleados': resultado_basico[13] or 0,
                    'costo_mano_obra': 0,
                    'subtotal': 0,
                    'margen_porcentaje': 0,
                    'total_ventas': 0
                }
            
            return None
            
        except Exception as ex:
            print("Error al cargar costos completos:", ex)
            return None

    @staticmethod
    def guardar_costos_completos(documento_cliente, datos_costos):
        """Guardar costos completos en la base de datos"""
        try:
            FuncionesCostos.crear_tabla_costos_detallados()
            
            conn = get_connection()
            cursor = conn.cursor()
            
            # Calcular totales automáticamente
            subtotal = sum([
                float(datos_costos.get('varios', 0) or 0),
                float(datos_costos.get('material', 0) or 0),
                float(datos_costos.get('valor_pelicula', 0) or 0),
                float(datos_costos.get('valor_tinta', 0) or 0),
                float(datos_costos.get('shablon', 0) or 0),
                float(datos_costos.get('barniz', 0) or 0),
                float(datos_costos.get('valor_corte', 0) or 0),
                float(datos_costos.get('valor_troquel', 0) or 0),
                float(datos_costos.get('valor_armado', 0) or 0),
                float(datos_costos.get('valor_troquelado', 0) or 0),
                float(datos_costos.get('valor_doblado', 0) or 0),
                float(datos_costos.get('aplicacion_cinta', 0) or 0),
                float(datos_costos.get('costo_mano_obra', 0) or 0)
            ])
            
            margen = float(datos_costos.get('margen_porcentaje', 0) or 0)
            total_ventas = subtotal * (1 + margen / 100)
            
            # Insertar o actualizar en costos_detallados
            cursor.execute("""
                INSERT OR REPLACE INTO costos_detallados (
                    documento_cliente, varios, material, valor_pelicula, valor_tinta,
                    shablon, barniz, valor_corte, valor_troquel, valor_armado,
                    valor_troquelado, valor_doblado, aplicacion_cinta,
                    cantidad_horas, cantidad_empleados, costo_mano_obra,
                    subtotal, margen_porcentaje, total_ventas
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                documento_cliente,
                float(datos_costos.get('varios', 0) or 0),
                float(datos_costos.get('material', 0) or 0),
                float(datos_costos.get('valor_pelicula', 0) or 0),
                float(datos_costos.get('valor_tinta', 0) or 0),
                float(datos_costos.get('shablon', 0) or 0),
                float(datos_costos.get('barniz', 0) or 0),
                float(datos_costos.get('valor_corte', 0) or 0),
                float(datos_costos.get('valor_troquel', 0) or 0),
                float(datos_costos.get('valor_armado', 0) or 0),
                float(datos_costos.get('valor_troquelado', 0) or 0),
                float(datos_costos.get('valor_doblado', 0) or 0),
                float(datos_costos.get('aplicacion_cinta', 0) or 0),
                float(datos_costos.get('cantidad_horas', 0) or 0),
                int(datos_costos.get('cantidad_empleados', 0) or 0),
                float(datos_costos.get('costo_mano_obra', 0) or 0),
                subtotal,
                margen,
                total_ventas
            ))
            
            # También actualizar en la tabla clientes para compatibilidad
            cursor.execute("""
                UPDATE clientes SET
                    Varios = ?, Material = ?, Valor_Pelicula = ?, Valor_Tinta = ?,
                    Shablon = ?, Barniz = ?, Vlor_Corte = ?, Valor_Troquel = ?,
                    Valor_Armado = ?, Valor_Troquelado = ?, Valor_Doblado = ?,
                    Aplicacion_Cinta = ?, Cantidad_Horas = ?, Cantidad_Empleados = ?,
                    fecha_ultima_edicion = CURRENT_DATE
                WHERE Documento = ?
            """, (
                float(datos_costos.get('varios', 0) or 0),
                float(datos_costos.get('material', 0) or 0),
                float(datos_costos.get('valor_pelicula', 0) or 0),
                float(datos_costos.get('valor_tinta', 0) or 0),
                float(datos_costos.get('shablon', 0) or 0),
                bool(datos_costos.get('barniz', False)),
                float(datos_costos.get('valor_corte', 0) or 0),
                float(datos_costos.get('valor_troquel', 0) or 0),
                float(datos_costos.get('valor_armado', 0) or 0),
                float(datos_costos.get('valor_troquelado', 0) or 0),
                float(datos_costos.get('valor_doblado', 0) or 0),
                bool(datos_costos.get('aplicacion_cinta', False)),
                float(datos_costos.get('cantidad_horas', 0) or 0),
                int(datos_costos.get('cantidad_empleados', 0) or 0),
                documento_cliente
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'subtotal': subtotal,
                'total_ventas': total_ventas,
                'success': True
            }
            
        except Exception as ex:
            print("Error al guardar costos completos:", ex)
            return {'success': False, 'error': str(ex)}

    @staticmethod
    def calcular_costo_mano_obra(cantidad_empleados, cantidad_horas, jornal_por_hora=1000):
        """Calcular costo de mano de obra"""
        try:
            empleados = int(cantidad_empleados or 0)
            horas = float(cantidad_horas or 0)
            jornal = float(jornal_por_hora)
            
            return empleados * horas * jornal
        except:
            return 0

    @staticmethod
    def obtener_resumen_costos(documento_cliente):
        """Obtener resumen de todos los costos de un cliente"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Obtener datos de costos detallados
            cursor.execute("""
                SELECT subtotal, margen_porcentaje, total_ventas 
                FROM costos_detallados 
                WHERE documento_cliente = ?
            """, (documento_cliente,))
            
            resultado_costos = cursor.fetchone()
            
            # Obtener datos de materiales (Pantalla7)
            cursor.execute("""
                SELECT 
                    Costo_material_Pe, Costo_impresion_Costo_Final, 
                    Costo_tinta_Costo_final, Costo_mano_de_obra,
                    Costo_cinta_Costo, Costo_barniz_Costo_Finalxcm
                FROM Materiales 
                WHERE Documento = ?
            """, (documento_cliente,))
            
            resultado_materiales = cursor.fetchone()
            
            # Obtener datos de pliegues
            cursor.execute("""
                SELECT Impre_Pliegos, Impre_Pasadas, Unidad_Superficie
                FROM Pliegues 
                WHERE Documento = ?
            """, (documento_cliente,))
            
            resultado_pliegues = cursor.fetchone()
            
            conn.close()
            
            resumen = {
                'costos_generales': {
                    'subtotal': resultado_costos[0] if resultado_costos else 0,
                    'margen': resultado_costos[1] if resultado_costos else 0,
                    'total_ventas': resultado_costos[2] if resultado_costos else 0
                },
                'costos_materiales': {
                    'costo_pelicula': resultado_materiales[0] if resultado_materiales else 0,
                    'costo_impresion': resultado_materiales[1] if resultado_materiales else 0,
                    'costo_tinta': resultado_materiales[2] if resultado_materiales else 0,
                    'costo_mano_obra': resultado_materiales[3] if resultado_materiales else 0,
                    'costo_cinta': resultado_materiales[4] if resultado_materiales else 0,
                    'costo_barniz': resultado_materiales[5] if resultado_materiales else 0
                },
                'datos_produccion': {
                    'pliegos': resultado_pliegues[0] if resultado_pliegues else 0,
                    'pasadas': resultado_pliegues[1] if resultado_pliegues else 0,
                    'superficie': resultado_pliegues[2] if resultado_pliegues else 0
                }
            }
            
            return resumen
            
        except Exception as ex:
            print("Error al obtener resumen de costos:", ex)
            return None
