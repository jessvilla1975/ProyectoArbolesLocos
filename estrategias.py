"""descripcion: Este archivo contiene las estrategias de búsqueda que se pueden utilizar para 
encontrar una ruta desde el ratón hasta el queso en un laberinto.
version: 1.0
"""
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import pygraphviz as pgv 
from io import BytesIO
from PIL import Image, ImageTk
import time
import random
import heapq
resul = []

def cargar_matriz(archivo):
    with open(archivo, 'r') as f:
        matriz = [list(map(int, line.strip().split())) for line in f] 

    posicion_raton = None # Posición inicial del ratón
    posicion_queso = None # Posición del queso
    ratoneras = [] # Posiciones de las ratoneras

    for i in range(len(matriz)): # Recorrer la matriz
        for j in range(len(matriz[0])):
            if matriz[i][j] == 2:
                posicion_raton = (i, j)
            elif matriz[i][j] == 3:
                posicion_queso = (i, j)
            elif matriz[i][j] == 4:
                ratoneras.append((i, j))

    return matriz, posicion_raton, posicion_queso, ratoneras

def dibujar_arbol(arbol, nodo_actual, path=[]):
    G = pgv.AGraph(strict=False, directed=True) # Crear un grafo dirigido

    # Crear las aristas del árbol
    for nodo in arbol: # Recorrer los nodos del árbol
        if arbol[nodo]: # Si el nodo tiene hijos
            for hijo in arbol[nodo]: # Recorrer los hijos
                G.add_edge(str(nodo), str(hijo)) # Agregar una arista del nodo al hijo

    # Dibujar los nodos
    for nodo in G.nodes():
        G.get_node(nodo).attr['label'] = nodo
        G.get_node(nodo).attr['shape'] = 'ellipse'
        G.get_node(nodo).attr['style'] = 'filled'  # Hacer que el nodo esté relleno
        G.get_node(nodo).attr['fontcolor'] = 'white'  # Cambiar el color del texto del label a blanco

        if str(nodo) in [str(p) for p in path]: # Si el nodo está en el camino
            G.get_node(nodo).attr['color'] = 'green'
            G.get_node(nodo).attr['fillcolor'] = 'green'  # Rellenar con color verde
        elif str(nodo) == str(nodo_actual):
            G.get_node(nodo).attr['color'] = 'red'
            G.get_node(nodo).attr['fillcolor'] = 'red'  # Rellenar con color rojo
        else:
            G.get_node(nodo).attr['color'] = 'black'  # Cambiar el borde a negro
            G.get_node(nodo).attr['fillcolor'] = 'black'  # Rellenar con color negro

    # Generar el layout y guardar la imagen
    G.layout(prog='dot') 

    # Crear un buffer en memoria para guardar la imagen
    buf = BytesIO()
    # Dibujar el grafo en el buffer en formato PNG
    G.draw(buf, format='png')
    # Mover el puntero del buffer al inicio
    buf.seek(0) 

    return Image.open(buf)
    


def tiene_hijos_no_explorados(nodo, arbol, matriz, visited):
    filas, columnas = len(matriz), len(matriz[0])
    vecinos = [
        (nodo[0] - 1, nodo[1]),  # Arriba
        (nodo[0] + 1, nodo[1]),  # Abajo
        (nodo[0], nodo[1] - 1),  # Izquierda
        (nodo[0], nodo[1] + 1)   # Derecha
    ]
    vecinos_validos = [
        v for v in vecinos
        if 0 <= v[0] < filas and 0 <= v[1] < columnas and matriz[v[0]][v[1]] != 1
    ]
    for vecino in vecinos_validos:
        if vecino not in visited and vecino not in arbol.get(nodo, []):
            return True
    return False

def obtener_nodo_no_explorado(arbol, visited):
    for nodo, hijos in arbol.items(): # Recorrer el árbol
        for hijo in hijos: # Recorrer los hijos
            if hijo not in visited: # Si el hijo no ha sido visitado
                return hijo # Devolver el hijo
    return None


def obtener_nodo_no_explorado_mas_cercano(arbol, matriz, visited, parent):
    queue = deque([list(arbol.keys())[0]])  # Comenzamos desde la raíz del árbol
    while queue: # Mientras la cola no esté vacía
        nodo_actual = queue.popleft() # Sacar el primer elemento de la cola
        if tiene_hijos_no_explorados(nodo_actual, arbol, matriz, visited):
            return nodo_actual # Devolver el nodo actual
        for hijo in arbol.get(nodo_actual, []): # Recorrer los hijos del nodo actual
            queue.append(hijo) # Agregar el hijo a la cola
    return None # Si no se encontró ningún nodo no explorado


def obtener_nivel_nodo(nodo, parent): # Función para obtener el nivel de un nodo en el árbol
    nivel = 0
    while nodo in parent: # Mientras el nodo tenga un padre
        nodo = parent[nodo] # Moverse al padre
        nivel += 1
    return nivel

#busquedad_por_amplitud-----------------------------------------------------------------------
def busquedad_por_amplitud(matriz, nodo_inicial, posicion_queso, arbol, 
                           actualizar_arbol_callback, actualizar_estrategia_callback, 
                           nodos_expandir, visited, parent):
    actualizar_estrategia_callback(f"Busqueda amplitud")
    filas, columnas = len(matriz), len(matriz[0]) # Obtener las dimensiones de la matriz
    graph = nx.grid_2d_graph(filas, columnas) # Crear un grafo 2D

    # Remover obstáculos del grafo
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    # Revisar si hay nodos anteriores con hijos no explorados
    nodo_inicial = obtener_nodo_no_explorado_mas_cercano(arbol, matriz, visited, parent) or nodo_inicial

    # Inicializar la cola con el nodo inicial más adecuado
    queue = deque([(nodo_inicial, 0)])
    ruta_actual = []
    nivel_actual = 0

    while queue:
        current_node, nivel_actual = queue.popleft() # Sacar el primer elemento de la cola

        if nivel_actual >= nodos_expandir: # Si se ha alcanzado el límite de nodos a expandir
            break

        if current_node not in visited: # Si el nodo actual no ha sido visitado
            visited.add(current_node) # Marcar el nodo como visitado
            ruta_actual.append(current_node) # Agregar el nodo a la ruta actual

            # Verificar si hemos encontrado el queso
            if current_node == posicion_queso: # Si el nodo actual es el queso
                path = [] # Inicializar el camino
                while current_node is not None: # Mientras el nodo actual no sea nulo
                    path.append(current_node) # Agregar el nodo al camino
                    current_node = parent.get(current_node) # Moverse al padre del nodo actual
                path = path[::-1] # Invertir el camino
                img = dibujar_arbol(arbol, None, path=path) # Dibujar el árbol con el camino
                actualizar_arbol_callback(img) # Actualizar la imagen del árbol
                return path, visited, parent # Devolver el camino, los nodos visitados y los padres

            # Obtener vecinos no explorados
            vecinos_posibles = list(graph.neighbors(current_node)) # Obtener los vecinos del nodo actual
            vecinos_posibles.sort(key=lambda x: (x[0], x[1])) # Ordenar los vecinos

            for neighbor in vecinos_posibles: # Recorrer los vecinos
                if neighbor not in visited: # Si el vecino no ha sido visitado
                    # Agregar al árbol si es necesario
                    if current_node in arbol: # Si el nodo actual está en el árbol
                        if neighbor not in arbol[current_node]: # Si el vecino no está en los hijos del nodo actual
                            arbol[current_node].append(neighbor) # Agregar el vecino a los hijos del nodo actual
                    else:
                        arbol[current_node] = [neighbor] # Crear una lista de hijos para el nodo actual
                    
                    # Agregar a la cola
                    queue.append((neighbor, nivel_actual + 1))
                    parent[neighbor] = current_node

                    # Visualización del árbol
                    img = dibujar_arbol(arbol, neighbor)
                    actualizar_arbol_callback(img)
                    time.sleep(0.5)
       
        # Antes de continuar al siguiente nivel, verificar si hay nodos no explorados en niveles superiores
        nodo_superior = obtener_nodo_no_explorado_mas_cercano(arbol, matriz, visited, parent)
        if nodo_superior and nodo_superior != current_node: # Si hay un nodo superior no explorado
            queue.append((nodo_superior, obtener_nivel_nodo(nodo_superior, parent))) # Agregar el nodo superior a la cola

    return ruta_actual, visited, parent


# Busqueda preferente por profundidad --------------------------------------------------------------------------------------

def busqueda_preferente_por_profundidad(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    actualizar_estrategia_callback(f"Busqueda preferente profundidad")
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    # Stack ahora almacena tuplas de (nodo, nivel)
    stack = [(nodo_inicial, 1)]  # Comenzamos en nivel 1
    visited_levels = {}  # Diccionario para rastrear el nivel de cada nodo visitado
    visited_levels[nodo_inicial] = 1

    while stack and len(visited) < nodos_expandir:
        current_node, current_level = stack.pop()

        if current_level > nodos_expandir:
            continue

        if current_node not in visited:
            visited.add(current_node)

            if current_node == posicion_queso:
                path = []
                node = current_node
                while node is not None:
                    path.append(node)
                    node = parent.get(node)
                img = dibujar_arbol(arbol, None, path=path[::-1])
                actualizar_arbol_callback(img)
                return path[::-1], visited, parent

            if current_node not in arbol:
                arbol[current_node] = []

            # Obtener las coordenadas del nodo actual
            i, j = current_node
            
            # Definir los vecinos en el orden: arriba, derecha, abajo, izquierda
            vecinos_ordenados = [
                (i-1, j),  # arriba
                (i, j+1),  # derecha
                (i+1, j),  # abajo
                (i, j-1)   # izquierda
            ]
            
            # Filtrar vecinos válidos
            vecinos = [v for v in vecinos_ordenados if v in graph.nodes()]

            # Procesar vecinos en orden inverso
            for neighbor in reversed(vecinos):
                if neighbor not in visited:
                    new_level = current_level + 1
                    if new_level <= nodos_expandir:  # Solo agregamos si no excede el nivel máximo
                        stack.append((neighbor, new_level))
                        visited_levels[neighbor] = new_level
                        parent[neighbor] = current_node
                        arbol[current_node].insert(0, neighbor)

                        img = dibujar_arbol(arbol, current_node)
                        actualizar_arbol_callback(img)
                        time.sleep(0.5)

    # Si no se encuentra el queso, devolver el camino explorado
    path = [nodo for nodo, _ in stack]
    return [nodo_inicial] + path, visited, parent


# Busquedad por profundización iterativa --------------------------------------------------------------------------------------------

def buquedad_profundidad_iteractiva(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visitados=None, padre=None):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    # Eliminar nodos que son obstáculos
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    queue = deque([nodo_inicial])
    count = 1
    max_profundidad = 0

    while queue and count < nodos_expandir:
        current_node = queue.popleft()
        
    if visitados is None:
        visitados = set()
    if padre is None:
        padre = {nodo_inicial: None}

    while max_profundidad <= nodos_expandir:
        arbol = {nodo_inicial: []}
        visitados = set()
        queue = deque([(nodo_inicial, 0)])

        while queue:
            nodo_actual, profundidad_actual = queue.popleft()

            if nodo_actual == posicion_queso:
                path = []
                while nodo_actual is not None:
                    path.append(nodo_actual)
                    nodo_actual = padre[nodo_actual]
                path.reverse()
                img = dibujar_arbol(arbol, None, path=path)
                actualizar_arbol_callback(img)
                return path, visitados, padre
        

            if profundidad_actual >= max_profundidad:
                # Si la profundidad actual es mayor a la máxima, terminar la iteración
                
                break

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)

                # Actualizar el árbol con el nodo actual
                if nodo_actual not in arbol:
                    arbol[nodo_actual] = []
                # Obtener los vecinos del nodo actual
                vecinos = list(graph.neighbors(nodo_actual))
                for vecino in vecinos:
                    if vecino not in visitados:
                        queue.append((vecino, profundidad_actual + 1))
                        padre[vecino] = nodo_actual
                        arbol[nodo_actual].append(vecino)
                # Dibuja el árbol en la profundidad actual
                img = dibujar_arbol(arbol, nodo_actual)
                actualizar_arbol_callback(img)
                time.sleep(0.5)
        max_profundidad += 1
        print(f"Profundidad actual: {max_profundidad}")

    print("No se encontró un camino hasta el queso en la profundidad máxima permitida.")
    return [nodo_inicial], visitados, padre

    
    

# Busqueda por costo uniforme --------------------------------------------------------------------------------------
def busqueda_por_costo_uniforme(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    actualizar_estrategia_callback(f"Busqueda costo uniforme")
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    # Eliminar nodos que son obstáculos en la matriz
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:  # Suponemos que 1 es un obstáculo
                graph.remove_node((i, j))

    # Usamos un min-heap para almacenar los nodos con sus costos
    queue = []
    heapq.heappush(queue, (0, nodo_inicial, 0))  # (costo, nodo, profundidad)
    costs = {nodo_inicial: 0}
    profundidades = {nodo_inicial: 0}

    # Bandera para verificar si el queso ya fue visitado o está en los nodos explorados
    queso_encontrado = False
    nodo_queso_encontrado = None

    while queue:
        current_cost, current_node, current_depth = heapq.heappop(queue)

        # Verificar si el queso ya ha sido encontrado en una iteración anterior
        if queso_encontrado:
            break

        # Verificar la profundidad máxima
        if current_depth > nodos_expandir:
            print(f"Profundidad máxima ({nodos_expandir}) alcanzada en el nodo {current_node}")
            break

        if current_node in visited:
            print(f"El nodo {current_node} ya fue visitado, continuando con el siguiente.")
            continue

        print(f"Procesando nodo: {current_node} con costo acumulado: {current_cost}, profundidad: {current_depth}")

        visited.add(current_node)

        # Verificar si el nodo actual es el queso o si el queso ya ha sido visitado
        if current_node == posicion_queso or posicion_queso in visited:
            print("Se ha encontrado el queso en el nodo:", current_node)
            queso_encontrado = True
            nodo_queso_encontrado = current_node
            break

        if current_node not in arbol:
            arbol[current_node] = []

        # Obtener las coordenadas del nodo actual
        i, j = current_node
        
        # Definir los vecinos en orden horario: arriba, derecha, abajo, izquierda
        vecinos_ordenados = [
            (i-1, j),  # arriba
            (i, j+1),  # derecha
            (i+1, j),  # abajo
            (i, j-1)   # izquierda
        ]
        
        # Filtrar solo los vecinos válidos que existen en el grafo
        vecinos = [v for v in vecinos_ordenados if v in graph.nodes()]

        # Procesar vecinos en orden inverso para mantener la visualización correcta
        for neighbor in reversed(vecinos):
            if neighbor not in visited:
                # Calcular el nuevo costo
                new_cost = current_cost + 1
                
                # Añadir costo adicional si la celda es tipo 4
                if matriz[neighbor[0]][neighbor[1]] == 4:
                    new_cost += 3 

                if neighbor not in costs or new_cost < costs[neighbor]:
                    print(f"Actualizando vecino {neighbor}, nuevo costo: {new_cost}, padre: {current_node}")
                    costs[neighbor] = new_cost
                    parent[neighbor] = current_node
                    
                    # Insertar al principio de la lista para mantener el orden visual
                    arbol[current_node].insert(0, neighbor)
                    heapq.heappush(queue, (new_cost, neighbor, current_depth + 1))

                    img = dibujar_arbol(arbol, current_node)
                    actualizar_arbol_callback(img)
                    time.sleep(0.5)

            else:
                print(f"Vecino {neighbor} ya visitado, saltando.")
    
    # Si se encontró el queso, devolver el camino hasta él
    if queso_encontrado:
        path = []
        current_node = nodo_queso_encontrado
        while current_node is not None:
            path.append(current_node)
            current_node = parent.get(current_node)
            img = dibujar_arbol(arbol, None, path=path[::-1])
            actualizar_arbol_callback(img)
        return path[::-1], visited, parent # Devolver el camino, los nodos visitados y los padres
    
    # Si no se encuentra el queso, devolver el nodo inicial
    return [nodo_inicial], visited, parent

# Busqueda limitada por profundidad --------------------------------------------------------------------------------------

def busqueda_limitada_por_profundidad(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    actualizar_estrategia_callback(f"Busqueda limitada por profundidad")
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    stack = [(nodo_inicial, 0)]  # Agregamos la profundidad al nodo (nodo, profundidad)
    ultimo_nodo_expandido = nodo_inicial  # Guardamos el último nodo expandido

    while stack:
        current_node, depth = stack.pop()

        # Si hemos llegado a la profundidad máxima, terminamos la expansión
        if depth >= nodos_expandir:
            
            break

        if current_node not in visited:
            visited.add(current_node)
            ultimo_nodo_expandido = current_node  # Actualizamos el último nodo expandido

            if current_node == posicion_queso:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                img = dibujar_arbol(arbol, None, path=path[::-1])
                actualizar_arbol_callback(img)
                return path[::-1], visited, parent

            if current_node not in arbol:
                arbol[current_node] = []

            # Obtener las coordenadas del nodo actual
            i, j = current_node
            
            # Definir los vecinos en el orden: arriba, derecha, abajo, izquierda
            vecinos_ordenados = [
                (i-1, j),  # arriba
                (i, j+1),  # derecha
                (i+1, j),  # abajo
                (i, j-1)   # izquierda
            ]
            
            # Filtrar solo los vecinos válidos que existen en el grafo
            vecinos = [v for v in vecinos_ordenados if v in graph.nodes()]

            # Al agregar los vecinos al árbol, los agregamos en orden inverso
            for neighbor in reversed(vecinos):
                if neighbor not in visited:
                    stack.append((neighbor, depth + 1))
                    parent[neighbor] = current_node
                    arbol[current_node].insert(0, neighbor)

                    img = dibujar_arbol(arbol, current_node)
                    actualizar_arbol_callback(img)
                    time.sleep(0.5)
                    

    # Devolver solo el último nodo expandido
    return [ultimo_nodo_expandido], visited, parent

# Busqueda Avara --------------------------------------------------------------------------------------
def heuristica(posicion_actual, posicion_queso):
    # Calcula la distancia de Manhattan entre el nodo actual y el queso
    return abs(posicion_actual[0] - posicion_queso[0]) + abs(posicion_actual[1] - posicion_queso[1])

def busqueda_avara(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    actualizar_estrategia_callback(f"Busqueda Avara")
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))
    # Usamos una priority queue (heapq) para almacenar nodos ordenados por su valor heurístico
    queue = []
    heapq.heappush(queue, (heuristica(nodo_inicial, posicion_queso), nodo_inicial))  # (heurística, nodo)
    count = 1

    while queue and count < nodos_expandir:
        _, current_node = heapq.heappop(queue) # aqui considera el camino con la menor heuristica

        # Si el nodo ya ha sido visitado, lo saltamos
        if current_node in visited:
            continue

        # Marcamos el nodo como visitado
        visited.add(current_node)

        # Verificamos si hemos llegado al queso
        if current_node == posicion_queso:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent.get(current_node)
            img = dibujar_arbol(arbol, None, path=path[::-1])
            actualizar_arbol_callback(img)
            return path[::-1], visited, parent

        # Si el nodo actual no está en el árbol, lo inicializamos
        if current_node not in arbol:
            arbol[current_node] = []

        # Obtener los vecinos del nodo actual
        vecinos = list(graph.neighbors(current_node))

        for neighbor in vecinos:
            if neighbor not in visited:
                parent[neighbor] = current_node
                arbol[current_node].append(neighbor)

                # Calcular heurística y añadir al heap
                heur_value = heuristica(neighbor, posicion_queso)  # Distancia Manhattan sin costo adicional
                heapq.heappush(queue, (heur_value, neighbor))

                # Dibujar el árbol con el nodo actual y los vecinos
                img = dibujar_arbol(arbol, current_node)
                actualizar_arbol_callback(img)
                time.sleep(0.5)

                # Contador para limitar el número de nodos expandidos
                count += 1
                if count == nodos_expandir:
                        nodo_inicial = neighbor
                      
                        break

    return [nodo_inicial], visited, parent

# Buscar ruta --------------------------------------------------------------------------------------
def buscar_ruta(
    matriz, posicion_raton, posicion_queso,
    actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir
):
    estrategias = [busquedad_por_amplitud,
                   busqueda_por_costo_uniforme,
                   busqueda_avara,
                   busqueda_limitada_por_profundidad,
                   busqueda_preferente_por_profundidad]  # Lista de estrategias
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    path = []  # Cambié para no inicializar con el nodo inicial
    visited = set()
    parent = {nodo_actual: None}  # Mapa de padres global para todas las estrategias

    while nodo_actual != posicion_queso:
        if not estrategias:
            print("No quedan estrategias por seleccionar.")
            break

        # Seleccionar la estrategia
        estrategia = random.choice(estrategias)
        estrategias.remove(estrategia)
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)
        print(f"Estrategia actual: {nombre_estrategia}")
        print(f"Nodo actual antes de la estrategia: {nodo_actual}")

        # Ejecutar la estrategia
        resultado, visited, parent = estrategia(
            matriz, nodo_actual, posicion_queso,
            arbol, actualizar_arbol_callback, actualizar_estrategia_callback,
            nodos_expandir, visited, parent
        )

        if resultado:
            print(f"Resultado de la estrategia {nombre_estrategia}: {resultado}")
            
            # Si se encuentra una ruta válida, verificar si el queso está en el resultado
            if resultado and resultado[-1] == posicion_queso:
                return resultado

            
            else:
                # Obtener el nodo no explorado o usar el último nodo expandido
                nuevo_nodo = obtener_nodo_no_explorado(arbol, visited)
                nodo_actual = nuevo_nodo if nuevo_nodo else resultado[-1]
                if nodo_actual not in visited:  # Evitar agregar nodos ya visitados
                    path.append(nodo_actual)
                print(f"Nuevo nodo actual: {nodo_actual}")
        else:
            print("No se pudo encontrar una ruta con la estrategia actual. Continuando con la siguiente.")
            nuevo_nodo = obtener_nodo_no_explorado(arbol, visited)
            nodo_actual = nuevo_nodo if nuevo_nodo else nodo_actual

        print(f"Nodo actual después de la estrategia: {nodo_actual}")
        print(f"Nodos visitados hasta ahora: {visited}")

    return None

if __name__ == "__main__":
    matriz, posicion_raton, posicion_queso, ratoneras = cargar_matriz("laberinto.txt")

    if posicion_raton is None or posicion_queso is None:
        print("Error: No se encontró la posición del ratón o del queso.")
    else:
        nodos_expandir = 4# Este valor puede ser configurado desde la interfaz pongo 6 por pruebas aqui sin interface
        ruta = buscar_ruta(matriz, posicion_raton, posicion_queso, lambda x: None, lambda x: None, nodos_expandir)

        if ruta:
            print("Ruta encontrada:", ruta)
        else:
            print("No se encontró una ruta al queso.")
