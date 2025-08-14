import random
import json


#Clase AgenteVivo
class AgenteVivo:
    def __init__(self,id,nombre, vida, atributos, inventario, hambre, sed, energia,
                 estado, memoria, nivelEstres, fatiga, edad, reproduccion, sexo, alimentacion, vision,posicion):
        self.id = id
        self.nombre = nombre
        self.vida = vida
        self.atributos = atributos
        self.inventario = inventario
        self.hambre = hambre
        self.sed = sed
        self.energia = energia
        self.estado = estado
        self.memoria = memoria
        self.nivelEstres = nivelEstres
        self.fatiga = fatiga
        self.edad = edad
        self.reproduccion = reproduccion
        self.sexo = sexo
        self.alimentacion = alimentacion
        self.vision = vision
        self.posicion = posicion

    def setAtributos(self):
        self.atributos.strenght = random.randint(6, 10)
        self.atributos.perception = random.randint(6, 10)
        self.atributos.endurance = random.randint(6, 10)
        self.atributos.carisma = random.randint(6, 10)
        self.atributos.inteligence = random.randint(6, 10)
        self.atributos.luck = random.randint(6, 10)

    def to_dict_base(self):
        return {
            'id':self.id,
            'nombre': self.nombre,
            'vida': self.vida,
            'atributos': {
                'strenght': self.atributos.strenght,
                'perception': self.atributos.perception,
                'endurance': self.atributos.endurance,
                'carisma': self.atributos.carisma,
                'inteligence': self.atributos.inteligence,
                'luck': self.atributos.luck
            },
            'hambre': self.hambre,
            'sed': self.sed,
            'energia': self.energia,
            'estado': self.estado,
            'memoria': self.memoria,
            'nivelEstres': self.nivelEstres,
            'fatiga': self.fatiga,
            'edad': self.edad,
            'reproduccion': self.reproduccion,
            'sexo': self.sexo,
            'alimentacion': self.alimentacion,
            'vision': self.vision,
            'posicion':self.posicion
        }


#CLASE PERSONAJE
class Personaje(AgenteVivo):
    def __init__(self,id,nombre, vida, atributos, inventario, hambre, sed, energia,
                 estado, memoria, nivelEstres, fatiga, edad, reproduccion, sexo, alimentacion, vision,posicion,arma):
        super().__init__(id,nombre, vida, atributos, inventario, hambre, sed, energia,
                         estado, memoria, nivelEstres, fatiga, edad, reproduccion, sexo, alimentacion, vision,posicion)
        self.arma = arma

    def setArmaAleatoria(self):
        with open('BDD/Armas.json', 'r') as file:
            armas = json.load(file)
        aleatorio = random.choice(armas)
        self.arma = Arma(0, '', aleatorio['nombre'], 0, '', '', 0, 0, '', 0, 0, 0, 0, '', '')

    def setSexoAleatorio(self, cont, contMujeres):
        numSexo = random.randint(1, 2)
        if numSexo == 1:
            self.sexo = "Masculino"
        else:
            self.sexo = "Femenino"

        if cont == 5 and contMujeres == 0:
            self.sexo = "Femenino"
        if contMujeres == 5:
            self.sexo = "Masculino"
        return numSexo

    def setNombreAleatorio(self, sexo):
        nombre = ""
        apellido = ""

        if sexo == "Masculino":
            with open('BDD/nombres/nombresMasculinos.json', 'r') as file:
                nombres = json.load(file)
                nombre = random.choice(nombres)['nombre']
        else:
            with open('BDD/nombres/nombresFemeninos.json', 'r') as file:
                nombres = json.load(file)
                nombre = random.choice(nombres)['nombre']

        with open('BDD/nombres/apellidos.json', 'r') as file:
            apellidos = json.load(file)
            apellido = random.choice(apellidos)['apellido']

        self.nombre = f"{nombre} {apellido}"

    def to_dict(self):
        data = super().to_dict_base()
        data['arma'] = {'nombre': self.arma.nombre}
        return data

    def __str__(self):
        return f"Nombre: {self.nombre}, Vida: {self.vida}, Sexo: {self.sexo}, Arma: {self.arma.nombre}"

#CLASE CRIATURA
class Criatura(AgenteVivo):
    def __init__(self,id,nombre, vida, atributos, inventario, hambre, sed, energia,
                 estado, memoria, nivelEstres, fatiga, edad, reproduccion, sexo, alimentacion, vision,posicion, arma,enemigos = None):
        super().__init__(id,nombre, vida, atributos, inventario, hambre, sed, energia,
                         estado, memoria, nivelEstres, fatiga, edad, reproduccion, sexo, alimentacion, vision,posicion)
        self.arma = arma
        self.enemigos = enemigos if enemigos else []


    def setNombreAleatorio(self):
        with open('CriaturasEnemigos.json', 'r') as file:
            nombres = json.load(file)
            self.nombre = random.choice(nombres)['nombre']

    #Metodos de comportamiento, IA dentro del mapa.

    #Determina si la criatura que ve es enemiga o no
    def es_enemigo(self,otro):
         if isinstance(otro,Personaje):
              return True # Todas las criaturas atacan a los personajes
         elif isinstance(otro,Criatura):
              return otro.nombre in self.enemigos
         return False

    #VER ENTORNO
    def ver_entorno(self, mapa):
         visibles = []
         rango = self.vision
         for dx in range(-rango, rango + 1):
            for dy in range(-rango, rango + 1):
                 x = self.posicion[0] + dx
                 y = self.posicion[1] + dy
                 if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
                      celda = mapa[x][y]
                      if celda.objeto is not None and celda.objeto != self:
                           visibles.append((x, y, celda.objeto))
         return visibles

    #MOVERSE POR EL MAPA
    def moverse(self, mapa):
        opciones = []
        x0, y0 = self.posicion
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = x0 + dx
                y = y0 + dy
                if (dx != 0 or dy != 0) and 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
                    if mapa[x][y].objeto is None:
                        opciones.append((x, y))

        if opciones:
            nuevo_x, nuevo_y = random.choice(opciones)
            mapa[nuevo_x][nuevo_y].objeto = self
            mapa[x0][y0].objeto = None
            self.posicion = (nuevo_x, nuevo_y)

    #BUSCAR COMIDA
    def buscar_comida(self, mapa):
        visibles = self.ver_entorno(mapa)
        for x, y, objeto in visibles:
            if isinstance(objeto, Comida):
                return (x, y, objeto)
        return None
    
    #COMER COMIDA
    def comer(self, objeto):
        if isinstance(objeto, comida):
            self.hambre = max(0, self.hambre - objeto.valorNutricional)

    #ACTUAR GENERICO
    def actuar(self, mapa):
        comida_encontrada = self.buscar_comida(mapa)
        if comida_encontrada:
            x, y, planta = comida_encontrada
            self.mover_hacia(x, y, mapa)
            if self.posicion == (x, y):
                self.comer(planta)
                mapa[x][y].objeto = None
        else:
            self.moverse(mapa)
    
    #MOVERSE HACIA UN OBJETIVO
    def mover_hacia(self, objetivo_x, objetivo_y, mapa):
        x0, y0 = self.posicion
        dx = objetivo_x - x0
        dy = objetivo_y - y0
        paso_x = 1 if dx > 0 else -1 if dx < 0 else 0
        paso_y = 1 if dy > 0 else -1 if dy < 0 else 0
        nuevo_x = x0 + paso_x
        nuevo_y = y0 + paso_y

        if 0 <= nuevo_x < len(mapa) and 0 <= nuevo_y < len(mapa[0]):
            if mapa[nuevo_x][nuevo_y].objeto is None:
                mapa[nuevo_x][nuevo_y].objeto = self
                mapa[x0][y0].objeto = None
                self.posicion = (nuevo_x, nuevo_y)

    #METODOS DE IMPRESION DE DATOS
    def to_dict(self):
        data = super().to_dict_base()
        data['arma'] = {'nombre': self.arma.nombre}
        return data

    def __str__(self):
        return f"Nombre: {self.nombre}, Vida: {self.vida}, Sexo: {self.sexo}, Arma: {self.arma.nombre}"

        

#Clase ATRIBUTOS
class Atributos:
	def __init__(self, strenght,perception,endurance,carisma,inteligence,luck):
		self.strenght=strenght
		self.perception=perception
		self.endurance=endurance
		self.carisma=carisma
		self.inteligence=inteligence
		self.luck=luck
	def __str__(self):
		return f"\n~Strenght={self.strenght}\n~Perception={self.perception}\n~Endurance={self.endurance}\n~Carisma={self.carisma}\n~Inteligence={self.inteligence}\n~Luck={self.luck}"
		
#Clase ARMA
class Arma:
    def __init__(self, id, tipo, nombre, daño, descripcion, tipo_municion, peso, durabilidad, modificaciones, nivel_requerido, precio, rango, velocidad_disparo, rareza, efecto_especial):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre
        self.daño = daño
        self.descripcion = descripcion
        self.tipo_municion = tipo_municion
        self.peso = peso
        self.durabilidad = durabilidad
        self.modificaciones = modificaciones
        self.nivel_requerido = nivel_requerido
        self.precio = precio
        self.rango = rango
        self.velocidad_disparo = velocidad_disparo
        self.rareza = rareza
        self.efecto_especial = efecto_especial
        
    def __str__(self):
        return (f"Arma:\n"
                f"  id: {self.id}\n"
                f"  tipo: {self.tipo}\n"
                f"  nombre: {self.nombre}\n"
                f"  daño: {self.daño}\n"
                f"  descripcion: {self.descripcion}\n"
                f"  tipo_municion: {self.tipo_municion}\n"
                f"  peso: {self.peso}\n"
                f"  durabilidad: {self.durabilidad}\n"
                f"  modificaciones: {self.modificaciones}\n"
                f"  nivel_requerido: {self.nivel_requerido}\n"
                f"  precio: {self.precio}\n"
                f"  rango: {self.rango}\n"
                f"  velocidad_disparo: {self.velocidad_disparo}\n"
                f"  rareza: {self.rareza}\n"
                f"  efecto_especial: {self.efecto_especial}")
                
		
#Clase ITEM
class Item:
	def __init__(self,id,nombre,descripcion,precio):
          self.id = id
          self.nombre = nombre
          self.descripcion = descripcion
          self.precio = precio
        

        
        
        
#Clase Ambiente -- CLASE A USAR A FUTURO EN VERSIONES MEJORADAS
class Ambiente:
	def __init__(self, nombre, visibilidad,temperatura):
		self.nombre=nombre
		self.visibilidad=visibilidad
		self.temperatura=temperatura
        

class Edificio:
    def __init__(self,id,nombre,tipoEdificio):
        self.id = id
        self.nombre = nombre
        self.tipoEdificio = tipoEdificio

class tipoEdificio:
     def __init__(self,id,nombre,color,numPisos,pisos):
          self.id = id
          self.nombre = nombre
          self.color = color
          self.numPisos = numPisos
          
class Piso:
     def __init__(self,id,numPiezas,piezas):
          self.id = id
          self.numPiezas = numPiezas
          self.piezas = piezas

class Pieza:
     def __init__(self,id,nombre,tipoPieza):
          self.id = id
          self.nombre = nombre
          self.tipoPieza = tipoPieza

class tipoPieza:
     def __init__(self,id,nombre,criaturas,items,comidas,armas):
          self.id = id
          self.nombre = nombre
          self.criaturas = criaturas
          self.items = items
          self.comidas = comidas
          self.armas = armas

class Comida:
     def __init__(self,id,nombre,valorNutricional,descripcion):
          self.id = id
          self.nombre = nombre
          self.valorNutricional = valorNutricional
          self.descripcion = descripcion

     
     
class Planta(Comida):
     def __init__(self, id, nombre, valorNutricional, descripcion,consumida):
          super().__init__(id, nombre, valorNutricional, descripcion)
          self.consumida = consumida


    #Conecta directamente con la criatura que se la come.
     def ser_comida(self,criatura):
          if not self.consumida:
               criatura.hambre = max(0, criatura.hambre - self.valorNutricional)
               self.cantidad -= 1
               if self.cantidad <= 0:
                    self.consumida = True
               return True
          return False
    