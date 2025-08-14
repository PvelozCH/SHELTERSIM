import pygame
import random
import noise
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

'''
###
#CONFIGURACION MAPA
###
''' 

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tituloPantalla = "Generador de Mapa Procedural"
pygame.display.set_caption(tituloPantalla) # Titulo pantalla

# Configuración del mapa
TILE_SIZE = 4  # Tamaño de cada celda en píxeles
MAP_WIDTH = WIDTH // TILE_SIZE  # Ancho del mapa en celdas
MAP_HEIGHT = HEIGHT // TILE_SIZE  # Alto del mapa en celdas

# Semilla aleatoria (para reproducibilidad)
SEED = random.randint(0, 9999)
random.seed(SEED)

# Paleta de colores para los biomas
WATER_COLORS = [(65, 105, 225), (70, 130, 180), (0, 105, 148)]  # Azules para agua
SAND_COLOR = (194, 178, 128)  # Arena/playa
GRASS_COLORS = [(34, 139, 34), (0, 100, 0), (85, 107, 47)]  # Verdes para tierra



# Configuración del ruido Perlin
OCTAVES = 12          # Número de capas de ruido para mayor detalle
PERSISTENCE = 0.53    # Controla la influencia de cada octava
LACUNARITY = 2.0     # Controla la frecuencia de cada octava
SCALE = 10.0        # Escala del ruido (mayor = más suave)
REPEAT = 1024

# Matriz para almacenar el mapa
world_map = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

'''
###
#IMPORTACION DE OBJETOS DENTRO DEL MAPA
### 
''' # Criaturas, personajes, edificios, etc.

# Listas de objetos dentro del mapa
structures = []  
criaturas = []
personajes = []

def generarPersonajes():
    a = 0

def generarCriaturas():
    a = 0 

#Genera estructuras, lugares, etc.
def generarEstructuras(x,y): 
    
    STRUCTURE_COLORS = {
    'house': (139, 69, 19),  # Marrón (casas)
    'tower': (47, 79, 79),   # Gris oscuro (torres)
    'ruin': (112, 128, 144)  # Gris claro (ruinas)
    }
    
    '''
    GENERA NUMERO ALEATORIO DE ESTRUCTURAS SOLAMENTE EN TIERRA ADECUADA
    '''
    if world_map[y][x]['type'] in ['grass', 'sand'] and random.random() < 0.005: #0.5%
                structures.append({
                    'type': random.choice(['house', 'tower', 'ruin']),
                    'x': x,
                    'y': y,
                    'size': 2,
                    'color': STRUCTURE_COLORS[random.choice(['house', 'tower', 'ruin'])]
                })

'''
###
#GENERACION DE TERRENO
###
''' 

def generate_terrain():
    """Genera el terreno usando ruido Perlin"""
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            # Normalizar coordenadas para el ruido Perlin
            nx = x / MAP_WIDTH - 0.5
            ny = y / MAP_HEIGHT - 0.5
            
            # Generar valores de ruido para elevación y humedad
            elevation = noise.pnoise2(nx, ny, octaves=OCTAVES, 
                                    persistence=PERSISTENCE, 
                                    lacunarity=LACUNARITY, 
                                    repeatx=REPEAT, 
                                    repeaty=REPEAT, 
                                    base=SEED)
            
            moisture = noise.pnoise2(nx + 1000, ny + 1000, octaves=OCTAVES,
                                   persistence=PERSISTENCE,
                                   lacunarity=LACUNARITY,
                                   repeatx=REPEAT,
                                   repeaty=REPEAT,
                                   base=SEED + 1)
            
            # Determinar el tipo de terreno basado en la elevación
            if elevation < -0.1:
                # Agua profunda
                world_map[y][x] = {'type': 'water', 'depth': 2}
            elif elevation < 0:
                # Agua poco profunda
                world_map[y][x] = {'type': 'water', 'depth': 1}
            elif elevation < 0.04: #Cantidad de arena
                # Arena/playa
                world_map[y][x] = {'type': 'sand'}
            else: #Cualquier elevacion > 0.04 se convierte en hierba
                # Tierra/pradera
                if moisture > 0.1:
                    world_map[y][x] = {'type': 'grass', 'variation': 1}  # Hierba húmeda
                else:
                    world_map[y][x] = {'type': 'grass', 'variation': 0}  # Hierba seca

            # GENERAR DENTRO DEL MAPA OBJETOS 
            generarPersonajes()
            generarEstructuras(x,y)
            generarCriaturas()

def draw_map():
    """Dibuja el mapa en la pantalla"""
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = world_map[y][x]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            # Asignar color según el tipo de terreno
            if tile['type'] == 'water':
                color = WATER_COLORS[tile['depth']]
            elif tile['type'] == 'sand':
                color = SAND_COLOR
            elif tile['type'] == 'grass':
                color = GRASS_COLORS[tile['variation']]
            
            pygame.draw.rect(screen, color, rect)
    
    # Dibujar estructuras
    for structure in structures:
        rect = pygame.Rect(
            structure['x'] * TILE_SIZE,
            structure['y'] * TILE_SIZE,
            structure['size'] * TILE_SIZE,
            structure['size'] * TILE_SIZE
        )
        pygame.draw.rect(screen, structure['color'], rect)

# Generar y dibujar el mapa
generate_terrain()

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_r:  # Regenerar mapa con nueva semilla
                SEED = random.randint(0, 9999)
                random.seed(SEED)
                world_map = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
                structures = []
                generate_terrain()
    
    # Dibujar
    screen.fill((0, 0, 0))  # Limpiar pantalla
    draw_map()
    
    # Mostrar información
    font = pygame.font.SysFont(None, 24)
    info_text = f"Semilla: {SEED} (Presiona R para regenerar)"
    text_surface = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()