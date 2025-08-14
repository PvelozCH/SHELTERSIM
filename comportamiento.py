from Clases import Planta,Personaje,Criatura
import random
# =========================
# ESTADOS DE EJECUCIÓN
# =========================
EXITO = "EXITO"
FALLO = "FALLO"
EJECUTANDO = "EJECUTANDO"

# =========================
# NODOS HOJA (Acciones básicas)
# =========================

class NodoVerEntorno:
    def __init__(self, criatura, mapa):
        self.criatura = criatura
        self.mapa = mapa

    def ejecutar(self):
        if not hasattr(self.criatura, "vision") or not hasattr(self.criatura, "posicion"):
            return FALLO

        vision = self.criatura.vision
        pos_x, pos_y = self.criatura.posicion

        celdas_visibles = []
        for dx in range(-vision, vision + 1):
            for dy in range(-vision, vision + 1):
                nuevo_x = pos_x + dx
                nuevo_y = pos_y + dy
                if 0 <= nuevo_x < len(self.mapa) and 0 <= nuevo_y < len(self.mapa[0]):
                    celda = self.mapa[nuevo_x][nuevo_y]
                    if celda.objeto:
                        celdas_visibles.append({
                            "x": nuevo_x,
                            "y": nuevo_y,
                            "objeto": celda.objeto  # Ahora guardamos el objeto completo, no solo el string
                        })

        self.criatura.memoria = celdas_visibles
        return EXITO if celdas_visibles else FALLO

class NodoMoverAleatorio:
    def __init__(self, criatura, mapa):
        self.criatura = criatura
        self.mapa = mapa

    def ejecutar(self):
        x, y = self.criatura.posicion
        direcciones = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)
        ]
        
        # Filtramos direcciones válidas
        posibles = []
        for nx, ny in direcciones:
            if 0 <= nx < len(self.mapa) and 0 <= ny < len(self.mapa[0]):
                """
                if self.mapa[nx][ny].objeto is None:  # Movimiento solo si es que la celda esta vacia.
                    posibles.append((nx, ny))
                """
                #Por ahora que se pueda mover a donde sea, aunque haya una criatura o un objeto.
                posibles.append((nx,ny))
        
        if posibles:
            nuevo_x, nuevo_y = random.choice(posibles)
            # Actualizamos posición en el mapa
            self.mapa[x][y].objeto = None
            self.mapa[nuevo_x][nuevo_y].objeto = self.criatura
            self.criatura.posicion = (nuevo_x, nuevo_y)
            return EXITO
        return FALLO

class NodoAtacar:
    def __init__(self, criatura, mapa):
        self.criatura = criatura
        self.mapa = mapa

    def ejecutar(self):
        # Buscamos objetivos en la memoria (vistos recientemente) / ataca personajes y otro tipo de criaturas
        objetivos = [obj for obj in self.criatura.memoria 
                    if (isinstance(obj['objeto'], Personaje) or 
                        (isinstance(obj['objeto'],Criatura) and 
                         self.criatura.es_enemigo(obj['objeto'])))]
        
        if not objetivos:
            return FALLO
        
        # Elegimos el objetivo más cercano
        objetivo = min(objetivos, key=lambda obj: 
                      abs(obj['x'] - self.criatura.posicion[0]) + 
                      abs(obj['y'] - self.criatura.posicion[1]))
        
        # Verificamos si está al alcance (adyacente)
        x, y = self.criatura.posicion
        if abs(objetivo['x'] - x) <= 1 and abs(objetivo['y'] - y) <= 1:
            # Calculamos daño basado en atributos y arma
            daño = max(1, self.criatura.atributos.strenght // 2 + 
                       (self.criatura.arma.daño if hasattr(self.criatura.arma, 'daño') else 5))
            
            objetivo['objeto'].vida -= daño
            print(f"{self.criatura.nombre} atacó a {objetivo['objeto'].nombre} causando {daño} de daño!")
            
            if objetivo['objeto'].vida <= 0:
                print(f"{objetivo['objeto'].nombre} ha muerto!")
                self.mapa[objetivo['x']][objetivo['y']].objeto = None
            return EXITO
        return FALLO

class NodoBuscarComida:
    def __init__(self, criatura, mapa):
        self.criatura = criatura
        self.mapa = mapa

    def ejecutar(self):
        # Buscamos comida en la memoria
        comidas = [obj for obj in self.criatura.memoria 
                  if isinstance(obj['objeto'], Planta) and not obj['objeto'].consumida]
        
        if not comidas:
            return FALLO
        
        # Elegimos la comida más cercana
        comida = min(comidas, key=lambda obj: 
                    abs(obj['x'] - self.criatura.posicion[0]) + 
                    abs(obj['y'] - self.criatura.posicion[1]))
        
        # Moverse hacia la comida
        x, y = self.criatura.posicion
        dx = comida['x'] - x
        dy = comida['y'] - y
        
        # Determinamos dirección (movimiento en un eje a la vez)
        nuevo_x, nuevo_y = x, y
        if abs(dx) > abs(dy):
            nuevo_x += 1 if dx > 0 else -1
        else:
            nuevo_y += 1 if dy > 0 else -1
        
        # Verificamos si podemos movernos allí
        if (0 <= nuevo_x < len(self.mapa)) and (0 <= nuevo_y < len(self.mapa[0])):
            if self.mapa[nuevo_x][nuevo_y].objeto is None:
                # Actualizamos posición
                self.mapa[x][y].objeto = None
                self.mapa[nuevo_x][nuevo_y].objeto = self.criatura
                self.criatura.posicion = (nuevo_x, nuevo_y)
                
                # Si llegamos a la comida, comer
                if nuevo_x == comida['x'] and nuevo_y == comida['y']:
                    if comida['objeto'].ser_comida(self.criatura):
                        print(f"{self.criatura.nombre} comió {comida['objeto'].nombre}!")
                        if comida['objeto'].consumida:
                            self.mapa[nuevo_x][nuevo_y].objeto = None
                        return EXITO
                    return FALLO
                return EJECUTANDO
        return FALLO

# =========================
# NODOS COMPUESTOS (Control de flujo)
# =========================

class NodoSecuencia:
    def __init__(self, hijos):
        self.hijos = hijos
    
    def ejecutar(self):
        for hijo in self.hijos:
            resultado = hijo.ejecutar()
            if resultado != EXITO:
                return resultado
        return EXITO

class NodoSelector:
    def __init__(self, hijos):
        self.hijos = hijos
    
    def ejecutar(self):
        for hijo in self.hijos:
            resultado = hijo.ejecutar()
            if resultado != FALLO:
                return resultado
        return FALLO

# =========================
# ÁRBOL DE COMPORTAMIENTO
# =========================

class ArbolComportamiento:
    def __init__(self, criatura, mapa):
        self.criatura = criatura
        self.mapa = mapa
        self.construir_arbol()
    
    def construir_arbol(self):
        # Definimos el árbol de comportamiento
        self.raiz = NodoSelector([
            # Prioridad 1: Si hay comida cerca, ir a comer
            NodoSecuencia([
                NodoVerEntorno(self.criatura, self.mapa),
                NodoBuscarComida(self.criatura, self.mapa)
            ]),
            
            # Prioridad 2: Si hay enemigos cerca, atacar
            NodoSecuencia([
                NodoVerEntorno(self.criatura, self.mapa),
                NodoAtacar(self.criatura, self.mapa)
            ]),
            
            # Prioridad 3: Moverse aleatoriamente
            NodoMoverAleatorio(self.criatura, self.mapa)
        ])
    
    def ejecutar(self):
        return self.raiz.ejecutar()