#Documentación de archivos.

## main.py
	-- Archivo principal que lo corre todo.
	-- Paso a paso : 
		#Primero Muestra el menu de opciones.
		#Permite elegir una opcion al usuario.
		**OPCION 1** 
			Permite a usuario crear nuevo refugio y gestionarlo.
			
			#CREACIÓN NUEVO REFUGIO 
			- Pide al usuario darle un numero al refugio
			- Crea una carpeta de saves donde se guardan los datos
			- Dentro de saves crea carpeta para refugio creado
			- Crea una lista de 5 personajes aleatorios.
				#Creación de personajes
				- Dentro de la clase Personaje se crean atributos
				aleatorios, le da una arma aleatoria(Armas.json) 
				y le da nombre y apellido aleatorios(NombresApellidos.json)
			- Los 5 personajes se guardan dentro de un json dentro de la carpeta saves
			
		**OPCION 2** 
			Permite cargar la partida y gestionarlo
			
			#Carga de refugio
			- Pide al usuario que ingrese el refugio que quiere 
			cargar.

		**OPCION 3**
			Se sale del juego


			
	-- Una vez creado o cargado el refugio muestra en pantalla las opciones dentro de este
	
			# 1. Salir a explorar
				- Se inicia el MapaGrafico.py 
				
## MapaGrafico.py
				- Se inicializa tamaño del mapa, tamaño de cuadros de
				este, cantidad de casillas y colores a utilizar.
				Se crea una clase CeldaMapa, para transformar 
				cada celda en un objeto.
				- Se crea la matriz del tamaño del mapa.
				- Se le agrega una cantidad de celdas aleatorias
				diferentes a la base (casas, edificios y lugares importantes)
				- Se cargan los personajes del json de personajes.
				- Se crea lista en donde se dejan esos personajes.
				- Deja a los personajes dentro del mapa en un lugar
				aleatorio.
				- Se comienza a ejecutar el mapa de color negro.
				- Obtiene las coordenadas del mouse.
				- Dibuja el mapa por completo y además detecta 
				si es que el mouse está encima de un personaje para
				mostrar sus datos en un pop-up.
				- Se cargan las criaturas/animales. 
				- Cada una de estas tiene su propio arbol de comportamientos (IA).

## Clases.py
	-- **AgenteVivo**: Clase base. Contiene atributos comunes a todos los seres vivos del juego (vida, hambre, sed, energía, atributos, estado, memoria, estrés, fatiga, edad, sexo, alimentación, visión, posición).
  		- Métodos clave: 
    	- `to_dict_base()`: Para serializar el estado base.
    	- `setAtributos()`: Para inicializar atributos.

	--**Personaje**: Hereda de `AgenteVivo`. Representa los personajes jugables, con métodos para la gestión de atributos y sexo.
	-- **Criatura**: Hereda de `AgenteVivo`. Es la base de los enemigos/animales controlados por IA.
		- Métodos principales (IA integrada):
			- `ver_entorno(mapa)`: Devuelve objetos/entidades cercanas dentro del rango de visión.
			- `moverse(mapa)`: Movimiento aleatorio si no hay nada relevante cerca.
			- `buscar_comida(mapa)`: Busca comida en el entorno visible.
			- `comer(objeto)`: Consume comida y reduce el hambre.
			- `actuar(mapa)`: Lógica de decisión: si hay comida, va hacia ella y la consume; si no, se mueve aleatoriamente.
			- `mover_hacia(x, y, mapa)`: Mueve la criatura hacia unas coordenadas objetivo.
			- `es_enemigos` : En caso de que el objeto sea un Personaje o una criatura distinta, arroja True
			
## Comportamiento.py
	**NodoVerEntorno** : Busca por objetos dentro del mapa. En caso de que ve algo devuelve EXITO, en caso contrario
	devuelve FALLO. Guarda la informacion en la memoria de la criatura.

	**NodoMoverAleatorio** : Considera 8 posibles movimientos. Solo en caso de movimiento valido se mueve.

	**NodoAtacar** : Filtra si es que hay enemigos, en el caso de que si, ataca al mas cercano. 

	**NodoBuscarComida** : Busca comida, elige comida, se dirige a comida e intenta comerla.

	`Nodos compuestos`

	**NodoSecuencia** : Ejecuta hijos hasta que uno falle.
	**NodoSelector** : Ejecuta hijos hasta que uno tenga exito.

	`Prioridades` : 1)Buscar comida
				  2)Atacar enemigos
				  3)Moverse aleatoriamente. 
