import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from estrategias import buscar_ruta
from busquedas import buscar_amplitud, costo_uniforme, iterativa
import time

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración del Laberinto")
        self.root.geometry("1400x800")

        # Calcular el ancho de cada mitad
        mitad_ancho = 1400 // 2

        # Frame izquierdo (mitad izquierda de la pantalla)
        self.frame_izquierdo = tk.Frame(root, width=mitad_ancho, height=800, bg="#f7f2f2")
        self.frame_izquierdo.place(x=0, y=0)

        self.label_estrategia = tk.Label(self.frame_izquierdo, text="Estrategia: ", font=("Arial", 14), bg="#f7f2f2")
        self.label_estrategia.place(x=20, y=20)

        self.canvas_arbol = tk.Canvas(self.frame_izquierdo, width=mitad_ancho-40, height=700, bg="#f7f2f2")
        self.canvas_arbol.place(x=20, y=60)

        # Frame derecho (mitad derecha de la pantalla)
        self.frame_derecho = tk.Frame(root, width=mitad_ancho, height=800, bg="#f7f2f2")
        self.frame_derecho.place(x=mitad_ancho, y=0)

        # Frame de entrada en la parte superior del frame derecho
        self.frame_entrada = tk.Frame(self.frame_derecho, width=mitad_ancho, height=260, bg="#f7f2f2")
        self.frame_entrada.place(x=0, y=0)

        tk.Label(self.frame_entrada, text="Ingrese el tamaño del laberinto (M,N):", font=("Arial", 12, "bold"), bg="#f7f2f2").place(x=20, y=20)
        self.entrada_tamano = tk.Entry(self.frame_entrada, font=("Arial", 12), width=10)
        self.entrada_tamano.place(x=310, y=20)

        tk.Label(self.frame_entrada, text="Nodos de expansión:", font=("Arial", 12, "bold"), bg="#f7f2f2").place(x=20, y=60)
        self.entrada_nodos = tk.Entry(self.frame_entrada, font=("Arial", 12), width=10)
        self.entrada_nodos.place(x=310, y=60)

        self.boton_tamano = tk.Button(self.frame_entrada, text="Crear Laberinto", command=self.crear_matriz, font=("Arial", 11, "bold"), width=15, bg="#353131", fg="white")
        self.boton_tamano.place(x=420, y=20)

        self.boton_buscar = tk.Button(self.frame_entrada, text="Iniciar Búsqueda", command=self.iniciar_busqueda, font=("Arial", 11, "bold"), width=15, bg="#3b8d21", fg="white")
        self.boton_buscar.place(x=420, y=60)

        self.boton_obstaculo = tk.Button(self.frame_entrada, text="Activar Modo Obstáculo", command=self.modo_obstaculo, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_obstaculo.place(x=20, y=110)
        
        self.boton_queso = tk.Button(self.frame_entrada, text="Poner Queso", command=self.modo_queso, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_queso.place(x=230, y=110)

        self.boton_raton = tk.Button(self.frame_entrada, text="Colocar Ratón", command=self.modo_raton, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_raton.place(x=370, y=110)

        self.boton_limpiar = tk.Button(self.frame_entrada, text="Limpiar Laberinto", command=self.limpiar_matriz, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_limpiar.place(x=20, y=150)
        
        self.label_metodos = tk.Label(self.frame_entrada, text="Seleccione el método de búsqueda:", font=("Arial", 12, "bold"), bg="#f7f2f2").place(x=20, y=190)
        
        self.boton_amplitud = tk.Button(self.frame_entrada, text="Amplitud", command=self.busquedadAmplitud, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_amplitud.place(x=20, y=215)
        
        self.boton_costo = tk.Button(self.frame_entrada, text="costo", command=self.busquedadCosto, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_costo.place(x=120, y=215)
        
        self.boton_iterativa = tk.Button(self.frame_entrada, text="Iterativa", command=self.busquedadIterativa, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_iterativa.place(x=195, y=215)
        
        self.boton_profundidad = tk.Button(self.frame_entrada, text="Profundidad", command=self.busquedadProfundida, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_profundidad.place(x=285, y=215)


        # Frame para la matriz en la parte inferior del frame derecho
        self.frame_matriz = tk.Frame(self.frame_derecho, width=mitad_ancho, height=540, bg="#f7f2f2")
        self.frame_matriz.place(x=200, y=280)

        # Canvas para la matriz
        self.canvas_matriz = tk.Canvas(self.frame_matriz, width=mitad_ancho-20, height=540, bg="#f7f2f2")
        self.canvas_matriz.place(x=10, y=10)

        # Frame dentro del canvas para la matriz
        self.frame_matriz_dentro_canvas = tk.Frame(self.canvas_matriz)
        self.canvas_matriz.create_window((0, 0), window=self.frame_matriz_dentro_canvas, anchor="nw")

        # Vincular el tamaño del canvas con el contenido del frame de la matriz
        self.frame_matriz_dentro_canvas.bind("<Configure>", lambda e: self.canvas_matriz.configure(scrollregion=self.canvas_matriz.bbox("all")))

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

    def limpiar_matriz(self):
        filas = len(self.matriz)
        columnas = len(self.matriz[0])
        
        for i in range(filas):
            for j in range(columnas):
                boton_celda = self.frame_matriz.grid_slaves(row=i, column=j)[0]
                boton_celda.config(bg="white", image="", width=4, height=2)
                self.matriz[i][j] = 0
        
        self.nodos_expandidos.set(0)
        messagebox.showinfo("Limpiar Matriz", "Todas las celdas han sido limpiadas.")

    def busquedadAmplitud(self):
        #aqui poner la funcion de generar laberinto
        self.generar_laberinto()
        nodos_expandir = int(self.entrada_nodos.get())
        
        def run_search():
            ruta = buscar_amplitud(
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

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)
      
    def busquedadCosto(self):
        #aqui poner la funcion de generar laberinto
        self.generar_laberinto()
        nodos_expandir = int(self.entrada_nodos.get())
        
        def run_search():
            ruta = costo_uniforme(
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

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)
        
    def busquedadIterativa(self):
        #aqui poner la funcion de generar laberinto
        self.generar_laberinto()
        nodos_expandir = int(self.entrada_nodos.get())
        
        def run_search():
            ruta = iterativa(
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

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)   
    
    def busquedadProfundida(self):
        messagebox.showinfo("Profundidad", "Profundidad")


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
       

    def modo_queso(self):
        self.modo_queso_activo = not self.modo_queso_activo
        self.modo_obstaculo_activo = False
        self.modo_raton_activo = False
        

    def modo_raton(self):
        self.modo_raton_activo = not self.modo_raton_activo
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
 

    def generar_laberinto(self):
        with open("laberinto.txt", "w") as f:
            filas = len(self.matriz)
            for i in range(filas):
                f.write(" ".join(map(str, self.matriz[i])) + "\n")

        #messagebox.showinfo("Éxito", "Laberinto guardado como laberinto.txt")
        
    def actualizar_arbol(self, imagen):
        photo = ImageTk.PhotoImage(imagen)
        self.canvas_arbol.delete("all")
        self.canvas_arbol.create_image(300, 350, image=photo)
        self.canvas_arbol.image = photo
        self.root.update()
        time.sleep(0.5)

    def actualizar_estrategia(self, nombre_estrategia):
        def update():
            try:
                if self.label_estrategia.winfo_exists():
                    self.label_estrategia.config(text=f"Estrategia actual: {nombre_estrategia}")
                    self.root.update_idletasks()
            except tk.TclError:
                print(f"No se pudo actualizar la etiqueta de estrategia: {nombre_estrategia}")

        self.root.after(0, update)

    def iniciar_busqueda(self):
        #aqui poner la funcion de generar laberinto
        self.generar_laberinto()
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

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)

     
    def pintar_ruta(self, ruta):
        for (fila, columna) in ruta:
            boton_celda = self.frame_matriz.grid_slaves(row=fila, column=columna)[0]
            boton_celda.config(bg="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()
