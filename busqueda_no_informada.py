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

def amplitud(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, padre):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    queue = deque([nodo_inicial])
    count = 1

    while queue and count < nodos_expandir:
        nodo_actual = queue.popleft()
        
        if nodo_actual not in visited:
            visited.add(nodo_actual)

            for vecino in graph.neighbors(nodo_actual):
                if vecino not in visited and vecino not in queue:
                    queue.append(vecino)
                    padre[vecino] = nodo_actual  # Actualizamos el parent
                    if nodo_actual in arbol:
                        arbol[nodo_actual].append(vecino)
                    else:
                        arbol[nodo_actual] = [vecino]

                    img = dibujar_arbol(arbol, vecino)
                    actualizar_arbol_callback(img)
                    time.sleep(0.5)

            count += 1

            if nodo_actual == posicion_queso:
                path = []
                while nodo_actual is not None:
                    path.append(nodo_actual)
                    nodo_actual = padre[nodo_actual]
                img = dibujar_arbol(arbol, None, path=path[::-1])
                actualizar_arbol_callback(img)
                return path[::-1], visited, padre  # Devolvemos `parent` actualizado

    return None, visited, padre


# Busquedad por profundización iterativa --------------------------------------------------------------------------------------------
# Aqui para poder poner un limite, uso nodos a expandir para que se expanda hasta esa profundidad
# falta corregir para que tome de nodo padre el ultimo nodo visitado de la anterior estrategia si hay una antes de esta estrategia
def Profundidad_Iteractiva(matriz, nodo_inicial, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visitados=None, padre=None):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    # Eliminar nodos que son obstáculos
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    max_profundidad = 0

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

            if profundidad_actual > max_profundidad:
                continue

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
    return None, visitados, padre


def buscar_ruta(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    estrategias = [amplitud, Profundidad_Iteractiva]  # Lista de estrategias 

    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    path = [nodo_actual]
    visited = set()
    padre = {nodo_actual: None}  # Mapa de padres global para todas las estrategias

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
        resultado, visited, padre = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, padre)

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
