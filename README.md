
## Integrantes
*Alejandro Marin Hoyos - 2259353-3743*
*Karen Jhulieth Grijalba Ortiz - 2259623-3743*
*Yessica Fernanda Villa Nuñez - 2266301-3743*
*Manuel Antonio Vidales Duran - 2155481-3743*
*Jersson Gutierrez Gonzalez 2060071-3743*

---
# ArbolesLocos
El proyecto "Árboles locos" consiste en desarrollar un programa en Python que permita a un ratón encontrar el queso usando técnicas de búsqueda no informadas y busqueda avara. El ratón inicia su recorrido en un tablero y debe tomar decisiones sobre qué camino seguir, aplicando distintas estrategias de búsqueda seleccionadas aleatoriamente para llegar al objetivo. Se implementarán cinco estrategias no informadas, además de una estrategia informada (Avara). El programa debe alternar entre estas estrategias durante la ejecución, y en cada ciclo de expansiones se cambiará la estrategia según el número de expansiones configurado.

---
## Creacion del Ambiente 
```python
python3 -m venv myenv
source myenv/bin/activate
```
---

## Estructura del proyecto
```
└── 📁ProyectoArbolesLocos
    └── .gitignore
    └── arbol_actual.png
    └── arbol.png
    └── busquedas.py
    └── estrategias.py
    └── InterfazLaberinto.py
    └── laberinto.txt
    └── Proyecto.pdf
    └── queso.png
    └── raton.png
    └── ratonera.png
    └── README.md
    └── representacion.txt
```
---
## Instalaciones

Se describen las bibliotecas utilizadas, sus funciones y los comandos necesarios para su instalación.

## Bibliotecas Utilizadas

1. **NetworkX**: 
   - **Descripción**: Una biblioteca para la creación, manipulación y estudio de la estructura, dinámica y funciones de complejas redes de grafos.
   - **Comando de Instalación**:
     ```bash
     pip install networkx
     ```

2. **Matplotlib**: 
   - **Descripción**: Una biblioteca de gráficos 2D para Python que se utiliza para crear gráficos a partir de datos.
   - **Comando de Instalación**:
     ```bash
     pip install matplotlib
     ```

3. **PyGraphviz**: 
   - **Descripción**: Un contenedor de Python para Graphviz, que permite crear y renderizar grafos utilizando el lenguaje DOT.
   - **Comando de Instalación**:
     ```bash
     pip install pygraphviz
     ```
   - **Requisito**: Es necesario tener Graphviz instalado en tu sistema. Puedes instalar Graphviz utilizando uno de los siguientes comandos según tu sistema operativo:
     - **En Ubuntu/Debian**:
       ```bash
       sudo apt-get install graphviz
       ```
     - **En macOS**:
       ```bash
       brew install graphviz
       ```

4. **Pillow (PIL)**: 
   - **Descripción**: Una biblioteca para abrir, manipular y guardar muchos formatos de archivo de imagen diferentes.
   - **Comando de Instalación**:
     ```bash
     pip install pillow
     ```

5. **Tkinter**: 
   - **Descripción**: La biblioteca estándar de Python para la creación de interfaces gráficas de usuario (GUI). No requiere instalación adicional si ya tienes Python instalado.
   - **Comando de Instalación**: No se requiere, ya que Tkinter viene incluido con la mayoría de las instalaciones de Python.

## Ejecutar programa

Para ejecutar el archivo `interfaz.py`, abre la terminal y escribe el siguiente comando:

```bash
python3 interfazLaberinto.py

# IA
