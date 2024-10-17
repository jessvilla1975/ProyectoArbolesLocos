import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import pygraphviz as pgv
from io import BytesIO
from PIL import Image, ImageTk
import time
import random
import heapq

def cargar_matriz(archivo):
    with open(archivo, 'r') as f:
        matriz = [list(map(int, line.strip().split())) for line in f]

    posicion_raton = None
    posicion_queso = None

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 2:
                posicion_raton = (i, j)
            elif matriz[i][j] == 3:
                posicion_queso = (i, j)

    return matriz, posicion_raton, posicion_queso

def dibujar_arbol(arbol, nodo_actual, path=[]):
    G = pgv.AGraph(strict=False, directed=True)

    for nodo in arbol:
        if arbol[nodo]:
            for hijo in arbol[nodo]:
                G.add_edge(str(nodo), str(hijo))

    for nodo in G.nodes():
        G.get_node(nodo).attr['label'] = nodo
        G.get_node(nodo).attr['shape'] = 'ellipse'

        if str(nodo) in [str(p) for p in path]:
            G.get_node(nodo).attr['color'] = 'green'
        elif str(nodo) == str(nodo_actual):
            G.get_node(nodo).attr['color'] = 'red'
        else:
            G.get_node(nodo).attr['color'] = 'lightblue'

    G.layout(prog='dot')

    buf = BytesIO()
    G.draw(buf, format='png')
    buf.seek(0)

    return Image.open(buf)

# Busqueda por amplitud --------------------------------------------------------------------------------------------------------------

def amplitud(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    queue = deque([nodo_inicial])
    count = 1

    while queue and count < nodos_expandir:
        current_node = queue.popleft()
        
        if current_node not in visited:
            visited.add(current_node)

            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    parent[neighbor] = current_node  # Actualizamos el parent
                    if current_node in arbol:
                        arbol[current_node].append(neighbor)
                    else:
                        arbol[current_node] = [neighbor]

                    img = dibujar_arbol(arbol, neighbor)
                    actualizar_arbol_callback(img)
                    time.sleep(0.5)

            count += 1

            if current_node == posicion_queso:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                img = dibujar_arbol(arbol, None, path=path[::-1])
                actualizar_arbol_callback(img)
                return path[::-1], visited, parent  # Devolvemos `parent` actualizado

    return [nodo_inicial] + list(queue), visited, parent


#estrategia falsa ------------------------------------------------------------------------------------------------
def estrategiafalsa(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    queue = deque([nodo_inicial])
    count = 1

    while queue and count < nodos_expandir:
        current_node = queue.popleft()
        
        if current_node not in visited:
            visited.add(current_node)

            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    parent[neighbor] = current_node  # Actualizamos el parent
                    if current_node in arbol:
                        arbol[current_node].append(neighbor)
                    else:
                        arbol[current_node] = [neighbor]

                    img = dibujar_arbol(arbol, neighbor)
                    actualizar_arbol_callback(img)
                    time.sleep(0.5)

            count += 1

            if current_node == posicion_queso:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                img = dibujar_arbol(arbol, None, path=path[::-1])
                actualizar_arbol_callback(img)
                return path[::-1], visited, parent  # Devolvemos `parent` actualizado

    return [nodo_inicial] + list(queue), visited, parent

# Busquedad por profundización iterativa --------------------------------------------------------------------------------------------
# Aqui cae en bucle infinito 
def Profundidad_Iteractiva(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited=None, parent=None):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    # Eliminar nodos que son obstáculos
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    max_profundidad = 0
    count = 0  # Contador de nodos expandidos

    if visited is None:
        visited = set()
    if parent is None:
        parent = {nodo_inicial: None}

    # Ciclo principal que incrementa la profundidad máxima permitida
    while max_profundidad <= nodos_expandir and count < nodos_expandir:
        # Reiniciar el árbol y la lista de visitados en cada iteración
        arbol = {nodo_inicial: []}
        local_visited = set()
        queue = deque([(nodo_inicial, 0)])  # Cola con nodo inicial y su profundidad

        print(f"Iniciando búsqueda con profundidad límite: {max_profundidad}")

        # Búsqueda en profundidad limitada a `max_profundidad`
        while queue and count < nodos_expandir:
            current_node, profundidad_actual = queue.popleft()

            if current_node == posicion_queso:
                # Si se encuentra el queso, reconstruir el camino
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                path.reverse()

                # Dibujar el árbol final con el camino al queso
                img = dibujar_arbol(arbol, None, path=path)
                actualizar_arbol_callback(img)
                return path, visited, parent

            if current_node not in local_visited:
                local_visited.add(current_node)
                visited.add(current_node)  # Agregar a los visitados globales

                # Actualizar el árbol con el nodo actual
                if current_node not in arbol:
                    arbol[current_node] = []

                # Obtener los vecinos del nodo actual
                vecinos = list(graph.neighbors(current_node))

                for neighbor in vecinos:
                    if neighbor not in local_visited:
                        if profundidad_actual < max_profundidad:
                            queue.append((neighbor, profundidad_actual + 1))
                            parent[neighbor] = current_node
                            arbol[current_node].append(neighbor)

                            # Dibuja el árbol en la profundidad actual
                            img = dibujar_arbol(arbol, current_node)
                            actualizar_arbol_callback(img)
                            time.sleep(0.5)

                            count += 1  # Incrementar el contador de nodos expandidos
                            if count >= nodos_expandir:
                                break

        max_profundidad += 1  # Incrementar la profundidad permitida
        print(f"Profundidad actual incrementada a: {max_profundidad}")

    print("No se encontró un camino hasta el queso en la cantidad máxima de nodos permitida.")
    return None, visited, parent





def buscar_ruta(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    estrategias = [Profundidad_Iteractiva]  # Lista de estrategias
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    path = [nodo_actual]
    visited = set()
    parent = {nodo_actual: None}  # Mapa de padres global para todas las estrategias

    while nodo_actual != posicion_queso:
        if not estrategias:
            print("No quedan estrategias por seleccionar.")
            break

        estrategia = random.choice(estrategias)  # Selecciona una estrategia al azar
        estrategias.remove(estrategia)
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)
        print(f"Estrategia actual: {nombre_estrategia}")
        
        # Pasamos `parent` para que las estrategias mantengan el árbol de padres correctamente
        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)
        
        if resultado:
            if resultado[-1] == posicion_queso:
                path.extend(resultado[1:])  # Agregar todos los nodos visitados a la ruta
                return path
            else:
                path.append(resultado[-1])  # Agregar solo el último nodo visitado
                nodo_actual = resultado[-1]  # Actualizar el nodo actual para la próxima iteración
        else:
            continue

    return None


if __name__ == "__main__":
    matriz, posicion_raton, posicion_queso = cargar_matriz("laberinto.txt")

    if posicion_raton is None or posicion_queso is None:
        print("Error: No se encontró la posición del ratón o del queso.")
    else:
        nodos_expandir = 6# Este valor puede ser configurado desde la interfaz pongo 6 por pruebas aqui sin interface
        ruta = buscar_ruta(matriz, posicion_raton, posicion_queso, lambda x: None, lambda x: None, nodos_expandir)

        if ruta:
            print("Ruta encontrada:", ruta)
        else:
            print("No se encontró una ruta al queso.")

# Busqueda por costo uniforme --------------------------------------------------------------------------------------

def busqueda_por_costo_uniforme(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:  # 1 representa un obstáculo en la matriz
                graph.remove_node((i, j))

    queue = []
    heapq.heappush(queue, (0, nodo_inicial))  # (costo_acumulado, nodo)
    costs = {nodo_inicial: 0}
    parent[nodo_inicial] = None

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_node == posicion_queso:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            path.reverse()
            return path, visited, parent

        visited.add(current_node)

        # Expandir nodos vecinos
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                new_cost = current_cost + 1  # Asignamos un costo uniforme de 1 a cada movimiento
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    parent[neighbor] = current_node
                    heapq.heappush(queue, (new_cost, neighbor))
        
        arbol[current_node] = list(graph.neighbors(current_node))  # Actualizar el árbol con los vecinos
        actualizar_arbol_callback(arbol)  # Llamada de actualización visual

    return None, visited, parent