#Aqui se implementan las funciones de busqueda de caminos para hacerlas individuales

from estrategias import *

def buscar_amplitud(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    visited = set()
    parent = {nodo_actual: None}
    estrategia = busquedad_por_amplitud  

    while nodo_actual != posicion_queso:
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)

        # Ejecutar la estrategia seleccionada
        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)

        if resultado:
            if resultado[-1] == posicion_queso:
                return resultado
            nodo_actual = resultado[-1]
        else:
            break  # Salir si no hay más resultados

    return None


def costo_uniforme(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    visited = set()
    parent = {nodo_actual: None}
    estrategia = busqueda_por_costo_uniforme  

    while nodo_actual != posicion_queso:
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)

        # Ejecutar la estrategia seleccionada
        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)

        if resultado:
            if resultado[-1] == posicion_queso:
                return resultado
            nodo_actual = resultado[-1]
        else:
            break  # Salir si no hay más resultados

    return None

def iterativa(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    visited = set()
    parent = {nodo_actual: None}
    estrategia = buquedad_profundidad_iteractiva  

    while nodo_actual != posicion_queso:
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)

        # Ejecutar la estrategia seleccionada
        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)

        if resultado:
            if resultado[-1] == posicion_queso:
                return resultado
            nodo_actual = resultado[-1]
        else:
            break  # Salir si no hay más resultados

    return None

def preferente_profundidad(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    visited = set()
    parent = {nodo_actual: None}
    estrategia = busqueda_preferente_por_profundidad  

    while nodo_actual != posicion_queso:
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)

        # Ejecutar la estrategia seleccionada
        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)

        if resultado:
            if resultado[-1] == posicion_queso:
                return resultado
            nodo_actual = resultado[-1]
        else:
            break  # Salir si no hay más resultados

    return None

def limitada_por_profundidad(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    visited = set()
    parent = {nodo_actual: None}
    estrategia = busqueda_limitada_por_profundidad  

    while nodo_actual != posicion_queso:
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)

        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)

        if resultado:
            if resultado[-1] == posicion_queso:
                return resultado
            nodo_actual = resultado[-1]
        else:
            break  # Salir si no hay más resultados

    return None

def Avara(matriz, posicion_raton, posicion_queso, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir):
    arbol = {posicion_raton: []}
    nodo_actual = posicion_raton
    visited = set()
    parent = {nodo_actual: None}
    estrategia = busqueda_avara  

    while nodo_actual != posicion_queso:
        nombre_estrategia = estrategia.__name__.capitalize()
        actualizar_estrategia_callback(nombre_estrategia)

        # Ejecutar la estrategia seleccionada
        resultado, visited, parent = estrategia(matriz, nodo_actual, posicion_queso, arbol, actualizar_arbol_callback, actualizar_estrategia_callback, nodos_expandir, visited, parent)

        if resultado:
            if resultado[-1] == posicion_queso:
                return resultado
            nodo_actual = resultado[-1]
        else:
            break  # Salir si no hay más resultados

    return None
