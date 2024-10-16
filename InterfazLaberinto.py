import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from busqueda_no_informada import buscar_ruta
import time

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración del Laberinto")
        self.root.geometry("1400x800")

        # Frame principal que contiene todo
        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Frame izquierdo para el canvas del árbol
        self.frame_izquierdo = tk.Frame(self.frame_principal, width=600)
        self.frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Label para mostrar la estrategia actual
        self.label_estrategia = tk.Label(self.frame_izquierdo, text="Estrategia: ", font=("Arial", 14))
        self.label_estrategia.pack(pady=10)

        # Canvas para el árbol de búsqueda
        self.canvas_arbol = tk.Canvas(self.frame_izquierdo, width=600, height=670)
        self.canvas_arbol.pack(fill=tk.BOTH, expand=True)

        # Frame derecho para los controles y la matriz
        self.frame_derecho = tk.Frame(self.frame_principal)
        self.frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame para la entrada de datos y botones
        self.frame_entrada = tk.Frame(self.frame_derecho)
        self.frame_entrada.pack(pady=20)

        tk.Label(self.frame_entrada, text="Ingrese el tamaño del laberinto (filas,columnas):", font=("Arial", 12)).pack()

        self.entrada_tamano = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entrada_tamano.pack(pady=5)

        self.boton_tamano = tk.Button(self.frame_entrada, text="Crear Laberinto", command=self.crear_matriz, font=("Arial", 12))
        self.boton_tamano.pack(pady=10)

        self.boton_obstaculo = tk.Button(self.frame_entrada, text="Activar Modo Obstáculo", command=self.modo_obstaculo, font=("Arial", 12))
        self.boton_obstaculo.pack(pady=10)

        self.boton_queso = tk.Button(self.frame_entrada, text="Poner Queso", command=self.modo_queso, font=("Arial", 12))
        self.boton_queso.pack(pady=10)

        self.boton_raton = tk.Button(self.frame_entrada, text="Colocar Ratón", command=self.modo_raton, font=("Arial", 12))
        self.boton_raton.pack(pady=10)

        self.boton_generar = tk.Button(self.frame_entrada, text="Generar Laberinto txt", command=self.generar_laberinto, font=("Arial", 12))
        self.boton_generar.pack(pady=10)

        tk.Label(self.frame_entrada, text="Nodos de expansión:", font=("Arial", 12)).pack()
        self.entrada_nodos = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entrada_nodos.pack(pady=5)

        self.boton_buscar = tk.Button(self.frame_entrada, text="Iniciar Búsqueda", command=self.iniciar_busqueda, font=("Arial", 12))
        self.boton_buscar.pack(pady=10)
        
        self.nodos_expandidos = tk.IntVar(value=0)
        self.label_nodos = tk.Label(root, textvariable=self.nodos_expandidos)
        self.label_nodos.pack()

        # Frame que contendrá el canvas con scroll
        self.frame_matriz_con_scroll = tk.Frame(self.frame_derecho)
        self.frame_matriz_con_scroll.pack(pady=20, fill=tk.BOTH, expand=True)

        # Canvas para la matriz
        self.canvas_matriz = tk.Canvas(self.frame_matriz_con_scroll)
        self.canvas_matriz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar_vertical = tk.Scrollbar(self.frame_matriz_con_scroll, orient=tk.VERTICAL, command=self.canvas_matriz.yview)
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_matriz.configure(yscrollcommand=self.scrollbar_vertical.set)

        # Crear un frame dentro del canvas para la matriz
        self.frame_matriz = tk.Frame(self.canvas_matriz)
        self.canvas_matriz.create_window((0, 0), window=self.frame_matriz, anchor="nw")

        # Vincular el tamaño del canvas con el contenido del frame de la matriz
        self.frame_matriz.bind("<Configure>", lambda e: self.canvas_matriz.configure(scrollregion=self.canvas_matriz.bbox("all")))

        self.matriz = None
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
        self.modo_raton_activo = False
        self.posicion_raton = None
        self.posicion_queso = None

        self.imagen_queso = Image.open("queso.png")
        self.imagen_queso = self.imagen_queso.resize((50, 50))
        self.imagen_queso = ImageTk.PhotoImage(self.imagen_queso)

        self.imagen_raton = Image.open("raton.png")
        self.imagen_raton = self.imagen_raton.resize((50, 50))
        self.imagen_raton = ImageTk.PhotoImage(self.imagen_raton)

    def crear_matriz(self):
        tamano = self.entrada_tamano.get()
        
        try:
            filas, columnas = map(int, tamano.split(','))
            self.entrada_tamano.delete(0, tk.END)
            self._crear_matriz(filas, columnas)
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto. Ingrese el tamaño como filas,columnas.")

    def _crear_matriz(self, filas, columnas):
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

        for i in range(filas):
            for j in range(columnas):
                boton_celda = tk.Button(self.frame_matriz, width=4, height=2, bg="white", command=lambda x=i, y=j: self.accion_celda(x, y))
                boton_celda.grid(row=i, column=j, padx=1, pady=1)
                self.matriz[i][j] = 0

    def accion_celda(self, fila, columna):
        if self.modo_obstaculo_activo:
            self.marcar_obstaculo(fila, columna)
        elif self.modo_queso_activo:
            self.poner_queso(fila, columna)
        elif self.modo_raton_activo:
            self.poner_raton(fila, columna)

    def marcar_obstaculo(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(bg="black")
        self.matriz[fila][columna] = 1

    def poner_queso(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(image=self.imagen_queso, width=50, height=50)
        self.matriz[fila][columna] = 3
        self.posicion_queso = (fila, columna)

    def poner_raton(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(image=self.imagen_raton, width=50, height=50)
        self.matriz[fila][columna] = 2
        self.posicion_raton = (fila, columna)

    def modo_obstaculo(self):
        self.modo_obstaculo_activo = not self.modo_obstaculo_activo
        self.modo_queso_activo = False
        self.modo_raton_activo = False
        if self.modo_obstaculo_activo:
            self.boton_obstaculo.config(text="Desactivar Modo Obstáculo")
            messagebox.showinfo("Modo Obstáculo", "Haz clic en una celda para colocar un obstáculo.")
        else:
            self.boton_obstaculo.config(text="Activar Modo Obstáculo")

    def modo_queso(self):
        self.modo_queso_activo = not self.modo_queso_activo
        self.modo_obstaculo_activo = False
        self.modo_raton_activo = False
        if self.modo_queso_activo:
            self.boton_queso.config(text="Desactivar Modo Queso")
            messagebox.showinfo("Modo Queso", "Haz clic en una celda para colocar el queso.")
        else:
            self.boton_queso.config(text="Poner Queso")

    def modo_raton(self):
        self.modo_raton_activo = not self.modo_raton_activo
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
        if self.modo_raton_activo:
            self.boton_raton.config(text="Desactivar Modo Ratón")
            messagebox.showinfo("Modo Ratón", "Haz clic en una celda para colocar el ratón.")
        else:
            self.boton_raton.config(text="Colocar Ratón")

    def generar_laberinto(self):
        with open("laberinto.txt", "w") as f:
            filas = len(self.matriz)
            for i in range(filas):
                f.write(" ".join(map(str, self.matriz[i])) + "\n")

        messagebox.showinfo("Éxito", "Laberinto guardado como laberinto.txt")
        
    def actualizar_arbol(self, imagen):
        photo = ImageTk.PhotoImage(imagen)
        self.canvas_arbol.delete("all")
        self.canvas_arbol.create_image(300, 350, image=photo)
        self.canvas_arbol.image = photo  # Mantén una referencia
        self.root.update()
        time.sleep(0.5)

    def actualizar_estrategia(self, nombre_estrategia):
        self.label_estrategia.config(text=f"Estrategia actual: {nombre_estrategia}")
        self.root.update()
        

    def iniciar_busqueda(self):
        nodos_expandir = int(self.entrada_nodos.get())
        
        def run_search():
            ruta = buscar_ruta(
                self.matriz,
                self.posicion_raton,
                self.posicion_queso,
                self.actualizar_arbol,
                self.actualizar_estrategia,
                nodos_expandir
            )
            
            if ruta:
                self.pintar_ruta(ruta)
                messagebox.showinfo("Éxito", "Ruta encontrada: " + str(ruta))
            else:
                messagebox.showwarning("Fallo", "No se encontró una ruta.")

        self.root.after(0, run_search)

     
    def pintar_ruta(self, ruta):
        for (fila, columna) in ruta:
            boton_celda = self.frame_matriz.grid_slaves(row=fila, column=columna)[0]
            boton_celda.config(bg="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()
