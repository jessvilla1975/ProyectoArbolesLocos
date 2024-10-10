import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from busqueda_no_informada import buscar_ruta  

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración del Laberinto")
        self.root.geometry("1000x600")

        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(pady=20)

        # Frame para la entrada de datos y botones
        self.frame_entrada = tk.Frame(self.frame_principal)
        self.frame_entrada.pack(side=tk.LEFT, padx=20)

        # Frame para la matriz
        self.frame_matriz = tk.Frame(self.frame_principal)
        self.frame_matriz.pack(side=tk.RIGHT, padx=20)

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

        # Nueva entrada para los nodos de expansión
        tk.Label(self.frame_entrada, text="Nodos de expansión:", font=("Arial", 12)).pack()
        self.entrada_nodos = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entrada_nodos.pack(pady=5)

        # Botón para iniciar la búsqueda
        self.boton_buscar = tk.Button(self.frame_entrada, text="Iniciar Búsqueda", command=self.iniciar_busqueda, font=("Arial", 12))
        self.boton_buscar.pack(pady=10)

        self.matriz = None
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
        self.modo_raton_activo = False
        self.posicion_raton = None
        self.posicion_queso = None

        self.imagen_queso = Image.open("queso.png")
        self.imagen_queso = self.imagen_queso.resize((50, 50))
        self.imagen_queso = ImageTk.PhotoImage(self.imagen_queso)

        self.imagen_raton = Image.open("raton.png")  # Asegúrate de tener una imagen de ratón
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
            widget.destroy()  # Limpiamos la matriz anterior si existe

        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]  # Inicializamos la matriz con ceros

        for i in range(filas):
            for j in range(columnas):
                boton_celda = tk.Button(self.frame_matriz, width=4, height=2, bg="white", command=lambda x=i, y=j: self.accion_celda(x, y))
                boton_celda.grid(row=i, column=j, padx=1, pady=1)
                self.matriz[i][j] = 0  # Inicializamos cada celda como 0

    def accion_celda(self, fila, columna):
        if self.modo_obstaculo_activo:
            self.marcar_obstaculo(fila, columna)
        elif self.modo_queso_activo:
            self.poner_queso(fila, columna)
        elif self.modo_raton_activo:
            self.poner_raton(fila, columna)

    def marcar_obstaculo(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(bg="black")
        self.matriz[fila][columna] = 1  # Marcamos un obstáculo

    def poner_queso(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(image=self.imagen_queso, width=50, height=50)
        self.matriz[fila][columna] = 3  # Marcamos la posición del queso
        self.posicion_queso = (fila, columna)

    def poner_raton(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(image=self.imagen_raton, width=50, height=50)
        self.matriz[fila][columna] = 2  # Marcamos la posición del ratón
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
                f.write(" ".join(map(str, self.matriz[i])) + "\n")  # Usar espacio en lugar de vacío entre los elementos

        messagebox.showinfo("Éxito", "Laberinto guardado como laberinto.txt")
        
    def iniciar_busqueda(self):
        nodos_expandir = int(self.entrada_nodos.get())
        ruta = buscar_ruta(self.matriz, self.posicion_raton, self.posicion_queso, nodos_expandir)
        
        if ruta:
            self.pintar_ruta(ruta)  # Llamamos al nuevo método para pintar la ruta
            messagebox.showinfo("Éxito", "Ruta encontrada: " + str(ruta))
        else:
            messagebox.showwarning("Fallo", "No se encontró una ruta.")

    def pintar_ruta(self, ruta):
        # Cambia el color de las celdas en la ruta a verde
        for (fila, columna) in ruta:
            boton_celda = self.frame_matriz.grid_slaves(row=fila, column=columna)[0]
            boton_celda.config(bg="yellow")

# Código principal
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()