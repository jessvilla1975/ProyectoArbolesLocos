import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import pygraphviz as pgv
from io import BytesIO
from PIL import Image, ImageTk
import time
import random

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
                G.add_edge(nodo, hijo)

    for nodo in G.nodes():
        G.get_node(nodo).attr['label'] = nodo
        G.get_node(nodo).attr['shape'] = 'ellipse'

        if nodo in path:
            G.get_node(nodo).attr['color'] = 'green'
        elif nodo == nodo_actual:
            G.get_node(nodo).attr['color'] = 'red'
        else:
            G.get_node(nodo).attr['color'] = 'lightblue'

    G.layout(prog='dot')

    buf = BytesIO()
    G.draw(buf, format='png')
    buf.seek(0)

    return Image.open(buf)

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


def estrategia2(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent):
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



def buscar_ruta(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    estrategias = [amplitud, estrategia2]  # Lista de estrategias
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
        nodos_expandir = 2  # Este valor puede ser configurado desde la interfaz
        ruta = buscar_ruta(matriz, posicion_raton, posicion_queso, lambda x: None, lambda x: None, nodos_expandir)

        if ruta:
            print("Ruta encontrada:", ruta)
        else:
            print("No se encontró un camino.")