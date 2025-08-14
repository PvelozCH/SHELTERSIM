#MAPA GRAFICO
import pygame
import random
#Para conectar personajes y elementos dentro del mapa.
from Clases import Personaje,Atributos,Arma,Criatura,Planta
from comportamiento import ArbolComportamiento
import json

def iniciarMapa(numRefugio):
    # Inicializar Pygame
    pygame.init()

    # =========================
    # VARIABLES IMPORTANTES
    # =========================

    #Tamano mapa
    TILE_SIZE = 10  #Tamaño de cada cuadro.
    fuente = pygame.font.SysFont("arial", 12) #Fuente de texto

    #Colores a usar
    BASE = (1,18,1) # verde base 
    AGUA = (0, 48, 0)   #verde muy oscuro
    EDIFICIO = (1,143,1) #verde claro intenso

    #Cantidad de relieves/elementos aleatorios
    cantRelieves = 385

    #Variables de conteo de ejecucion del mapa
    tiempo_ultima_actualizacion = 0
    intervalo_actualizacion = 800 #Numero de milisegundos que demoran en actuar la IA

    #Cantidad de cuadros en el mapa
    pixelesX = 800
    pixelesY = 600

    # =========================
    # FIN VARIABLES IMPORTANTES
    # =========================

    
    screen = pygame.display.set_mode((pixelesX, pixelesY))
    clock = pygame.time.Clock() 


    ## Cantidad de casillas por ancho y por largo
    cantCasillasX = int((pixelesX/TILE_SIZE))
    cantCasillasY = int((pixelesY/TILE_SIZE))
   
    #Plantilla para cada una de las celdas del mapa.
    class CeldaMapa:
        def __init__(self, x,y,tipo_terreno,objeto=None):
            self.x = x
            self.y = y
            self.tipo_terreno = tipo_terreno
            self.objeto = objeto

    # Crea la matriz del mapa con terreno base
    mapa = []
    for x in range(cantCasillasX):
        fila = []
        for y in range(cantCasillasY):
            fila.append(CeldaMapa(x,y,BASE))
        mapa.append(fila)

    for _ in range(cantRelieves): # Crea x cantidad de relieves aleatorios
        x = random.randint(0, cantCasillasX - 1)
        y = random.randint(0, cantCasillasY - 1)
        color = random.choice([BASE, AGUA, EDIFICIO])
        mapa[x][y].tipo_terreno = color
        
    #Cargar personajes desde Partida
    ruta_personajes = f"saves/Refugio{numRefugio}/personajes.json"

    personajes = [] #Lista dinámica de personajes dentro del mapa
    try:
        with open(ruta_personajes, "r") as file:
            datos = json.load(file)
        for p in datos:
            #carga la informacion dentro del json
            atributos = Atributos(**p['atributos'])
            arma = Arma(0, '', p['arma']['nombre'], 0, '', '', 0, 0, '', 0, 0, 0, 0, '', '')
            personaje = Personaje(p['id'],p['nombre'], p['vida'],atributos,0,p['hambre'],p['sed'],p['energia'],p['estado'],p['memoria'],p['nivelEstres'],p['fatiga'],p['edad'],p['reproduccion'],p['sexo'],p['alimentacion'],p['vision'],p['posicion'],arma)
            personajes.append(personaje)

        # Posicionar personajes en el mapa de manera aleatoria
        for personaje in personajes:
            while True:
                #Los personajes solo aparecen en una esquina del mapa
                x = random.randint(0,6)
                y = random.randint(0,6)
                if mapa[x][y].objeto is None:
                    mapa[x][y].objeto = personaje
                    break
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_personajes}")
        personajes = []

    #Cargar criaturas desde Partida
    ruta_criaturas = f"saves/Refugio{numRefugio}/criaturas.json"

    criaturas = [] #Lista dinamica criaturas
    try:
        with open(ruta_criaturas,"r") as file:
              datos = json.load(file)
        for c in datos:
            
            atributos = Atributos(**c['atributos'])
            arma = Arma(0, '', c['arma']['nombre'], 0, '', '', 0, 0, '', 0, 0, 0, 0, '', '')
            criatura = Criatura(c['id'],c['nombre'], c['vida'],atributos,0,c['hambre'],c['sed'],c['energia'],c['estado'],c['memoria'],c['nivelEstres'],c['fatiga'],c['edad'],c['reproduccion'],c['sexo'],c['alimentacion'],c['vision'],c['posicion'],arma,enemigos=c.get('enemigos',[]))
            criaturas.append(criatura)
        
        #posicionar criaturas en mapa aleatoriamente
        for criatura in criaturas:
            while True:
                 x = random.randint(7,cantCasillasX -1)
                 y = random.randint(7,cantCasillasY -1)

                 if mapa[x][y].objeto is None:
                    mapa[x][y].objeto = criatura
                    criatura.posicion = (x,y)

                    break
                 
    except FileExistsError:
         print(f"No se encontro archivo: {ruta_criaturas}")
         criaturas = []
    

    #Cargar vegetacion desde Partida
    ruta_vegetacion = f"saves/Refugio{numRefugio}/vegetacion.json"

    plantas = [] #Lista dinamica criaturas
    try:
        with open(ruta_vegetacion,"r") as file:
              datos = json.load(file)
        for v in datos:
            planta = Planta(v['id'],v['nombre'],v['valorNutricional'],v['descripcion'],v['consumida'])
            plantas.append(planta)
        
        #posicionar criaturas en mapa aleatoriamente
        for planta in plantas:
            while True:
                 x = random.randint(7,cantCasillasX -1)
                 y = random.randint(7,cantCasillasY -1)

                 if mapa[x][y].objeto is None:
                    mapa[x][y].objeto = planta
                    break
                 
    except FileExistsError:
         print(f"No se encontro archivo: {ruta_vegetacion}")
         plantas = []

    # Bucle principal -- inicio del mapa
    running = True 
    while running: # mientras se esté ejecutando

        tiempo_actual = pygame.time.get_ticks()
        

        #Obtener posición del mouse
        mouse_x,mouse_y = pygame.mouse.get_pos()
        celda_hover = None
        
       

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Si le doy a la x se cierra
                running = False
                
            if event.type == pygame.KEYDOWN: # Si le doy al esc se cierra
                 if event.key == pygame.K_ESCAPE:
                     running = False


        #Actualizacion de IA cada 4 segundos.
        if tiempo_actual - tiempo_ultima_actualizacion >= intervalo_actualizacion:
             tiempo_ultima_actualizacion = tiempo_actual

             #Actualizacion de criaturas 
             for x in range(len(mapa)):
                  for y in range(len(mapa[0])):
                       celda = mapa[x][y]
                       if celda.objeto and isinstance(celda.objeto, Criatura):
                            criatura = celda.objeto

                            #verificar posicion de criatura
                            if criatura.posicion == (x,y):
                                 arbol = ArbolComportamiento(criatura,mapa)
                                 resultado = arbol.ejecutar()
                                 print(f"{criatura.nombre} en ({x},{y}): {resultado}")
        
        
        screen.fill((0,0,0)) # se llena la pantalla de color negro

        # Dibujar el mapa
        for fila in mapa:
            for celda in fila:
                # Dibuja el rectángulo de color del terreno
                pygame.draw.rect(screen, celda.tipo_terreno,
                                 (celda.x * TILE_SIZE, celda.y * TILE_SIZE,
                                  TILE_SIZE, TILE_SIZE))

                # Dibuja el borde negro alrededor de la celda
                pygame.draw.rect(screen, (0, 0, 0),
                                 (celda.x * TILE_SIZE, celda.y * TILE_SIZE,
                                  TILE_SIZE, TILE_SIZE), 1)  # El último "1" es el grosor del borde

                # Dibujar personajes si es que existe
                if celda.objeto and isinstance(celda.objeto, Personaje):
                    pygame.draw.circle(screen, (0,255,247),
                                       (celda.x * TILE_SIZE + TILE_SIZE // 2,
                                        celda.y * TILE_SIZE + TILE_SIZE // 2),
                                       TILE_SIZE // 2)
                    
                # Dibujar criaturas si es que existen
                if celda.objeto and isinstance(celda.objeto, Criatura):
                    pygame.draw.circle(screen, (176,5,5),
                                       (celda.x * TILE_SIZE + TILE_SIZE // 2,
                                        celda.y * TILE_SIZE + TILE_SIZE // 2),
                                       TILE_SIZE // 2)

                #Detenctar mouse encima de un personaje
                if (celda.x * TILE_SIZE <= mouse_x <= (celda.x + 1) * TILE_SIZE and
                                        celda.y * TILE_SIZE <= mouse_y <= (celda.y + 1) * TILE_SIZE):
                                        celda_hover = celda

                


        #Mostrar pop up con datos de personajes
        if celda_hover and isinstance(celda_hover.objeto, Personaje):
            personaje = celda_hover.objeto
            info = [
                f"Nombre: {personaje.nombre}",
                f"Vida: {personaje.vida}"
            ]
            tooltip_x = mouse_x + 10
            tooltip_y = mouse_y + 10
            padding = 5
            line_height = 15
            width = max([fuente.size(text)[0] for text in info]) + padding * 2
            height = line_height * len(info) + padding * 2
            pygame.draw.rect(screen, (255, 255, 200), (tooltip_x, tooltip_y, width, height))
            pygame.draw.rect(screen, (0, 0, 0), (tooltip_x, tooltip_y, width, height), 1)

            for i, text in enumerate(info):
                render = fuente.render(text, True, (0, 0, 0))
                screen.blit(render, (tooltip_x + padding, tooltip_y + padding + i * line_height))

                
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Ejecutar la función solo si el archivo es el principal
if __name__ == "__main__":
    iniciarMapa()
