import pygame
import random
import sys
import os
import math
import json
from datetime import datetime

def resource_path(relative_path):
    """Función para rutas compatibles con Linux y Windows"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    path = os.path.join(base_path, relative_path)
    return os.path.normpath(path)

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    try:
        pygame.init()
        return True
    except Exception as e:
        print(f"Error inicializando Pygame: {e}")
        return False

# Inicializar Pygame con verificación
if not verificar_dependencias():
    print("Error: Pygame no está instalado correctamente.")
    print("Instala con: sudo apt install python3-pygame")
    sys.exit(1)

# Constantes del juego
ANCHO, ALTO = 1200, 800
TAMANIO_CELDA = 60
MARGEN_X = (ANCHO - 9 * TAMANIO_CELDA) // 2
MARGEN_Y = (ALTO - 9 * TAMANIO_CELDA) // 2 - 50

FPS = 60

# Colores - ESQUEMA MÁS MODERNO Y ELEGANTE
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_OSCURO = (40, 40, 40)
GRIS_MEDIO = (100, 100, 100)
GRIS_CLARO = (200, 200, 200)
COLOR_BOTON = (70, 130, 180)
COLOR_BOTON_HOVER = (100, 160, 210)
COLOR_FONDO = (15, 25, 35)
COLOR_TABLERO = (245, 245, 245)
COLOR_BORDE = (30, 30, 30)
COLOR_TEXTO = (30, 30, 30)
COLOR_CELDA_SELECCIONADA = (100, 180, 255, 100)
COLOR_NUMERO_USUARIO = (0, 100, 200)
COLOR_NUMERO_ORIGINAL = (30, 30, 30)
COLOR_CONFLICTO = (255, 100, 100, 150)
COLOR_CELDA_VALIDA = (100, 200, 100, 80)
COLOR_NOTA = (150, 150, 150, 120)
COLOR_VERDE = (0, 180, 0)
COLOR_ROJO = (220, 0, 0)
COLOR_AMARILLO = (255, 200, 0)
COLOR_NARANJA = (255, 140, 0)
COLOR_PURPURA = (180, 0, 180)
COLOR_ROSA = (255, 100, 180)

# Crear pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sudoku Premium - Juego Profesional")

# Variables globales para fuentes
fuente = None
fuente_grande = None
fuente_pista = None

# Cargar icono
def cargar_icono():
    """Cargar icono con formatos compatibles"""
    try:
        icono = pygame.Surface((32, 32))
        icono.fill(COLOR_FONDO)
        pygame.draw.rect(icono, COLOR_BOTON, (8, 8, 16, 16), 2)
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(icono, COLOR_TEXTO, (10 + i*5, 10 + j*5, 3, 3))
        pygame.display.set_icon(icono)
        print("Icono cargado")
        return True
    except Exception as e:
        print(f"No se pudo cargar icono: {e}")
        return False

cargar_icono()

# Sistema de partículas mejorado
particulas = []

class Particula:
    def __init__(self, x, y, tipo="confeti", color=None):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.life = random.uniform(60, 120)
        self.size = random.randint(2, 6)
        self.original_size = self.size
        
        if tipo == "brillo":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.gravity = 0.05
        elif tipo == "confeti":
            self.color = color or random.choice([
                (255, 50, 50), (50, 255, 50), (50, 50, 255), 
                (255, 255, 50), (255, 50, 255), (50, 255, 255),
                (255, 150, 50), (150, 50, 255)
            ])
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-8, -2)
            self.gravity = 0.2
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-5, 5)
        elif tipo == "estrellas":
            self.color = color or (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            self.gravity = 0.1
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-5, 5)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
        if self.tipo == "estrellas" or self.tipo == "confeti":
            self.rotation += self.rotation_speed
            
        self.size = max(1, self.original_size * (self.life / 120))
        self.life -= 1
        return self.life > 0
        
    def draw(self, pantalla):
        alpha = min(255, int(self.life * 2))
        
        if self.tipo == "estrellas":
            points = []
            for i in range(5):
                angle = self.rotation + i * 72
                rad = math.radians(angle)
                x = self.x + math.cos(rad) * self.size
                y = self.y + math.sin(rad) * self.size
                points.append((x, y))
                
                inner_angle = angle + 36
                inner_rad = math.radians(inner_angle)
                inner_x = self.x + math.cos(inner_rad) * (self.size / 2)
                inner_y = self.y + math.sin(inner_rad) * (self.size / 2)
                points.append((inner_x, inner_y))
            
            surf = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
            pygame.draw.polygon(surf, (*self.color, alpha), 
                               [(p[0] - self.x + self.size * 1.5, p[1] - self.y + self.size * 1.5) for p in points])
            pantalla.blit(surf, (self.x - self.size * 1.5, self.y - self.size * 1.5))
            
        elif self.tipo == "brillo":
            surf = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (self.size * 1.5, self.size * 1.5), self.size)
            pantalla.blit(surf, (self.x - self.size * 1.5, self.y - self.size * 1.5))
        else:
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            rotated_surf = pygame.transform.rotate(surf, self.rotation)
            pygame.draw.rect(rotated_surf, (*self.color, alpha), 
                           (self.size * 0.5, self.size * 0.5, self.size, self.size))
            pantalla.blit(rotated_surf, (self.x - self.size, self.y - self.size))

def crear_particulas(x, y, cantidad=50, tipo="confeti", color=None):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo, color))

# Botones
boton_pausa_rect = pygame.Rect(ANCHO - 80, 10, 32, 32)
boton_reiniciar_rect = pygame.Rect(ANCHO - 120, 10, 32, 32)

# ============================
# SISTEMA DE AUTO-GUARDADO
# ============================

class SistemaAutoguardado:
    def __init__(self):
        self.archivo_autoguardado = "autoguardado_sudoku.json"
        self.ultimo_autoguardado = 0
        self.intervalo_autoguardado = 120000  # 2 minutos en milisegundos
    
    def autoguardar_partida(self, juego):
        """Guarda el progreso automáticamente cada 2 minutos"""
        tiempo_actual = pygame.time.get_ticks()
        
        if (juego.estado_juego == "jugando" and not juego.pausa and 
            tiempo_actual - self.ultimo_autoguardado > self.intervalo_autoguardado):
            
            datos_autoguardado = {
                'tablero_completo': juego.tablero.tablero_completo,
                'tablero_juego': juego.tablero.tablero_juego,
                'tablero_usuario': juego.tablero.tablero_usuario,
                'tablero_notas': juego.tablero.tablero_notas,
                'celda_seleccionada': juego.tablero.celda_seleccionada,
                'estadisticas': {
                    'tiempo_inicio': juego.estadisticas.tiempo_inicio,
                    'tiempo_juego': juego.estadisticas.tiempo_juego,
                    'movimientos': juego.estadisticas.movimientos,
                    'errores': juego.estadisticas.errores,
                    'pistas_usadas': juego.estadisticas.pistas_usadas,
                    'nivel_dificultad': juego.estadisticas.nivel_dificultad
                },
                'config': {
                    'dificultad': juego.config.dificultad,
                    'mostrar_conflictos': juego.config.mostrar_conflictos,
                    'mostrar_pistas': juego.config.mostrar_pistas
                },
                'timestamp': datetime.now().isoformat(),
                'usuario': juego.usuarios.usuario_actual
            }
            
            try:
                with open(self.archivo_autoguardado, 'w') as f:
                    json.dump(datos_autoguardado, f, indent=2)
                self.ultimo_autoguardado = tiempo_actual
                print("Partida autoguardada correctamente")
                return True
            except Exception as e:
                print(f"Error en autoguardado: {e}")
        
        return False
    
    def cargar_autoguardado(self):
        """Carga la partida autoguardada si existe"""
        try:
            with open(self.archivo_autoguardado, 'r') as f:
                datos = json.load(f)
            return datos
        except:
            return None
    
    def existe_autoguardado(self):
        """Verifica si existe una partida autoguardada"""
        return os.path.exists(self.archivo_autoguardado)
    
    def eliminar_autoguardado(self):
        """Elimina el archivo de autoguardado"""
        try:
            if os.path.exists(self.archivo_autoguardado):
                os.remove(self.archivo_autoguardado)
                return True
        except:
            pass
        return False

# ============================
# SISTEMA DE PISTAS INTELIGENTES
# ============================

class SistemaPistasInteligentes:
    def __init__(self):
        self.ultima_pista = None
    
    def obtener_pista_inteligente(self, tablero):
        """Analiza el tablero y sugiere la celda más fácil de resolver"""
        # Buscar celdas con una sola posibilidad (más fáciles)
        pista = self._encontrar_celda_unica_posibilidad(tablero)
        if pista:
            return pista
        
        # Buscar números únicos en filas, columnas o cajas
        pista = self._encontrar_numero_unico(tablero)
        if pista:
            return pista
        
        # Buscar pares desnudos (naked pairs)
        pista = self._encontrar_pares_desnudos(tablero)
        if pista:
            return pista
        
        return None
    
    def _encontrar_celda_unica_posibilidad(self, tablero):
        """Encuentra celdas que solo tienen una posibilidad"""
        for fila in range(9):
            for col in range(9):
                if tablero.tablero_usuario[fila][col] == 0 and tablero.tablero_juego[fila][col] == 0:
                    posibilidades = self._obtener_posibilidades(tablero, fila, col)
                    if len(posibilidades) == 1:
                        return {
                            'tipo': 'unica_posibilidad',
                            'fila': fila,
                            'columna': col,
                            'numero': posibilidades[0],
                            'dificultad': 'fácil',
                            'explicacion': f'Esta celda solo puede contener el número {posibilidades[0]}'
                        }
        return None
    
    def _encontrar_numero_unico(self, tablero):
        """Encuentra números que solo pueden ir en una celda específica dentro de una fila/columna/caja"""
        for numero in range(1, 10):
            # Buscar en filas
            for fila in range(9):
                posiciones_validas = []
                for col in range(9):
                    if (tablero.tablero_usuario[fila][col] == 0 and 
                        tablero.tablero_juego[fila][col] == 0 and
                        self._es_numero_valido(tablero, fila, col, numero)):
                        posiciones_validas.append(col)
                
                if len(posiciones_validas) == 1:
                    return {
                        'tipo': 'numero_unico_fila',
                        'fila': fila,
                        'columna': posiciones_validas[0],
                        'numero': numero,
                        'dificultad': 'medio',
                        'explicacion': f'El número {numero} solo puede ir en esta posición en la fila {fila+1}'
                    }
            
            # Buscar en columnas
            for col in range(9):
                posiciones_validas = []
                for fila in range(9):
                    if (tablero.tablero_usuario[fila][col] == 0 and 
                        tablero.tablero_juego[fila][col] == 0 and
                        self._es_numero_valido(tablero, fila, col, numero)):
                        posiciones_validas.append(fila)
                
                if len(posiciones_validas) == 1:
                    return {
                        'tipo': 'numero_unico_columna',
                        'fila': posiciones_validas[0],
                        'columna': col,
                        'numero': numero,
                        'dificultad': 'medio',
                        'explicacion': f'El número {numero} solo puede ir en esta posición en la columna {col+1}'
                    }
        
        return None
    
    def _encontrar_pares_desnudos(self, tablero):
        """Busca pares desnudos en filas, columnas y cajas"""
        # Implementación simplificada de pares desnudos
        for fila in range(9):
            for col in range(9):
                if (tablero.tablero_usuario[fila][col] == 0 and 
                    tablero.tablero_juego[fila][col] == 0):
                    posibilidades = self._obtener_posibilidades(tablero, fila, col)
                    if len(posibilidades) == 2:
                        # Verificar si hay otra celda en la misma fila con las mismas dos posibilidades
                        for otra_col in range(9):
                            if (otra_col != col and 
                                tablero.tablero_usuario[fila][otra_col] == 0 and
                                tablero.tablero_juego[fila][otra_col] == 0):
                                otras_posibilidades = self._obtener_posibilidades(tablero, fila, otra_col)
                                if set(posibilidades) == set(otras_posibilidades):
                                    return {
                                        'tipo': 'par_desnudo',
                                        'fila': fila,
                                        'columna': col,
                                        'numero': None,
                                        'dificultad': 'difícil',
                                        'explicacion': f'Par desnudo encontrado: los números {posibilidades} deben ir en estas dos celdas'
                                    }
        return None
    
    def _obtener_posibilidades(self, tablero, fila, col):
        """Obtiene los números posibles para una celda"""
        posibilidades = []
        for num in range(1, 10):
            if self._es_numero_valido(tablero, fila, col, num):
                posibilidades.append(num)
        return posibilidades
    
    def _es_numero_valido(self, tablero, fila, col, num):
        """Verifica si un número es válido en una posición"""
        # Verificar fila
        for i in range(9):
            if tablero.tablero_usuario[fila][i] == num or tablero.tablero_juego[fila][i] == num:
                return False
        
        # Verificar columna
        for i in range(9):
            if tablero.tablero_usuario[i][col] == num or tablero.tablero_juego[i][col] == num:
                return False
        
        # Verificar caja 3x3
        inicio_fila = (fila // 3) * 3
        inicio_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if (tablero.tablero_usuario[inicio_fila + i][inicio_col + j] == num or 
                    tablero.tablero_juego[inicio_fila + i][inicio_col + j] == num):
                    return False
        
        return True

# ============================
# SISTEMA DE LOGROS
# ============================

LOGROS = {
    "primer_pasito": {
        "nombre": "Primer Pasito",
        "descripcion": "Completa tu primer Sudoku",
        "recompensa": "Tema Clásico Desbloqueado",
        "obtenido": False,
        "tipo": "progreso"
    },
    "velocista": {
        "nombre": "Velocista",
        "descripcion": "Completa un Sudoku en menos de 5 minutos",
        "recompensa": "Tema Oscuro Desbloqueado",
        "obtenido": False,
        "tipo": "tiempo"
    },
    "perfeccionista": {
        "nombre": "Perfeccionista", 
        "descripcion": "Completa un Sudoku sin errores",
        "recompensa": "Tema Verde Desbloqueado",
        "obtenido": False,
        "tipo": "precision"
    },
    "coleccionista": {
        "nombre": "Coleccionista",
        "descripcion": "Completa 10 Sudokus diferentes",
        "recompensa": "Efectos de Partículas Mejorados",
        "obtenido": False,
        "tipo": "cantidad"
    },
    "estratega": {
        "nombre": "Estratega",
        "descripcion": "Usa 10 pistas inteligentes",
        "recompensa": "Pistas Ilimitadas por 1 día",
        "obtenido": False,
        "tipo": "pistas"
    }
}

class SistemaLogros:
    def __init__(self):
        self.archivo_logros = "logros_sudoku.json"
        self.logros = self.cargar_logros()
        self.logros_desbloqueados = []
    
    def cargar_logros(self):
        """Carga los logros desde archivo"""
        try:
            with open(self.archivo_logros, 'r') as f:
                datos = json.load(f)
                # Actualizar los logros base con los datos guardados
                for key, value in datos.items():
                    if key in LOGROS:
                        LOGROS[key]["obtenido"] = value.get("obtenido", False)
                return datos
        except:
            return LOGROS.copy()
    
    def guardar_logros(self):
        """Guarda el estado de los logros"""
        try:
            with open(self.archivo_logros, 'w') as f:
                json.dump(self.logros, f, indent=2)
        except Exception as e:
            print(f"Error guardando logros: {e}")
    
    def verificar_logro(self, tipo_logro, valor, juego):
        """Verifica si se ha desbloqueado algún logro"""
        logros_desbloqueados = []
        
        for key, logro in LOGROS.items():
            if not logro["obtenido"]:
                if logro["tipo"] == tipo_logro:
                    if tipo_logro == "progreso" and valor >= 1:
                        logro["obtenido"] = True
                        logros_desbloqueados.append(logro)
                    elif tipo_logro == "tiempo" and valor <= 300000:  # 5 minutos en milisegundos
                        logro["obtenido"] = True
                        logros_desbloqueados.append(logro)
                    elif tipo_logro == "precision" and valor == 0:
                        logro["obtenido"] = True
                        logros_desbloqueados.append(logro)
                    elif tipo_logro == "cantidad" and valor >= 10:
                        logro["obtenido"] = True
                        logros_desbloqueados.append(logro)
                    elif tipo_logro == "pistas" and valor >= 10:
                        logro["obtenido"] = True
                        logros_desbloqueados.append(logro)
        
        # Guardar y mostrar logros desbloqueados
        if logros_desbloqueados:
            self.logros = LOGROS.copy()
            self.guardar_logros()
            for logro in logros_desbloqueados:
                self.mostrar_logro_desbloqueado(logro, juego)
    
    def mostrar_logro_desbloqueado(self, logro, juego):
        """Muestra una notificación de logro desbloqueado"""
        juego.efectos.agregar_texto_flotante(
            f"¡Logro Desbloqueado: {logro['nombre']}!",
            ANCHO // 2,
            100,
            COLOR_AMARILLO
        )
        crear_particulas(ANCHO // 2, 150, 30, "estrellas", COLOR_AMARILLO)
        print(f"¡Logro desbloqueado: {logro['nombre']}!")

# ============================
# SISTEMA DE TEMAS
# ============================

TEMAS = {
    "Clásico": {
        "fondo": (15, 25, 35),
        "tablero": (245, 245, 245),
        "borde": (30, 30, 30),
        "numeros_originales": (30, 30, 30),
        "numeros_usuario": (0, 100, 200),
        "boton": (70, 130, 180),
        "boton_hover": (100, 160, 210),
        "texto": (30, 30, 30)
    },
    "Oscuro": {
        "fondo": (10, 10, 20),
        "tablero": (40, 40, 50),
        "borde": (70, 70, 90),
        "numeros_originales": (200, 200, 200),
        "numeros_usuario": (100, 180, 255),
        "boton": (50, 70, 90),
        "boton_hover": (70, 90, 110),
        "texto": (220, 220, 220)
    },
    "Verde": {
        "fondo": (20, 40, 30),
        "tablero": (230, 245, 230),
        "borde": (40, 80, 60),
        "numeros_originales": (30, 70, 40),
        "numeros_usuario": (0, 150, 100),
        "boton": (60, 120, 80),
        "boton_hover": (80, 140, 100),
        "texto": (30, 50, 40)
    }
}

class SistemaAudio:
    def __init__(self):
        self.sonidos = {}
        self.volumen_efectos = 0.3
        self.inicializar_sonidos_virtuales()
    
    def inicializar_sonidos_virtuales(self):
        """Crear sonidos básicos programáticamente"""
        print("Inicializando sistema de audio virtual...")
    
    def reproducir(self, nombre):
        """Reproducir efecto de sonido (implementación virtual)"""
        print(f"Sonido reproducido: {nombre}")

class Estadisticas:
    def __init__(self):
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_juego = 0
        self.movimientos = 0
        self.errores = 0
        self.pistas_usadas = 0
        self.pistas_inteligentes_usadas = 0
        self.nivel_dificultad = "Medio"
        self.max_errores = 3
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.partidas_completadas = 0
        self.movimientos_correctos = 0
        self.movimientos_totales = 0
        self.racha_victorias = 0
        self.mejor_racha = 0
        self.tiempo_total = 0
    
    def actualizar_tiempo(self):
        self.tiempo_juego = pygame.time.get_ticks() - self.tiempo_inicio
    
    def registrar_movimiento(self, correcto=False):
        self.movimientos += 1
        self.movimientos_totales += 1
        if correcto:
            self.movimientos_correctos += 1
    
    def registrar_error(self):
        self.errores += 1
        return self.errores >= self.max_errores
    
    def registrar_pista(self, inteligente=False):
        self.pistas_usadas += 1
        if inteligente:
            self.pistas_inteligentes_usadas += 1
    
    def registrar_victoria(self):
        self.partidas_ganadas += 1
        self.partidas_completadas += 1
        self.racha_victorias += 1
        self.tiempo_total += self.tiempo_juego
        if self.racha_victorias > self.mejor_racha:
            self.mejor_racha = self.racha_victorias
    
    def registrar_derrota(self):
        self.partidas_perdidas += 1
        self.racha_victorias = 0
    
    def obtener_estadisticas(self):
        minutos = self.tiempo_juego // 60000
        segundos = (self.tiempo_juego % 60000) // 1000
        return {
            'Tiempo': f"{minutos}:{segundos:02d}",
            'Movimientos': self.movimientos,
            'Errores': f"{self.errores}/{self.max_errores}",
            'Pistas Usadas': self.pistas_usadas,
            'Pistas Inteligentes': self.pistas_inteligentes_usadas,
            'Dificultad': self.nivel_dificultad
        }
    
    def obtener_estadisticas_avanzadas(self):
        tiempo_promedio = self.tiempo_total // max(1, self.partidas_completadas)
        minutos_prom = tiempo_promedio // 60000
        segundos_prom = (tiempo_promedio % 60000) // 1000
        precision = (self.movimientos_correctos / max(1, self.movimientos_totales)) * 100
        
        return {
            'Partidas Completadas': self.partidas_completadas,
            'Tiempo Promedio': f"{minutos_prom}:{segundos_prom:02d}",
            'Precisión': f"{precision:.1f}%",
            'Racha Actual': self.racha_victorias,
            'Mejor Racha': self.mejor_racha,
            'Total Pistas': self.pistas_usadas
        }

class SistemaPuntuaciones:
    def __init__(self):
        self.archivo_puntuaciones = "puntuaciones_sudoku.txt"
        self.puntuaciones = self.cargar_puntuaciones()
    
    def cargar_puntuaciones(self):
        try:
            with open(self.archivo_puntuaciones, 'r') as f:
                lineas = f.readlines()
                puntuaciones = []
                for linea in lineas:
                    if linea.strip():
                        try:
                            datos = json.loads(linea.strip())
                            puntuaciones.append(datos)
                        except:
                            continue
                return puntuaciones
        except:
            return []
    
    def guardar_puntuacion(self, datos_puntuacion):
        self.puntuaciones.append(datos_puntuacion)
        self.puntuaciones.sort(key=lambda x: x['tiempo'])
        self.puntuaciones = self.puntuaciones[:10]
        
        try:
            with open(self.archivo_puntuaciones, 'w') as f:
                for score in self.puntuaciones:
                    f.write(f"{json.dumps(score)}\n")
        except Exception as e:
            print(f"Error guardando puntuación: {e}")
    
    def es_puntuacion_alta(self, tiempo):
        return len(self.puntuaciones) < 10 or tiempo < max([p['tiempo'] for p in self.puntuaciones])
    
    def dibujar_tabla_puntuaciones(self, pantalla, fuente, x, y):
        panel_ancho = 320
        panel_alto = 350
        panel_rect = pygame.Rect(x, y, panel_ancho, panel_alto)
        
        for i in range(panel_alto):
            alpha = 200 - (i * 200 // panel_alto)
            color = (25, 35, 45, alpha)
            pygame.draw.line(pantalla, color, (x, y + i), (x + panel_ancho, y + i))
        
        pygame.draw.rect(pantalla, (255, 255, 255, 30), panel_rect, border_radius=12)
        pygame.draw.rect(pantalla, COLOR_BOTON, panel_rect, 2, border_radius=12)
        
        titulo = fuente.render("MEJORES TIEMPOS", True, BLANCO)
        sombra = fuente.render("MEJORES TIEMPOS", True, (0, 0, 0, 100))
        pantalla.blit(sombra, (x + panel_ancho//2 - titulo.get_width()//2 + 2, y + 22))
        pantalla.blit(titulo, (x + panel_ancho//2 - titulo.get_width()//2, y + 20))
        
        encabezados = ["Pos", "Tiempo", "Dificultad"]
        for i, encabezado in enumerate(encabezados):
            texto = fuente.render(encabezado, True, COLOR_AMARILLO)
            pantalla.blit(texto, (x + 20 + i*100, y + 60))
        
        for i, score in enumerate(self.puntuaciones[:5]):
            if i % 2 == 0:
                pygame.draw.rect(pantalla, (255, 255, 255, 20), 
                               (x + 10, y + 90 + i * 45, panel_ancho - 20, 35), border_radius=6)
            
            texto_pos = fuente.render(f"{i+1}.", True, BLANCO)
            pantalla.blit(texto_pos, (x + 25, y + 100 + i * 45))
            
            minutos = score['tiempo'] // 60000
            segundos = (score['tiempo'] % 60000) // 1000
            texto_tiempo = fuente.render(f"{minutos}:{segundos:02d}", True, BLANCO)
            pantalla.blit(texto_tiempo, (x + 80, y + 100 + i * 45))
            
            color_dificultad = COLOR_VERDE if score['dificultad'] == "Fácil" else \
                             COLOR_AMARILLO if score['dificultad'] == "Medio" else \
                             COLOR_NARANJA if score['dificultad'] == "Difícil" else \
                             COLOR_ROJO if score['dificultad'] == "Experto" else \
                             COLOR_PURPURA if score['dificultad'] == "Maestro" else COLOR_ROSA
            texto_dif = fuente.render(score['dificultad'][:3], True, color_dificultad)
            pantalla.blit(texto_dif, (x + 180, y + 100 + i * 45))

class SistemaUsuarios:
    def __init__(self):
        self.archivo_usuarios = "usuarios_sudoku.json"
        self.usuario_actual = None
        self.usuarios = self.cargar_usuarios()
    
    def cargar_usuarios(self):
        try:
            with open(self.archivo_usuarios, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def guardar_usuarios(self):
        try:
            with open(self.archivo_usuarios, 'w') as f:
                json.dump(self.usuarios, f, indent=2)
        except Exception as e:
            print(f"Error guardando usuarios: {e}")
    
    def registrar_usuario(self, usuario, password):
        if usuario in self.usuarios:
            return False, "El usuario ya existe"
        
        self.usuarios[usuario] = {
            'password': password,
            'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'estadisticas': {
                'partidas_ganadas': 0,
                'partidas_perdidas': 0,
                'mejor_tiempo': None,
                'total_pistas': 0,
                'logros_desbloqueados': [],
                'tema_actual': 'Clásico'
            }
        }
        self.guardar_usuarios()
        return True, "Usuario registrado exitosamente"
    
    def login(self, usuario, password):
        if usuario in self.usuarios and self.usuarios[usuario]['password'] == password:
            self.usuario_actual = usuario
            return True, "Login exitoso"
        return False, "Usuario o contraseña incorrectos"
    
    def logout(self):
        self.usuario_actual = None
    
    def obtener_estadisticas_usuario(self):
        if self.usuario_actual:
            return self.usuarios[self.usuario_actual]['estadisticas']
        return None
    
    def actualizar_estadisticas(self, nuevas_estadisticas):
        if self.usuario_actual:
            for key, value in nuevas_estadisticas.items():
                if key in self.usuarios[self.usuario_actual]['estadisticas']:
                    self.usuarios[self.usuario_actual]['estadisticas'][key] = value
            self.guardar_usuarios()

class Configuracion:
    def __init__(self):
        self.mostrar_conflictos = True
        self.mostrar_pistas = True
        self.mostrar_timer = True
        self.dificultad = "Medio"
        self.tema_actual = "Clásico"
        self.controles = {
            'seleccionar': [pygame.MOUSEBUTTONDOWN],
            'numero': [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                      pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9],
            'borrar': [pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0],
            'pista': [pygame.K_h],
            'notas': [pygame.K_n],
            'deshacer': [pygame.K_z]
        }
    
    def guardar_configuracion(self):
        config = {
            'mostrar_conflictos': self.mostrar_conflictos,
            'mostrar_pistas': self.mostrar_pistas,
            'mostrar_timer': self.mostrar_timer,
            'dificultad': self.dificultad,
            'tema_actual': self.tema_actual
        }
        
        try:
            with open('config_sudoku.json', 'w') as f:
                json.dump(config, f)
        except:
            print("Error guardando configuración")
    
    def cargar_configuracion(self):
        try:
            with open('config_sudoku.json', 'r') as f:
                config = json.load(f)
                self.mostrar_conflictos = config.get('mostrar_conflictos', True)
                self.mostrar_pistas = config.get('mostrar_pistas', True)
                self.mostrar_timer = config.get('mostrar_timer', True)
                self.dificultad = config.get('dificultad', 'Medio')
                self.tema_actual = config.get('tema_actual', 'Clásico')
        except:
            print("Configuración no encontrada, usando valores por defecto")
    
    def aplicar_tema(self, nombre_tema):
        if nombre_tema in TEMAS:
            self.tema_actual = nombre_tema
            return TEMAS[nombre_tema]
        return TEMAS["Clásico"]

class TextoFlotante:
    def __init__(self, texto, x, y, color=BLANCO, duracion=1500):
        self.texto = texto
        self.x = x
        self.y = y
        self.color = color
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = duracion
    
    def actualizar(self):
        return pygame.time.get_ticks() - self.tiempo_inicio < self.duracion
    
    def dibujar(self, pantalla, fuente):
        tiempo = pygame.time.get_ticks() - self.tiempo_inicio
        progreso = tiempo / self.duracion
        
        alpha = int(255 * (1 - progreso))
        y_offset = -50 * progreso
        
        texto_surf = fuente.render(self.texto, True, self.color)
        texto_surf.set_alpha(alpha)
        
        pantalla.blit(texto_surf, (self.x - texto_surf.get_width() // 2, 
                                 self.y + y_offset - texto_surf.get_height() // 2))

class EfectosEspeciales:
    def __init__(self):
        self.animaciones = []
    
    def agregar_explosion_celda(self, x, y):
        crear_particulas(
            MARGEN_X + x * TAMANIO_CELDA + TAMANIO_CELDA // 2,
            MARGEN_Y + y * TAMANIO_CELDA + TAMANIO_CELDA // 2,
            15, "confeti", (100, 200, 255)
        )
    
    def agregar_texto_flotante(self, texto, x, y, color=BLANCO):
        self.animaciones.append(TextoFlotante(texto, x, y, color))
    
    def actualizar(self):
        self.animaciones = [anim for anim in self.animaciones if anim.actualizar()]
    
    def dibujar(self, pantalla, fuente):
        for anim in self.animaciones:
            anim.dibujar(pantalla, fuente)

class GeneradorSudoku:
    def __init__(self):
        self.tablero = [[0 for _ in range(9)] for _ in range(9)]
    
    def es_valido(self, tablero, fila, col, num):
        for i in range(9):
            if tablero[fila][i] == num:
                return False
        
        for i in range(9):
            if tablero[i][col] == num:
                return False
        
        inicio_fila = (fila // 3) * 3
        inicio_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if tablero[inicio_fila + i][inicio_col + j] == num:
                    return False
        
        return True
    
    def resolver(self, tablero):
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    for num in range(1, 10):
                        if self.es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num
                            if self.resolver(tablero):
                                return True
                            tablero[fila][col] = 0
                    return False
        return True
    
    def generar_tablero_completo(self):
        self.tablero = [[0 for _ in range(9)] for _ in range(9)]
        
        for i in range(0, 9, 3):
            numeros = list(range(1, 10))
            random.shuffle(numeros)
            for j in range(3):
                for k in range(3):
                    self.tablero[i + j][i + k] = numeros.pop()
        
        self.resolver(self.tablero)
        return self.tablero
    
    def remover_celdas(self, dificultad):
        tablero_completo = [fila[:] for fila in self.tablero]
        celdas_remover = 0
        
        if dificultad == "Fácil":
            celdas_remover = 30
        elif dificultad == "Medio":
            celdas_remover = 40
        elif dificultad == "Difícil":
            celdas_remover = 50
        elif dificultad == "Experto":
            celdas_remover = 55
        elif dificultad == "Maestro":
            celdas_remover = 60
        else:
            celdas_remover = 65
        
        celdas_removidas = 0
        intentos = 0
        max_intentos = 1000
        
        while celdas_removidas < celdas_remover and intentos < max_intentos:
            fila = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if tablero_completo[fila][col] != 0:
                valor_original = tablero_completo[fila][col]
                tablero_completo[fila][col] = 0
                
                if self.contar_soluciones([fila[:] for fila in tablero_completo]) == 1:
                    celdas_removidas += 1
                else:
                    tablero_completo[fila][col] = valor_original
                
                intentos += 1
        
        return tablero_completo
    
    def contar_soluciones(self, tablero, limite=2):
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    count = 0
                    for num in range(1, 10):
                        if self.es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num
                            count += self.contar_soluciones(tablero, limite - count)
                            tablero[fila][col] = 0
                            if count >= limite:
                                return count
                    return count
        return 1
    
    def generar_juego(self, dificultad):
        self.generar_tablero_completo()
        tablero_incompleto = self.remover_celdas(dificultad)
        return self.tablero, tablero_incompleto

class TableroSudoku:
    def __init__(self):
        self.tablero_completo = None
        self.tablero_juego = None
        self.tablero_usuario = None
        self.tablero_notas = [[[] for _ in range(9)] for _ in range(9)]
        self.celda_seleccionada = None
        self.conflictos = set()
        self.historial = []
        self.modo_notas = False
    
    def inicializar(self, tablero_completo, tablero_juego):
        self.tablero_completo = tablero_completo
        self.tablero_juego = tablero_juego
        self.tablero_usuario = [fila[:] for fila in tablero_juego]
        self.tablero_notas = [[[] for _ in range(9)] for _ in range(9)]
        self.celda_seleccionada = None
        self.conflictos = set()
        self.historial = []
        self.modo_notas = False
    
    def seleccionar_celda(self, fila, col):
        if 0 <= fila < 9 and 0 <= col < 9:
            if self.tablero_juego[fila][col] == 0:
                self.celda_seleccionada = (fila, col)
                return True
        return False
    
    def colocar_numero(self, fila, col, numero):
        if self.tablero_juego[fila][col] != 0:
            return False
            
        if self.modo_notas:
            if numero in self.tablero_notas[fila][col]:
                self.tablero_notas[fila][col].remove(numero)
            else:
                self.tablero_notas[fila][col].append(numero)
                self.tablero_notas[fila][col].sort()
            return True
        else:
            if self.tablero_usuario[fila][col] == 0:
                estado_anterior = (fila, col, self.tablero_usuario[fila][col], self.tablero_notas[fila][col][:])
                self.historial.append(estado_anterior)
                
                self.tablero_usuario[fila][col] = numero
                self.tablero_notas[fila][col] = []
                self.actualizar_conflictos()
                return True
        return False
    
    def borrar_numero(self, fila, col):
        if self.tablero_juego[fila][col] != 0:
            return False
            
        if self.tablero_usuario[fila][col] != 0 or self.tablero_notas[fila][col]:
            estado_anterior = (fila, col, self.tablero_usuario[fila][col], self.tablero_notas[fila][col][:])
            self.historial.append(estado_anterior)
            
            if self.modo_notas:
                self.tablero_notas[fila][col] = []
            else:
                self.tablero_usuario[fila][col] = 0
            
            self.actualizar_conflictos()
            return True
        return False
    
    def deshacer(self):
        if self.historial:
            fila, col, valor, notas = self.historial.pop()
            self.tablero_usuario[fila][col] = valor
            self.tablero_notas[fila][col] = notas
            self.actualizar_conflictos()
            return True
        return False
    
    def obtener_pista(self):
        if self.celda_seleccionada:
            fila, col = self.celda_seleccionada
            if self.tablero_juego[fila][col] == 0 and self.tablero_usuario[fila][col] == 0:
                estado_anterior = (fila, col, self.tablero_usuario[fila][col], self.tablero_notas[fila][col][:])
                self.historial.append(estado_anterior)
                
                numero_correcto = self.tablero_completo[fila][col]
                self.tablero_usuario[fila][col] = numero_correcto
                self.tablero_notas[fila][col] = []
                self.actualizar_conflictos()
                return True
        return False
    
    def actualizar_conflictos(self):
        self.conflictos = set()
        
        for fila in range(9):
            numeros_vistos = set()
            for col in range(9):
                num = self.tablero_usuario[fila][col]
                if num != 0:
                    if num in numeros_vistos:
                        for c in range(9):
                            if self.tablero_usuario[fila][c] == num:
                                self.conflictos.add((fila, c))
                    numeros_vistos.add(num)
        
        for col in range(9):
            numeros_vistos = set()
            for fila in range(9):
                num = self.tablero_usuario[fila][col]
                if num != 0:
                    if num in numeros_vistos:
                        for f in range(9):
                            if self.tablero_usuario[f][col] == num:
                                self.conflictos.add((f, col))
                    numeros_vistos.add(num)
        
        for caja_fila in range(0, 9, 3):
            for caja_col in range(0, 9, 3):
                numeros_vistos = set()
                for i in range(3):
                    for j in range(3):
                        fila = caja_fila + i
                        col = caja_col + j
                        num = self.tablero_usuario[fila][col]
                        if num != 0:
                            if num in numeros_vistos:
                                for x in range(3):
                                    for y in range(3):
                                        f = caja_fila + x
                                        c = caja_col + y
                                        if self.tablero_usuario[f][c] == num:
                                            self.conflictos.add((f, c))
                            numeros_vistos.add(num)
    
    def es_completo(self):
        for fila in range(9):
            for col in range(9):
                if self.tablero_usuario[fila][col] != self.tablero_completo[fila][col]:
                    return False
        return True
    
    def dibujar(self, pantalla, fuente, config):
        tema = TEMAS[config.tema_actual]
        
        tablero_rect = pygame.Rect(MARGEN_X, MARGEN_Y, 9 * TAMANIO_CELDA, 9 * TAMANIO_CELDA)
        pygame.draw.rect(pantalla, tema["tablero"], tablero_rect)
        pygame.draw.rect(pantalla, tema["borde"], tablero_rect, 3)
        
        for i in range(1, 3):
            pygame.draw.line(
                pantalla, tema["borde"],
                (MARGEN_X + i * 3 * TAMANIO_CELDA, MARGEN_Y),
                (MARGEN_X + i * 3 * TAMANIO_CELDA, MARGEN_Y + 9 * TAMANIO_CELDA),
                4
            )
            pygame.draw.line(
                pantalla, tema["borde"],
                (MARGEN_X, MARGEN_Y + i * 3 * TAMANIO_CELDA),
                (MARGEN_X + 9 * TAMANIO_CELDA, MARGEN_Y + i * 3 * TAMANIO_CELDA),
                4
            )
        
        for i in range(1, 9):
            if i % 3 != 0:
                pygame.draw.line(
                    pantalla, GRIS_CLARO,
                    (MARGEN_X + i * TAMANIO_CELDA, MARGEN_Y),
                    (MARGEN_X + i * TAMANIO_CELDA, MARGEN_Y + 9 * TAMANIO_CELDA),
                    2
                )
                pygame.draw.line(
                    pantalla, GRIS_CLARO,
                    (MARGEN_X, MARGEN_Y + i * TAMANIO_CELDA),
                    (MARGEN_X + 9 * TAMANIO_CELDA, MARGEN_Y + i * TAMANIO_CELDA),
                    2
                )
        
        for fila in range(9):
            for col in range(9):
                x = MARGEN_X + col * TAMANIO_CELDA
                y = MARGEN_Y + fila * TAMANIO_CELDA
                
                if self.celda_seleccionada == (fila, col):
                    pygame.draw.rect(pantalla, COLOR_CELDA_SELECCIONADA, 
                                   (x, y, TAMANIO_CELDA, TAMANIO_CELDA))
                
                if config.mostrar_conflictos and (fila, col) in self.conflictos:
                    pygame.draw.rect(pantalla, COLOR_CONFLICTO, 
                                   (x, y, TAMANIO_CELDA, TAMANIO_CELDA))
                
                num = self.tablero_usuario[fila][col]
                if num != 0:
                    if self.tablero_juego[fila][col] != 0:
                        color = tema["numeros_originales"]
                    else:
                        color = tema["numeros_usuario"]
                    
                    texto = fuente.render(str(num), True, color)
                    texto_rect = texto.get_rect(center=(x + TAMANIO_CELDA // 2, y + TAMANIO_CELDA // 2))
                    pantalla.blit(texto, texto_rect)
                
                elif self.tablero_notas[fila][col]:
                    for i, nota in enumerate(self.tablero_notas[fila][col]):
                        nota_x = x + (i % 3) * (TAMANIO_CELDA // 3) + 8
                        nota_y = y + (i // 3) * (TAMANIO_CELDA // 3) + 8
                        texto_nota = fuente_pista.render(str(nota), True, COLOR_NOTA)
                        pantalla.blit(texto_nota, (nota_x, nota_y))

def dibujar_boton_reiniciar():
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_reiniciar_rect.collidepoint(mouse_pos) else COLOR_BOTON
    color_icono = BLANCO if boton_reiniciar_rect.collidepoint(mouse_pos) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_reiniciar_rect, border_radius=8)
    pygame.draw.rect(pantalla, color_icono, boton_reiniciar_rect, 2, border_radius=8)
    
    centro_x = boton_reiniciar_rect.centerx
    centro_y = boton_reiniciar_rect.centery
    radio = 10
    
    pygame.draw.circle(pantalla, color_icono, (centro_x, centro_y), radio, 2)
    
    puntos_flecha = [
        (centro_x + 5, centro_y - 3),
        (centro_x - 2, centro_y - 6),
        (centro_x - 2, centro_y)
    ]
    pygame.draw.polygon(pantalla, color_icono, puntos_flecha)

def dibujar_boton_pausa():
    mouse_pos = pygame.mouse.get_pos()
    color_boton = COLOR_BOTON_HOVER if boton_pausa_rect.collidepoint(mouse_pos) else COLOR_BOTON
    color_icono = BLANCO if boton_pausa_rect.collidepoint(mouse_pos) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_pausa_rect, border_radius=8)
    pygame.draw.rect(pantalla, color_icono, boton_pausa_rect, 2, border_radius=8)
    
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 9, boton_pausa_rect.y + 8, 4, 16))
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 19, boton_pausa_rect.y + 8, 4, 16))

def dibujar_panel_login(juego):
    panel_ancho, panel_alto = 400, 500
    panel_x = (ANCHO - panel_ancho) // 2
    panel_y = (ALTO - panel_alto) // 2
    
    s = pygame.Surface((panel_ancho, panel_alto), pygame.SRCALPHA)
    s.fill((255, 255, 255, 30))
    pygame.draw.rect(s, (255, 255, 255, 50), (0, 0, panel_ancho, panel_alto), border_radius=20)
    pygame.draw.rect(s, COLOR_BOTON, (0, 0, panel_ancho, panel_alto), 3, border_radius=20)
    pantalla.blit(s, (panel_x, panel_y))
    
    titulo = juego.fuente_grande.render("INICIAR SESIÓN", True, BLANCO)
    pantalla.blit(titulo, (panel_x + panel_ancho//2 - titulo.get_width()//2, panel_y + 40))
    
    campos = [
        {"label": "Usuario:", "text": "", "rect": pygame.Rect(panel_x + 50, panel_y + 150, 300, 45), "active": False},
        {"label": "Contraseña:", "text": "", "rect": pygame.Rect(panel_x + 50, panel_y + 220, 300, 45), "active": False, "password": True}
    ]
    
    for campo in campos:
        label = juego.fuente_pista.render(campo["label"], True, BLANCO)
        pantalla.blit(label, (campo["rect"].x, campo["rect"].y - 25))
        
        color_campo = COLOR_BOTON_HOVER if campo["active"] else COLOR_BOTON
        pygame.draw.rect(pantalla, color_campo, campo["rect"], border_radius=8)
        pygame.draw.rect(pantalla, BLANCO, campo["rect"], 2, border_radius=8)
        
        texto_mostrar = "*" * len(campo["text"]) if campo.get("password") else campo["text"]
        texto = juego.fuente_pista.render(texto_mostrar, True, BLANCO)
        pantalla.blit(texto, (campo["rect"].x + 10, campo["rect"].y + 10))
    
    boton_login = pygame.Rect(panel_x + 50, panel_y + 300, 300, 50)
    boton_registro = pygame.Rect(panel_x + 50, panel_y + 370, 300, 50)
    boton_skip = pygame.Rect(panel_x + 50, panel_y + 440, 300, 40)
    
    botones = [
        (boton_login, "INICIAR SESIÓN", COLOR_VERDE),
        (boton_registro, "REGISTRARSE", COLOR_BOTON),
        (boton_skip, "JUGAR SIN CUENTA", GRIS_MEDIO)
    ]
    
    for boton, texto, color in botones:
        mouse_pos = pygame.mouse.get_pos()
        color_boton = COLOR_BOTON_HOVER if boton.collidepoint(mouse_pos) else color
        
        pygame.draw.rect(pantalla, color_boton, boton, border_radius=10)
        pygame.draw.rect(pantalla, BLANCO, boton, 2, border_radius=10)
        
        texto_boton = juego.fuente.render(texto, True, BLANCO)
        texto_rect = texto_boton.get_rect(center=boton.center)
        pantalla.blit(texto_boton, texto_rect)
    
    return campos, boton_login, boton_registro, boton_skip

def dibujar_menu_principal(juego):
    tema = TEMAS[juego.config.tema_actual]
    pantalla.fill(tema["fondo"])
    
    if random.random() < 0.03:
        crear_particulas(random.randint(0, ANCHO), random.randint(0, ALTO), 3, "brillo", (100, 100, 255))
    
    tiempo = pygame.time.get_ticks() / 1000
    titulo = juego.fuente_grande.render("SUDOKU PREMIUM", True, BLANCO)
    titulo_rect = titulo.get_rect(center=(ANCHO//2, 120))
    
    surf_temp = pygame.Surface(titulo.get_size(), pygame.SRCALPHA)
    surf_temp.blit(titulo, (0, 0))
    alpha = 200 + int(math.sin(tiempo * 3) * 55)
    surf_temp.set_alpha(alpha)
    pantalla.blit(surf_temp, titulo_rect)
    
    sombra = juego.fuente_grande.render("SUDOKU PREMIUM", True, (0, 0, 0, 100))
    pantalla.blit(sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
    
    if juego.usuarios.usuario_actual:
        usuario_texto = juego.fuente_pista.render(f"Bienvenido, {juego.usuarios.usuario_actual}", True, COLOR_AMARILLO)
        pantalla.blit(usuario_texto, (ANCHO - usuario_texto.get_width() - 20, 20))
    
    botones_menu = [
        ("🎮 INICIAR PARTIDA", 250, COLOR_VERDE),
        ("📅 DESAFÍOS DIARIOS", 320, COLOR_BOTON),
        ("👤 MI CUENTA", 390, COLOR_PURPURA),
        ("⚙️ CONFIGURACIÓN", 460, COLOR_NARANJA)
    ]
    
    botones = []
    for texto, y, color in botones_menu:
        boton = pygame.Rect(ANCHO//2 - 180, y, 360, 65)
        botones.append((boton, texto, color))
        
        mouse_pos = pygame.mouse.get_pos()
        color_boton = COLOR_BOTON_HOVER if boton.collidepoint(mouse_pos) else color
        
        pygame.draw.rect(pantalla, color_boton, boton, border_radius=15)
        pygame.draw.rect(pantalla, BLANCO, boton, 3, border_radius=15)
        
        sombra_boton = pygame.Rect(boton.x + 3, boton.y + 3, boton.width, boton.height)
        pygame.draw.rect(pantalla, (0, 0, 0, 50), sombra_boton, border_radius=15)
        
        texto_boton = juego.fuente.render(texto, True, BLANCO)
        texto_rect = texto_boton.get_rect(center=boton.center)
        pantalla.blit(texto_boton, texto_rect)
    
    titulo_dificultad = juego.fuente_mediana.render("SELECCIONA DIFICULTAD:", True, COLOR_AMARILLO)
    pantalla.blit(titulo_dificultad, (ANCHO//2 - titulo_dificultad.get_width()//2, 550))
    
    dificultades = ["Fácil", "Medio", "Difícil", "Experto", "Maestro", "Extremo"]
    colores_dificultad = [COLOR_VERDE, COLOR_AMARILLO, COLOR_NARANJA, COLOR_ROJO, COLOR_PURPURA, COLOR_ROSA]
    botones_dificultad = []
    
    for i, (dificultad, color) in enumerate(zip(dificultades, colores_dificultad)):
        boton = pygame.Rect(ANCHO//2 - 285 + i * 95, 590, 90, 40)
        botones_dificultad.append((boton, dificultad, color))
        
        mouse_pos = pygame.mouse.get_pos()
        color_boton = COLOR_BOTON_HOVER if boton.collidepoint(mouse_pos) else color
        
        pygame.draw.rect(pantalla, color_boton, boton, border_radius=10)
        pygame.draw.rect(pantalla, BLANCO, boton, 2, border_radius=10)
        
        if juego.config.dificultad == dificultad:
            pygame.draw.rect(pantalla, BLANCO, boton, 3, border_radius=10)
        
        texto = juego.fuente_pista.render(dificultad[:3], True, BLANCO)
        texto_rect = texto.get_rect(center=boton.center)
        pantalla.blit(texto, texto_rect)
    
    juego.puntuaciones.dibujar_tabla_puntuaciones(pantalla, juego.fuente_pista, 50, 200)
    
    if juego.usuarios.usuario_actual:
        stats = juego.usuarios.obtener_estadisticas_usuario()
        if stats:
            panel_stats = pygame.Rect(ANCHO - 350, 200, 300, 150)
            pygame.draw.rect(pantalla, (255, 255, 255, 30), panel_stats, border_radius=12)
            pygame.draw.rect(pantalla, COLOR_BOTON, panel_stats, 2, border_radius=12)
            
            titulo_stats = juego.fuente_pista.render("TUS ESTADÍSTICAS", True, COLOR_AMARILLO)
            pantalla.blit(titulo_stats, (panel_stats.centerx - titulo_stats.get_width()//2, panel_stats.y + 15))
            
            textos_stats = [
                f"Victorias: {stats['partidas_ganadas']}",
                f"Derrotas: {stats['partidas_perdidas']}",
                f"Pistas usadas: {stats['total_pistas']}"
            ]
            
            for i, texto in enumerate(textos_stats):
                texto_stat = juego.fuente_pista.render(texto, True, BLANCO)
                pantalla.blit(texto_stat, (panel_stats.x + 20, panel_stats.y + 50 + i * 25))
    
    return botones, botones_dificultad

def mostrar_pausa_mejorada(juego):
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    juego.pantalla.blit(s, (0, 0))
    
    panel_rect = pygame.Rect(ANCHO//2 - 200, ALTO//2 - 150, 400, 300)
    
    for i in range(panel_rect.height):
        alpha = 200 - (i * 100 // panel_rect.height)
        color = (30, 40, 50, alpha)
        pygame.draw.line(juego.pantalla, color, 
                        (panel_rect.x, panel_rect.y + i), 
                        (panel_rect.x + panel_rect.width, panel_rect.y + i))
    
    pygame.draw.rect(juego.pantalla, (255, 255, 255, 30), panel_rect, border_radius=20)
    pygame.draw.rect(juego.pantalla, COLOR_BOTON, panel_rect, 3, border_radius=20)
    
    texto_pausa = juego.fuente_grande.render("PAUSA", True, BLANCO)
    sombra_pausa = juego.fuente_grande.render("PAUSA", True, (0, 0, 0, 100))
    juego.pantalla.blit(sombra_pausa, (ANCHO//2 - texto_pausa.get_width()//2 + 2, ALTO//2 - 122))
    juego.pantalla.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, ALTO//2 - 120))
    
    stats = juego.estadisticas.obtener_estadisticas()
    textos_stats = [
        f"⏱️  Tiempo: {stats['Tiempo']}",
        f"🎯 Movimientos: {stats['Movimientos']}",
        f"❌ Errores: {stats['Errores']}",
        f"💡 Pistas: {stats['Pistas Usadas']}"
    ]
    
    for i, texto in enumerate(textos_stats):
        texto_surf = juego.fuente.render(texto, True, BLANCO)
        juego.pantalla.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 60 + i * 40))
    
    texto_continuar = juego.fuente_pista.render("Presiona ESC para continuar", True, COLOR_AMARILLO)
    juego.pantalla.blit(texto_continuar, (ANCHO//2 - texto_continuar.get_width()//2, ALTO//2 + 100))

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Sudoku Premium - Juego Profesional")
        self.reloj = pygame.time.Clock()
        
        # Sistemas
        self.audio = SistemaAudio()
        self.estadisticas = Estadisticas()
        self.puntuaciones = SistemaPuntuaciones()
        self.usuarios = SistemaUsuarios()
        self.config = Configuracion()
        self.efectos = EfectosEspeciales()
        self.generador = GeneradorSudoku()
        self.tablero = TableroSudoku()
        self.autoguardado = SistemaAutoguardado()
        self.pistas_inteligentes = SistemaPistasInteligentes()
        self.logros = SistemaLogros()
        
        # Fuentes
        self.fuente = self.obtener_fuente(28)
        self.fuente_grande = self.obtener_fuente(60)
        self.fuente_mediana = self.obtener_fuente(24)
        self.fuente_pista = self.obtener_fuente(20)
        
        # Estados
        self.campos_login = []
        self.campo_activo = None
        
        # Cargar configuración
        self.config.cargar_configuracion()
        
        self.reiniciar_juego()
    
    def obtener_fuente(self, tamaño):
        fuentes_linux = [
            'dejavusans',
            'liberationsans', 
            'freesans',
            'arial',
            None
        ]
        
        for fuente_nombre in fuentes_linux:
            try:
                fuente = pygame.font.SysFont(fuente_nombre, tamaño)
                texto_prueba = fuente.render('Test', True, BLANCO)
                if texto_prueba.get_width() > 0:
                    return fuente
            except:
                continue
        
        return pygame.font.Font(None, tamaño)
    
    def reiniciar_juego(self):
        tablero_completo, tablero_juego = self.generador.generar_juego(self.config.dificultad)
        self.tablero.inicializar(tablero_completo, tablero_juego)
        
        self.estadisticas = Estadisticas()
        self.estadisticas.nivel_dificultad = self.config.dificultad
        
        if self.config.dificultad == "Fácil":
            self.estadisticas.max_errores = 5
        elif self.config.dificultad == "Medio":
            self.estadisticas.max_errores = 4
        elif self.config.dificultad == "Difícil":
            self.estadisticas.max_errores = 3
        else:
            self.estadisticas.max_errores = 3
        
        self.juego_activo = True
        self.pausa = False
        if not hasattr(self, 'estado_juego'):
            self.estado_juego = "login"
        self.ultima_actualizacion_tiempo = pygame.time.get_ticks()
    
    def cargar_partida_autoguardada(self):
        """Carga una partida autoguardada si existe"""
        datos = self.autoguardado.cargar_autoguardado()
        if datos:
            try:
                self.tablero.tablero_completo = datos['tablero_completo']
                self.tablero.tablero_juego = datos['tablero_juego']
                self.tablero.tablero_usuario = datos['tablero_usuario']
                self.tablero.tablero_notas = datos['tablero_notas']
                self.tablero.celda_seleccionada = datos['celda_seleccionada']
                
                # Restaurar estadísticas
                stats = datos['estadisticas']
                self.estadisticas.tiempo_inicio = pygame.time.get_ticks() - stats['tiempo_juego']
                self.estadisticas.tiempo_juego = stats['tiempo_juego']
                self.estadisticas.movimientos = stats['movimientos']
                self.estadisticas.errores = stats['errores']
                self.estadisticas.pistas_usadas = stats['pistas_usadas']
                self.estadisticas.nivel_dificultad = stats['nivel_dificultad']
                
                # Restaurar configuración
                config_data = datos['config']
                self.config.dificultad = config_data['dificultad']
                self.config.mostrar_conflictos = config_data['mostrar_conflictos']
                self.config.mostrar_pistas = config_data['mostrar_pistas']
                
                self.estado_juego = "jugando"
                self.juego_activo = True
                self.pausa = False
                
                print("Partida autoguardada cargada correctamente")
                return True
            except Exception as e:
                print(f"Error cargando partida autoguardada: {e}")
        
        return False
    
    def manejar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.config.guardar_configuracion()
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado_juego == "login":
                    campos, boton_login, boton_registro, boton_skip = dibujar_panel_login(self)
                    
                    for campo in campos:
                        if campo["rect"].collidepoint(mouse_pos):
                            self.campo_activo = campo
                            for c in campos:
                                c["active"] = False
                            campo["active"] = True
                    
                    if boton_login.collidepoint(mouse_pos):
                        usuario = campos[0]["text"]
                        password = campos[1]["text"]
                        if usuario and password:
                            success, message = self.usuarios.login(usuario, password)
                            if success:
                                self.estado_juego = "menu"
                                print(f"Login exitoso: {usuario}")
                            else:
                                print(f"Error login: {message}")
                    
                    elif boton_registro.collidepoint(mouse_pos):
                        usuario = campos[0]["text"]
                        password = campos[1]["text"]
                        if usuario and password:
                            success, message = self.usuarios.registrar_usuario(usuario, password)
                            if success:
                                self.estado_juego = "menu"
                                print(f"Registro exitoso: {usuario}")
                            else:
                                print(f"Error registro: {message}")
                    
                    elif boton_skip.collidepoint(mouse_pos):
                        self.estado_juego = "menu"
                        print("Jugando sin cuenta")
                
                elif self.estado_juego == "menu":
                    botones, botones_dificultad = dibujar_menu_principal(self)
                    
                    for boton, texto, _ in botones:
                        if boton.collidepoint(mouse_pos):
                            if "INICIAR PARTIDA" in texto:
                                # Verificar si hay partida autoguardada
                                if self.autoguardado.existe_autoguardado():
                                    self.cargar_partida_autoguardada()
                                else:
                                    self.estado_juego = "jugando"
                                self.audio.reproducir('inicio')
                                print(f"Iniciando juego en dificultad: {self.config.dificultad}")
                            elif "DESAFÍOS DIARIOS" in texto:
                                print("Desafíos diarios - Funcionalidad en desarrollo")
                            elif "MI CUENTA" in texto:
                                if self.usuarios.usuario_actual:
                                    print(f"Cuenta de: {self.usuarios.usuario_actual}")
                                else:
                                    self.estado_juego = "login"
                            elif "CONFIGURACIÓN" in texto:
                                print("Configuración - Funcionalidad en desarrollo")
                    
                    for boton, dificultad, _ in botones_dificultad:
                        if boton.collidepoint(mouse_pos):
                            self.config.dificultad = dificultad
                            print(f"Dificultad cambiada a: {dificultad}")
                
                elif self.estado_juego == "jugando":
                    if boton_pausa_rect.collidepoint(mouse_pos):
                        self.pausa = not self.pausa
                        print(f"Pausa: {self.pausa}")
                        continue
                    
                    elif boton_reiniciar_rect.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('reiniciar')
                        print("Juego reiniciado")
                    
                    elif self.pausa:
                        self.pausa = False
                        print("Pausa desactivada")
                    
                    else:
                        x, y = mouse_pos
                        if (MARGEN_X <= x < MARGEN_X + 9 * TAMANIO_CELDA and 
                            MARGEN_Y <= y < MARGEN_Y + 9 * TAMANIO_CELDA):
                            col = (x - MARGEN_X) // TAMANIO_CELDA
                            fila = (y - MARGEN_Y) // TAMANIO_CELDA
                            if self.tablero.seleccionar_celda(fila, col):
                                self.audio.reproducir('seleccionar')
                                print(f"Celda seleccionada: ({fila}, {col})")
                        
                        botones_control = self.dibujar_controles()
                        for boton, accion in botones_control:
                            if boton.collidepoint(mouse_pos):
                                if accion == "pista":
                                    # Primero intentar pista inteligente
                                    pista_inteligente = self.pistas_inteligentes.obtener_pista_inteligente(self.tablero)
                                    if pista_inteligente:
                                        self.estadisticas.registrar_pista(inteligente=True)
                                        self.estadisticas.registrar_movimiento()
                                        self.audio.reproducir('pista_inteligente')
                                        
                                        # Aplicar la pista inteligente
                                        fila = pista_inteligente['fila']
                                        col = pista_inteligente['columna']
                                        numero = pista_inteligente['numero']
                                        
                                        if self.tablero.colocar_numero(fila, col, numero):
                                            self.efectos.agregar_explosion_celda(col, fila)
                                            self.efectos.agregar_texto_flotante(
                                                pista_inteligente['explicacion'],
                                                MARGEN_X + col * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                                MARGEN_Y + fila * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                                COLOR_AMARILLO
                                            )
                                    else:
                                        # Pista normal
                                        if self.tablero.obtener_pista():
                                            self.estadisticas.registrar_pista()
                                            self.estadisticas.registrar_movimiento()
                                            self.audio.reproducir('pista')
                                            if self.tablero.celda_seleccionada:
                                                fila, col = self.tablero.celda_seleccionada
                                                self.efectos.agregar_explosion_celda(col, fila)
                                elif accion == "deshacer":
                                    if self.tablero.deshacer():
                                        self.audio.reproducir('deshacer')
                                        self.estadisticas.registrar_movimiento()
                                elif accion == "borrar":
                                    if self.tablero.celda_seleccionada:
                                        fila, col = self.tablero.celda_seleccionada
                                        if self.tablero.borrar_numero(fila, col):
                                            self.estadisticas.registrar_movimiento()
                                            self.audio.reproducir('borrar')
                                elif accion == "notas":
                                    self.tablero.modo_notas = not self.tablero.modo_notas
                                    self.audio.reproducir('notas')
                                elif accion == "pista_inteligente":
                                    # Botón específico para pistas inteligentes
                                    pista_inteligente = self.pistas_inteligentes.obtener_pista_inteligente(self.tablero)
                                    if pista_inteligente:
                                        self.estadisticas.registrar_pista(inteligente=True)
                                        self.estadisticas.registrar_movimiento()
                                        self.audio.reproducir('pista_inteligente')
                                        
                                        fila = pista_inteligente['fila']
                                        col = pista_inteligente['columna']
                                        numero = pista_inteligente['numero']
                                        
                                        if self.tablero.colocar_numero(fila, col, numero):
                                            self.efectos.agregar_explosion_celda(col, fila)
                                            self.efectos.agregar_texto_flotante(
                                                pista_inteligente['explicacion'],
                                                MARGEN_X + col * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                                MARGEN_Y + fila * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                                COLOR_AMARILLO
                                            )
                
                elif self.estado_juego == "completado":
                    boton_reiniciar, boton_menu = self.dibujar_pantalla_completado()
                    
                    if boton_reiniciar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Reiniciando desde completado")
                    
                    elif boton_menu.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
                        print("Volviendo al menú principal")
                
                elif self.estado_juego == "game_over":
                    boton_reiniciar, boton_menu = self.dibujar_pantalla_game_over()
                    
                    if boton_reiniciar.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Reiniciando desde game over")
                    
                    elif boton_menu.collidepoint(mouse_pos):
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
                        print("Volviendo al menú principal")
            
            elif evento.type == pygame.KEYDOWN:
                if self.estado_juego == "login" and self.campo_activo:
                    if evento.key == pygame.K_RETURN:
                        pass
                    elif evento.key == pygame.K_BACKSPACE:
                        self.campo_activo["text"] = self.campo_activo["text"][:-1]
                    elif evento.key == pygame.K_TAB:
                        campos, _, _, _ = dibujar_panel_login(self)
                        current_index = campos.index(self.campo_activo)
                        next_index = (current_index + 1) % len(campos)
                        self.campo_activo = campos[next_index]
                    else:
                        if len(self.campo_activo["text"]) < 20:
                            self.campo_activo["text"] += evento.unicode
                
                elif self.estado_juego == "jugando":
                    if evento.key == pygame.K_ESCAPE:
                        self.pausa = not self.pausa
                        print(f"Pausa con ESC: {self.pausa}")
                    
                    elif not self.pausa and self.tablero.celda_seleccionada:
                        fila, col = self.tablero.celda_seleccionada
                        
                        if evento.key in self.config.controles['numero']:
                            numero = int(pygame.key.name(evento.key))
                            if self.tablero.colocar_numero(fila, col, numero):
                                self.estadisticas.registrar_movimiento(correcto=True)
                                self.audio.reproducir('colocar')
                                
                                if not self.tablero.modo_notas and numero != self.tablero.tablero_completo[fila][col]:
                                    if self.estadisticas.registrar_error():
                                        self.estado_juego = "game_over"
                                        self.estadisticas.registrar_derrota()
                                        self.audio.reproducir('game_over')
                                        crear_particulas(ANCHO//2, ALTO//2, 50, "confeti", COLOR_ROJO)
                                    else:
                                        self.efectos.agregar_texto_flotante("¡Error!", 
                                            MARGEN_X + col * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                            MARGEN_Y + fila * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                            COLOR_ROJO)
                                elif not self.tablero.modo_notas:
                                    self.efectos.agregar_explosion_celda(col, fila)
                                    self.efectos.agregar_texto_flotante("¡Correcto!", 
                                        MARGEN_X + col * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                        MARGEN_Y + fila * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                        COLOR_VERDE)
                                
                                if not self.tablero.modo_notas and self.tablero.es_completo():
                                    self.estado_juego = "completado"
                                    self.estadisticas.registrar_victoria()
                                    self.audio.reproducir('completado')
                                    crear_particulas(ANCHO//2, ALTO//2, 100, "estrellas")
                                    
                                    # Verificar logros
                                    self.logros.verificar_logro("progreso", 1, self)
                                    self.logros.verificar_logro("tiempo", self.estadisticas.tiempo_juego, self)
                                    self.logros.verificar_logro("precision", self.estadisticas.errores, self)
                                    self.logros.verificar_logro("cantidad", self.estadisticas.partidas_completadas, self)
                                    self.logros.verificar_logro("pistas", self.estadisticas.pistas_inteligentes_usadas, self)
                                    
                                    if self.puntuaciones.es_puntuacion_alta(self.estadisticas.tiempo_juego):
                                        datos_puntuacion = {
                                            'tiempo': self.estadisticas.tiempo_juego,
                                            'dificultad': self.config.dificultad,
                                            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                            'movimientos': self.estadisticas.movimientos,
                                            'errores': self.estadisticas.errores
                                        }
                                        self.puntuaciones.guardar_puntuacion(datos_puntuacion)
                        
                        elif evento.key in self.config.controles['borrar']:
                            if self.tablero.borrar_numero(fila, col):
                                self.estadisticas.registrar_movimiento()
                                self.audio.reproducir('borrar')
                        
                        elif evento.key in self.config.controles['pista']:
                            pista_inteligente = self.pistas_inteligentes.obtener_pista_inteligente(self.tablero)
                            if pista_inteligente:
                                self.estadisticas.registrar_pista(inteligente=True)
                                self.estadisticas.registrar_movimiento()
                                self.audio.reproducir('pista_inteligente')
                                
                                fila_pista = pista_inteligente['fila']
                                col_pista = pista_inteligente['columna']
                                numero_pista = pista_inteligente['numero']
                                
                                if self.tablero.colocar_numero(fila_pista, col_pista, numero_pista):
                                    self.efectos.agregar_explosion_celda(col_pista, fila_pista)
                                    self.efectos.agregar_texto_flotante(
                                        pista_inteligente['explicacion'],
                                        MARGEN_X + col_pista * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                        MARGEN_Y + fila_pista * TAMANIO_CELDA + TAMANIO_CELDA // 2,
                                        COLOR_AMARILLO
                                    )
                            else:
                                if self.tablero.obtener_pista():
                                    self.estadisticas.registrar_pista()
                                    self.estadisticas.registrar_movimiento()
                                    self.audio.reproducir('pista')
                                    if self.tablero.celda_seleccionada:
                                        fila, col = self.tablero.celda_seleccionada
                                        self.efectos.agregar_explosion_celda(col, fila)
                        
                        elif evento.key in self.config.controles['notas']:
                            self.tablero.modo_notas = not self.tablero.modo_notas
                            self.audio.reproducir('notas')
                        
                        elif evento.key in self.config.controles['deshacer']:
                            if self.tablero.deshacer():
                                self.audio.reproducir('deshacer')
                                self.estadisticas.registrar_movimiento()
                
                elif self.estado_juego in ["completado", "game_over"]:
                    if evento.key == pygame.K_RETURN:
                        self.reiniciar_juego()
                        self.estado_juego = "jugando"
                        self.audio.reproducir('inicio')
                        print("Reiniciando con ENTER")
                    elif evento.key == pygame.K_ESCAPE:
                        self.reiniciar_juego()
                        self.estado_juego = "menu"
                        self.audio.reproducir('menu')
                        print("Volviendo al menú con ESC")
        
        return True

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        dt = tiempo_actual - self.ultima_actualizacion_tiempo
        self.ultima_actualizacion_tiempo = tiempo_actual
        
        if self.estado_juego == "jugando" and not self.pausa:
            self.estadisticas.actualizar_tiempo()
            self.efectos.actualizar()
            
            # Autoguardar cada 2 minutos
            self.autoguardado.autoguardar_partida(self)
    
    def dibujar(self):
        tema = TEMAS[self.config.tema_actual]
        self.pantalla.fill(tema["fondo"])
        
        if self.estado_juego == "login":
            dibujar_panel_login(self)
            
        elif self.estado_juego == "menu":
            dibujar_menu_principal(self)
            
        elif self.estado_juego == "jugando":
            self.tablero.dibujar(self.pantalla, self.fuente, self.config)
            self.dibujar_informacion()
            dibujar_boton_reiniciar()
            dibujar_boton_pausa()
            self.dibujar_controles()
            self.dibujar_selector_numeros()
            self.efectos.dibujar(self.pantalla, self.fuente_grande)
            
            if self.pausa:
                mostrar_pausa_mejorada(self)
                
        elif self.estado_juego == "completado":
            self.dibujar_pantalla_completado()
        
        elif self.estado_juego == "game_over":
            self.dibujar_pantalla_game_over()
        
        for particula in particulas:
            particula.draw(self.pantalla)
        
        pygame.display.flip()
    
    def dibujar_informacion(self):
        panel_x = MARGEN_X + 9 * TAMANIO_CELDA + 20
        panel_y = MARGEN_Y
        
        panel_principal = pygame.Rect(panel_x, panel_y, 280, 220)
        
        for i in range(panel_principal.height):
            alpha = 200 - (i * 100 // panel_principal.height)
            color = (25, 35, 45, alpha)
            pygame.draw.line(self.pantalla, color, 
                           (panel_principal.x, panel_principal.y + i), 
                           (panel_principal.x + panel_principal.width, panel_principal.y + i))
        
        pygame.draw.rect(self.pantalla, (255, 255, 255, 30), panel_principal, border_radius=12)
        pygame.draw.rect(self.pantalla, COLOR_BOTON, panel_principal, 2, border_radius=12)
        
        titulo = self.fuente_pista.render("INFORMACIÓN DE JUEGO", True, COLOR_AMARILLO)
        self.pantalla.blit(titulo, (panel_x + 20, panel_y + 15))
        
        stats = self.estadisticas.obtener_estadisticas()
        textos = [
            f"⏱️  {stats['Tiempo']}",
            f"🎯 {stats['Movimientos']}",
            f"❌ {stats['Errores']}",
            f"💡 {stats['Pistas Usadas']}",
            f"🎯 {stats['Dificultad']}"
        ]
        
        colores = [BLANCO, BLANCO, 
                  COLOR_ROJO if int(stats['Errores'].split('/')[0]) > 0 else BLANCO,
                  COLOR_AMARILLO if int(stats['Pistas Usadas']) > 0 else BLANCO,
                  COLOR_VERDE if stats['Dificultad'] == "Fácil" else
                  COLOR_AMARILLO if stats['Dificultad'] == "Medio" else
                  COLOR_NARANJA if stats['Dificultad'] == "Difícil" else
                  COLOR_ROJO if stats['Dificultad'] == "Experto" else
                  COLOR_PURPURA if stats['Dificultad'] == "Maestro" else COLOR_ROSA]
        
        for i, (texto, color) in enumerate(zip(textos, colores)):
            texto_surf = self.fuente_pista.render(texto, True, color)
            self.pantalla.blit(texto_surf, (panel_x + 30, panel_y + 50 + i * 32))
    
    def dibujar_controles(self):
        panel_x = MARGEN_X
        panel_y = MARGEN_Y + 9 * TAMANIO_CELDA + 20
        ancho_boton = 140
        alto_boton = 45
        espacio = 15
        
        botones = [
            ("💡 PISTA (H)", "pista", COLOR_AMARILLO),
            ("🧠 PISTA INTEL.", "pista_inteligente", COLOR_PURPURA),
            ("↶ DESHACER (Z)", "deshacer", (150, 100, 50)),
            ("🗑️ BORRAR", "borrar", (200, 50, 50)),
            ("📝 NOTAS (N)", "notas", (100, 50, 150) if not self.tablero.modo_notas else (150, 100, 200))
        ]
        
        botones_rect = []
        
        for i, (texto, accion, color) in enumerate(botones):
            boton = pygame.Rect(panel_x + i * (ancho_boton + espacio), panel_y, ancho_boton, alto_boton)
            botones_rect.append((boton, accion))
            
            mouse_pos = pygame.mouse.get_pos()
            color_boton = COLOR_BOTON_HOVER if boton.collidepoint(mouse_pos) else color
            
            pygame.draw.rect(self.pantalla, color_boton, boton, border_radius=10)
            pygame.draw.rect(self.pantalla, BLANCO, boton, 2, border_radius=10)
            
            sombra_boton = pygame.Rect(boton.x + 2, boton.y + 2, boton.width, boton.height)
            pygame.draw.rect(self.pantalla, (0, 0, 0, 50), sombra_boton, border_radius=10)
            
            texto_boton = self.fuente_pista.render(texto, True, BLANCO)
            texto_rect = texto_boton.get_rect(center=boton.center)
            self.pantalla.blit(texto_boton, texto_rect)
        
        return botones_rect
    
    def dibujar_selector_numeros(self):
        panel_x = MARGEN_X
        panel_y = MARGEN_Y + 9 * TAMANIO_CELDA + 75
        ancho_numero = 55
        alto_numero = 55
        espacio = 8
        
        selector_rect = pygame.Rect(panel_x - 10, panel_y - 10, 
                                  9 * (ancho_numero + espacio) - espacio + 20, 
                                  alto_numero + 20)
        pygame.draw.rect(self.pantalla, (255, 255, 255, 30), selector_rect, border_radius=15)
        pygame.draw.rect(self.pantalla, COLOR_BOTON, selector_rect, 2, border_radius=15)
        
        for i in range(1, 10):
            boton = pygame.Rect(panel_x + (i-1) * (ancho_numero + espacio), panel_y, ancho_numero, alto_numero)
            
            mouse_pos = pygame.mouse.get_pos()
            color_boton = COLOR_BOTON_HOVER if boton.collidepoint(mouse_pos) else COLOR_BOTON
            
            pygame.draw.rect(self.pantalla, color_boton, boton, border_radius=12)
            pygame.draw.rect(self.pantalla, BLANCO, boton, 2, border_radius=12)
            
            sombra_boton = pygame.Rect(boton.x + 2, boton.y + 2, boton.width, boton.height)
            pygame.draw.rect(self.pantalla, (0, 0, 0, 50), sombra_boton, border_radius=12)
            
            texto = self.fuente.render(str(i), True, BLANCO)
            texto_rect = texto.get_rect(center=boton.center)
            self.pantalla.blit(texto, texto_rect)

    def dibujar_pantalla_completado(self):
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.pantalla.blit(s, (0, 0))
        
        panel_rect = pygame.Rect(ANCHO//2 - 350, ALTO//2 - 200, 700, 400)
        
        for i in range(panel_rect.height):
            alpha = 200 - (i * 100 // panel_rect.height)
            color = (0, 100, 0, alpha)
            pygame.draw.line(self.pantalla, color, 
                           (panel_rect.x, panel_rect.y + i), 
                           (panel_rect.x + panel_rect.width, panel_rect.y + i))
        
        pygame.draw.rect(self.pantalla, (255, 255, 255, 30), panel_rect, border_radius=25)
        pygame.draw.rect(self.pantalla, COLOR_VERDE, panel_rect, 4, border_radius=25)
        
        texto_completado = self.fuente_grande.render("¡VICTORIA!", True, COLOR_VERDE)
        sombra_completado = self.fuente_grande.render("¡VICTORIA!", True, (0, 0, 0, 100))
        self.pantalla.blit(sombra_completado, (ANCHO//2 - texto_completado.get_width()//2 + 3, ALTO//2 - 147))
        self.pantalla.blit(texto_completado, (ANCHO//2 - texto_completado.get_width()//2, ALTO//2 - 150))
        
        if self.puntuaciones.es_puntuacion_alta(self.estadisticas.tiempo_juego):
            texto_alta = self.fuente_grande.render("¡NUEVO RÉCORD!", True, COLOR_AMARILLO)
            self.pantalla.blit(texto_alta, (ANCHO//2 - texto_alta.get_width()//2, ALTO//2 - 220))
        
        stats = self.estadisticas.obtener_estadisticas()
        textos_estadisticas = [
            f'⏱️  Tiempo total: {stats["Tiempo"]}',
            f'🎯 Movimientos: {stats["Movimientos"]}',
            f'❌ Errores: {stats["Errores"]}',
            f'💡 Pistas usadas: {stats["Pistas Usadas"]}',
            f'🎯 Dificultad: {stats["Dificultad"]}'
        ]
        
        for i, texto in enumerate(textos_estadisticas):
            texto_surf = self.fuente.render(texto, True, BLANCO)
            self.pantalla.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 80 + i * 40))
        
        boton_reiniciar = pygame.Rect(ANCHO//2 - 150, ALTO//2 + 120, 300, 60)
        mouse_pos = pygame.mouse.get_pos()
        color_reiniciar = COLOR_BOTON_HOVER if boton_reiniciar.collidepoint(mouse_pos) else COLOR_VERDE
        
        pygame.draw.rect(self.pantalla, color_reiniciar, boton_reiniciar, border_radius=15)
        pygame.draw.rect(self.pantalla, BLANCO, boton_reiniciar, 3, border_radius=15)
        
        texto_reiniciar = self.fuente.render("🎮 JUGAR DE NUEVO", True, BLANCO)
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
        self.pantalla.blit(texto_reiniciar, texto_reiniciar_rect)
        
        boton_menu = pygame.Rect(ANCHO//2 - 150, ALTO//2 + 200, 300, 60)
        color_menu = COLOR_BOTON_HOVER if boton_menu.collidepoint(mouse_pos) else COLOR_BOTON
        
        pygame.draw.rect(self.pantalla, color_menu, boton_menu, border_radius=15)
        pygame.draw.rect(self.pantalla, BLANCO, boton_menu, 3, border_radius=15)
        
        texto_menu = self.fuente.render("🏠 MENÚ PRINCIPAL", True, BLANCO)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)
        self.pantalla.blit(texto_menu, texto_menu_rect)
        
        return boton_reiniciar, boton_menu

    def dibujar_pantalla_game_over(self):
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.pantalla.blit(s, (0, 0))
        
        panel_rect = pygame.Rect(ANCHO//2 - 300, ALTO//2 - 150, 600, 300)
        
        for i in range(panel_rect.height):
            alpha = 200 - (i * 100 // panel_rect.height)
            color = (100, 0, 0, alpha)
            pygame.draw.line(self.pantalla, color, 
                           (panel_rect.x, panel_rect.y + i), 
                           (panel_rect.x + panel_rect.width, panel_rect.y + i))
        
        pygame.draw.rect(self.pantalla, (255, 255, 255, 30), panel_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, COLOR_ROJO, panel_rect, 4, border_radius=20)
        
        texto_game_over = self.fuente_grande.render("GAME OVER", True, COLOR_ROJO)
        sombra_game_over = self.fuente_grande.render("GAME OVER", True, (0, 0, 0, 100))
        self.pantalla.blit(sombra_game_over, (ANCHO//2 - texto_game_over.get_width()//2 + 2, ALTO//2 - 122))
        self.pantalla.blit(texto_game_over, (ANCHO//2 - texto_game_over.get_width()//2, ALTO//2 - 120))
        
        texto_mensaje = self.fuente.render("Has alcanzado el máximo de errores permitidos", True, BLANCO)
        self.pantalla.blit(texto_mensaje, (ANCHO//2 - texto_mensaje.get_width()//2, ALTO//2 - 30))
        
        boton_reiniciar = pygame.Rect(ANCHO//2 - 140, ALTO//2 + 30, 280, 60)
        mouse_pos = pygame.mouse.get_pos()
        color_reiniciar = COLOR_BOTON_HOVER if boton_reiniciar.collidepoint(mouse_pos) else COLOR_ROJO
        
        pygame.draw.rect(self.pantalla, color_reiniciar, boton_reiniciar, border_radius=12)
        pygame.draw.rect(self.pantalla, BLANCO, boton_reiniciar, 3, border_radius=12)
        
        texto_reiniciar = self.fuente.render("🔄 REINTENTAR", True, BLANCO)
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=boton_reiniciar.center)
        self.pantalla.blit(texto_reiniciar, texto_reiniciar_rect)
        
        boton_menu = pygame.Rect(ANCHO//2 - 140, ALTO//2 + 110, 280, 60)
        color_menu = COLOR_BOTON_HOVER if boton_menu.collidepoint(mouse_pos) else COLOR_BOTON
        
        pygame.draw.rect(self.pantalla, color_menu, boton_menu, border_radius=12)
        pygame.draw.rect(self.pantalla, BLANCO, boton_menu, 3, border_radius=12)
        
        texto_menu = self.fuente.render("🏠 MENÚ PRINCIPAL", True, BLANCO)
        texto_menu_rect = texto_menu.get_rect(center=boton_menu.center)
        self.pantalla.blit(texto_menu, texto_menu_rect)
        
        return boton_reiniciar, boton_menu

    def correr(self):
        global particulas
        
        corriendo = True
        while corriendo:
            particulas = [p for p in particulas if p.update()]
            
            corriendo = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

def main():
    try:
        print("=" * 60)
        print("SUDOKU PREMIUM - JUEGO PROFESIONAL")
        print("=" * 60)
        print("NUEVAS CARACTERÍSTICAS IMPLEMENTADAS:")
        print("✓ Sistema de Autoguardado automático cada 2 minutos")
        print("✓ Pistas Inteligentes que analizan el tablero")
        print("✓ Sistema de Logros con recompensas")
        print("✓ Temas personalizables (Clásico, Oscuro, Verde)")
        print("✓ Estadísticas avanzadas y métricas de rendimiento")
        print("✓ Protección contra pérdida de progreso")
        print("=" * 60)
        
        juego = Juego()
        
        global fuente, fuente_grande, fuente_pista
        fuente = juego.fuente
        fuente_grande = juego.fuente_grande
        fuente_pista = juego.fuente_pista
        
        juego.correr()
        
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("¡Gracias por jugar Sudoku Premium!")

if __name__ == "__main__":
    main()