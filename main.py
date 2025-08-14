#CLASE MAIN - PRINCIPAL
from Clases import Personaje, Atributos, Arma, Ambiente, Item
import os,json,platform,random
import MapaGrafico as mapa

# --- Métodos dentro del juego

#Detecta el sistema que se usa
def sistema():
    so = platform.system()
    return so
    
#Limpia la pantalla
def clean_screen():
    if sistema() == "Windows":
        os.system("cls")
    elif sistema() == "Linux":
        os.system('clear')

def clic_continuar():
    input("Haz clic para continuar: ")

#Menu inicial del juego
def mostrar_menu_principal():
    print("*Fallout*")
    print("1. Juego nuevo")
    print("2. Cargar juego")
    print("3. Salir")

#Numero de refugio 
num_refugio = 0
#Creacion de nuevo refugio, devuelve el número del refugio
def nuevo_refugio():
    clean_screen()
    print("*Nuevo refugio*")
    #Se pide a usuario número de refugio 
    num_refugio = input("Asigna un número al refugio: ")
    clean_screen()
    print(f"Bienvenido al refugio {num_refugio}")
    
    # Verificar si la carpeta 'saves' existe, si no, crearla
    if not os.path.exists('saves'):
        os.makedirs('saves')

    # Crear la carpeta del refugio para saves
    refugio_path = os.path.join('saves',
    f"Refugio{num_refugio}")
    if not os.path.exists(refugio_path):
        os.makedirs(refugio_path)
        
     #Crear aleatoriamente a los habitantes del refugio 
     
     #CREACIÓN DE PERSONAJES DEL REFUGIO
    personajes = []
    
    atributo_inicial = Atributos(0, 0, 0, 0, 0, 0)
    arma_inicial = Arma(0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0)
    
    #Contadores de personajes y contadores de mujeres para comprobar que siempre haya al menos una mujer para que se puedan reproducir
    cont = 0
    contMujeres = 0
    #Se crean 5 personajes aleatorios
    for i in range(5):
        cont +=1
        nombre_personaje = f"nom{i+1}"
        personaje = Personaje(cont,nombre_personaje, 100,atributo_inicial,0,0,0,100,"tranquilo",0,0,0,18,"Sexual",0,"Omnivoro",5,"posicionBase",arma_inicial)
        personaje.setAtributos()
        personaje.setSexoAleatorio(cont,contMujeres)
        if personaje.sexo == "Femenino":
             contMujeres +=1
        personaje.setNombreAleatorio(personaje.sexo)
        personaje.setArmaAleatoria()
        print(personaje)
        personajes.append(personaje)
        
    # Guardar personajes en un archivo JSON
    with open(os.path.join(refugio_path, 
        'personajes.json'), 'w') as file:
        json.dump([personaje.to_dict() for personaje in personajes],
        file, indent=4)
        input("Presione Enter para continuar")
        
    #CREACIÓN DE CRIATURAS EN EL MUNDO
    
    #Se abre json de base de datos de criaturas
    with open("BDD/CriaturasEnemigos.json","r") as file:
         criaturas = json.load(file)

    #Se eligen x criaturas al azar
    criaturas = random.choices(criaturas,k=25)

    #Guardar en la partida la cantidad de criaturas
    with open(os.path.join(refugio_path,'criaturas.json'),'w') as file:
         json.dump(criaturas,file,indent=4)
         

    #CREACION DE FRUTAS Y PLANTAS EN EL MUNDO

    #Se abre json de base de datos de frutas y plantas
    with open("BDD/frutasYplantas.json","r") as file:
         plantas = json.load(file)
    
    #Se eligen 120 plantas al azar
    plantas = random.choices(plantas,k=120)

    #Guardar en la partida la cantidad de criaturas
    with open(os.path.join(refugio_path,'vegetacion.json'),'w') as file:
         json.dump(plantas,file,indent=4)


    return num_refugio
        
        
#Menu al estar dentro de un refugio
def opciones_refugio():
   clean_screen()
   print("**Te encuentras en el refugio**")
   print("1. Salir a explorar")
   print("2. Ver recursos")
   print("3. Listar habitantes")
   print("4. Salir")

#Eleccion dentro de un refugio cargado
def elegir_opcion_refugio(numRefugio):
    opcion = 0
    while opcion != 4:
        #Muestra las opciones dentro del refugio
        opciones_refugio()
        opcion = int(input("Elige una opcion: "))
        clean_screen()
        if opcion == 1:
            print("saliste a explorar...")
            mapa.iniciarMapa(numRefugio)
        elif opcion == 2:
            print("Recursos disponibles: ")
            clic_continuar()
        elif opcion == 3:
            print("Lista de habitantes")
            clic_continuar()    
    

def cargar_partida():
    clean_screen()
    num = int(input("Ingrese el refugio al que quiere entrar: "))

    return num

def salir():
    print("Hasta pronto")
    
    


# --- Función principal del juego

def main():
    clean_screen()
    #Muestra menu principal
    mostrar_menu_principal()
    opcion = int(input("Elige una opción: "))
    #Crear refugio nuevo
    if opcion == 1:
            elegir_opcion_refugio(nuevo_refugio())
    elif opcion == 2:
            elegir_opcion_refugio(cargar_partida())
    elif opcion == 3:
            salir()
            clean_screen()
    else:
            print("Opción no válida")
            

if __name__ == "__main__":
    main()
