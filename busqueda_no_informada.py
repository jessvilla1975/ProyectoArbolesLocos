import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import pygraphviz as pgv
from io import BytesIO


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


def dibujar_arbol(arbol, nodo_actual, ax, path=[]):
    G = pgv.AGraph(strict=False, directed=True)

    for nodo in arbol:
        if arbol[nodo]:
            for hijo in arbol[nodo]:
                G.add_edge(nodo, hijo)

    for nodo in G.nodes():
        G.get_node(nodo).attr['label'] = nodo
        G.get_node(nodo).attr['shape'] = 'ellipse'

        # Si el nodo está en el camino encontrado, pintarlo de verde
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

    ax.clear()
    ax.imshow(plt.imread(buf))
    ax.axis('off')
    plt.draw()
    plt.pause(0.5)


def amplitud(matriz, posicion_raton, posicion_queso, arbol, ax, nodos_expandir):
    filas, columnas = len(matriz), len(matriz[0])
    graph = nx.grid_2d_graph(filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 1:
                graph.remove_node((i, j))

    queue = deque([posicion_raton])
    visited = set()
    parent = {posicion_raton: None}
    count = 0

    while queue:
        current_node = queue.popleft()
        visited.add(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                parent[neighbor] = current_node
                if current_node in arbol:
                    arbol[current_node].append(neighbor)
                else:
                    arbol[current_node] = [neighbor]

        count += 1

        # Dibuja el árbol hasta el nodo actual
        dibujar_arbol(arbol, current_node, ax)

        # Verifica si se ha alcanzado el queso
        if current_node == posicion_queso:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]

            # Dibuja el camino en verde
            dibujar_arbol(arbol, None, ax, path=path[::-1])
            return path[::-1]

        # Detener la expansión si se ha alcanzado el número máximo de nodos a expandir
        if count >= nodos_expandir:
            print(f"Se han expandido {nodos_expandir} nodos. Deteniendo la búsqueda.")
            return None

    return None


def buscar_ruta(matriz, posicion_raton, posicion_queso, nodos_expandir):
    estrategias = [amplitud]  # Agregar las funciones de búsqueda aquí
    arbol = {posicion_raton: []}
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.ion()

    for estrategia in estrategias:
        print(f"Estrategia actual: {estrategia.__name__}")
        path = estrategia(matriz, posicion_raton, posicion_queso, arbol, ax, nodos_expandir)

        if path:
            plt.ioff()
            plt.show()
            return path

    plt.ioff()
    plt.show()
    return None


if __name__ == "__main__":
    matriz, posicion_raton, posicion_queso = cargar_matriz("laberinto.txt")

    if posicion_raton is None or posicion_queso is None:
        print("Error: No se encontró la posición del ratón o del queso.")
    else:
        nodos_expandir = 2  # Este valor puede ser configurado desde la interfaz
        ruta = buscar_ruta(matriz, posicion_raton, posicion_queso, nodos_expandir)

        if ruta:
            print("Ruta encontrada:", ruta)
        else:
            print("No se encontró un camino.")