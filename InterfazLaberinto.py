import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from estrategias import buscar_ruta
from busquedas import *
import time
import random
class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración del Laberinto")
        self.root.geometry("1400x800")
       

        # Calcular el ancho de cada mitad
        mitad_ancho = 1400 // 2

        # Frame izquierdo con scroll (usando Canvas)
        self.canvas_izquierdo = tk.Canvas(root, width=mitad_ancho, height=800, bg="#f7f2f2")
        self.canvas_izquierdo.place(x=0, y=0)

        """ self.scrollbar_izquierda = tk.Scrollbar(root, orient="vertical", command=self.canvas_izquierdo.yview)
        self.scrollbar_izquierda.place(x=mitad_ancho-20, y=0, height=800)

        self.canvas_izquierdo.configure(yscrollcommand=self.scrollbar_izquierda.set) """
        
        self.frame_izquierdo = tk.Frame(self.canvas_izquierdo, width=mitad_ancho, height=1000, bg="#f7f2f2")  # Ajusta la altura
        self.canvas_izquierdo.create_window((0, 0), window=self.frame_izquierdo, anchor="nw")

        # Actualizar el scrollregion
        self.frame_izquierdo.bind("<Configure>", lambda e: self.canvas_izquierdo.configure(scrollregion=self.canvas_izquierdo.bbox("all")))

        # Label estrategia
        self.label_estrategia = tk.Label(self.frame_izquierdo, text="Estrategia: ", font=("Arial", 14), bg="#f7f2f2")
        self.label_estrategia.place(x=20, y=20)

        # Canvas para el árbol
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
        
        self.boton_matriz_predeterminada = tk.Button(self.frame_entrada, text="Predeterminada", command=self.crear_matriz_predeterminada, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_matriz_predeterminada.place(x=500, y=110)

        # Botón para colocar ratonera
        self.boton_ratonera = tk.Button(self.frame_entrada, text="Colocar Ratonera", command=self.modo_ratonera, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_ratonera.place(x=20, y=150)


        self.boton_limpiar = tk.Button(self.frame_entrada, text="Limpiar Laberinto", command=self.limpiar_matriz, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_limpiar.place(x=185, y=150)
        
        self.boton_limpiar_camino = tk.Button(self.frame_entrada, text="Limpiar Camino", command=self.limpiar, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_limpiar_camino.place(x=350, y=150)
        
        self.boton_aleatorio = tk.Button(self.frame_entrada, text="Aleatorio", command=self.crear_matriz_aleatoria, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_aleatorio.place(x=500, y=150)
        
        self.label_metodos = tk.Label(self.frame_entrada, text="Seleccione el método de búsqueda:", font=("Arial", 12, "bold"), bg="#f7f2f2").place(x=20, y=190)
        
        self.boton_amplitud = tk.Button(self.frame_entrada, text="Amplitud", command=self.busquedadAmplitud, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_amplitud.place(x=20, y=215)
        
        self.boton_costo = tk.Button(self.frame_entrada, text="costo", command=self.busquedadCosto, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_costo.place(x=120, y=215)
        
        self.boton_iterativa = tk.Button(self.frame_entrada, text="Iterativa", command=self.busquedadIterativa, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_iterativa.place(x=195, y=215)
        
        self.boton_profundidad = tk.Button(self.frame_entrada, text="Profundidad", command=self.busquedadProfundida, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_profundidad.place(x=285, y=215)

        self.boton_profundidad = tk.Button(self.frame_entrada, text="Avara", command=self.busquedaAvara, font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_profundidad.place(x=410, y=215)
        
        self.boton_limite = tk.Button(self.frame_entrada, text="Limitada", command=self.busquedadLimitadaProfundidad , font=("Arial", 11, "bold"), bg="#353131", fg="white")
        self.boton_limite.place(x=490, y=215)



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
        # Scrollbar para el canvas del árbol
        self.scrollbar_arbol = tk.Scrollbar(self.frame_izquierdo, orient="vertical", command=self.canvas_arbol.yview)
        self.scrollbar_arbol.place(x=mitad_ancho-40, y=60, height=500)

        self.canvas_arbol.configure(yscrollcommand=self.scrollbar_arbol.set)



        self.matriz = None
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
        self.modo_ratonera_activo = False  # Estado para la ratonera
        self.modo_raton_activo = False
        self.posicion_raton = None
        self.posicion_queso = None
        self.posicion_ratonera = None  # Posición para la ratonera

        self.imagen_queso = Image.open("queso.png")
        self.imagen_queso = self.imagen_queso.resize((50, 50))
        self.imagen_queso = ImageTk.PhotoImage(self.imagen_queso)

        self.imagen_raton = Image.open("raton.png")
        self.imagen_raton = self.imagen_raton.resize((50, 50))
        self.imagen_raton = ImageTk.PhotoImage(self.imagen_raton)

        self.imagen_ratonera = Image.open("ratonera.png")
        self.imagen_ratonera = self.imagen_ratonera.resize((50, 50))
        self.imagen_ratonera = ImageTk.PhotoImage(self.imagen_ratonera)
        self.crear_matriz_predeterminada()

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
                label_posicion = tk.Label(self.frame_matriz, text=f"({i},{j})", font=("Arial", 8), bg="white")
                label_posicion.place(in_=boton_celda, relx=0.5, rely=0.5, anchor="center")

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
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
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
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
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
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
            else:
                messagebox.showwarning("Fallo", "No se encontró una ruta.")

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)   
    
    def busquedadProfundida(self):
        #aqui poner la funcion de generar laberinto
        self.generar_laberinto()
        nodos_expandir = int(self.entrada_nodos.get())
        
        def run_search():
            ruta = preferente_profundidad(
                self.matriz,
                self.posicion_raton,
                self.posicion_queso,
                self.actualizar_arbol,
                self.actualizar_estrategia,
                nodos_expandir
            )
            
            if ruta:
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
            else:
                messagebox.showwarning("Fallo", "No se encontró una ruta.")

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)
        
    def busquedadLimitadaProfundidad(self):
        self.generar_laberinto()
        nodos_expandir = int(self.entrada_nodos.get())

        def run_search():
            ruta = limitada_por_profundidad(
                self.matriz,
                self.posicion_raton,
                self.posicion_queso,
                self.actualizar_arbol,
                self.actualizar_estrategia,
                nodos_expandir
            )

            if ruta:
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
            else:
                messagebox.showwarning("Fallo", "No se encontró una ruta.")

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)

    def busquedaAvara(self):
        #aqui poner la funcion de generar laberinto
        self.generar_laberinto()
        nodos_expandir = int(self.entrada_nodos.get())
        
        def run_search():
            ruta = Avara(
                self.matriz,
                self.posicion_raton,
                self.posicion_queso,
                self.actualizar_arbol,
                self.actualizar_estrategia,
                nodos_expandir
            )
            
            if ruta:
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
            else:
                messagebox.showwarning("Fallo", "No se encontró una ruta.")

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)
        
    def accion_celda(self, fila, columna):
        if self.modo_obstaculo_activo:
            self.marcar_obstaculo(fila, columna)
        elif self.modo_queso_activo:
            self.poner_queso(fila, columna)
        elif self.modo_raton_activo:
            self.poner_raton(fila, columna)
        elif self.modo_ratonera_activo:
            self.poner_ratonera(fila, columna)

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

    def poner_ratonera(self, fila, columna):
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(image=self.imagen_ratonera, width=50, height=50)
        self.matriz[fila][columna] = 4  # Identificador para la ratonera
        self.posicion_ratonera = (fila, columna)

    def modo_obstaculo(self):
        self.modo_obstaculo_activo = not self.modo_obstaculo_activo
        self.modo_queso_activo = False
        self.modo_raton_activo = False
        self.modo_ratonera_activo = False
       

    def modo_queso(self):
        self.modo_queso_activo = not self.modo_queso_activo
        self.modo_obstaculo_activo = False
        self.modo_raton_activo = False
        self.modo_ratonera_activo = False
        

    def modo_raton(self):
        self.modo_raton_activo = not self.modo_raton_activo
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
        self.modo_ratonera_activo = False

    def modo_ratonera(self):
        self.modo_ratonera_activo = not self.modo_ratonera_activo
        self.modo_obstaculo_activo = False
        self.modo_queso_activo = False
        self.modo_raton_activo = False
 
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
        time.sleep(1)

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
                self.mover_raton_a_la_ruta(ruta)
                messagebox.showinfo("Éxito", "Encontro el quesito :)")
            else:
                messagebox.showwarning("Fallo", "No se encontró una ruta.")

        # Ejecutamos la búsqueda en un hilo separado
        self.root.after(0, run_search)

     
    def mover_raton_a_la_ruta(self, ruta):

        for (fila, columna) in ruta:
            boton_celda = self.frame_matriz.grid_slaves(row=fila, column=columna)[0]
            boton_celda.config(bg="yellow")
            
        for paso in ruta:
            fila, columna = paso
            # Mover el ratón en la interfaz
            self.mover_raton(fila, columna)
            # Esperar un poco antes de mover al siguiente paso para mostrar el movimiento
            self.root.after(500)  # Espera de 500 ms entre pasos (ajustable)
            self.root.update()  # Actualiza la interfaz

    def mover_raton(self, fila, columna):

        if self.posicion_raton:
            fila_anterior, columna_anterior = self.posicion_raton
            # Borrar la imagen del ratón de la celda anterior
            self.frame_matriz.grid_slaves(row=fila_anterior, column=columna_anterior)[0].config(image="", width=4, height=2)
            self.matriz[fila_anterior][columna_anterior] = 0

        # Colocar la imagen del ratón en la nueva celda
        self.frame_matriz.grid_slaves(row=fila, column=columna)[0].config(image=self.imagen_raton, width=50, height=50)
        self.matriz[fila][columna] = 2
        self.posicion_raton = (fila, columna)  # Actualizar la posición del ratón


            
    # Función para pintar las celdas de blanco conservando las imagenes
    def limpiar(self):
        filas = len(self.matriz)
        columnas = len(self.matriz[0])
        
        for i in range(filas):
            for j in range(columnas):
                boton_celda = self.frame_matriz.grid_slaves(row=i, column=j)[0]
                if self.matriz[i][j] == 2:
                    boton_celda.config(bg="white", image=self.imagen_raton, width=50, height=50)
                    self.matriz[i][j] = 2
                elif self.matriz[i][j] == 3:
                    boton_celda.config(bg="white", image=self.imagen_queso, width=50, height=50)
                    self.matriz[i][j] = 3
                elif self.matriz[i][j] == 4:
                    boton_celda.config(bg="white", image=self.imagen_ratonera, width=50, height=50)
                    self.matriz[i][j] = 4
                elif self.matriz[i][j] == 1:
                    boton_celda.config(bg="black", image="", width=4, height=2)
                    self.matriz[i][j] = 1
                else:
                    boton_celda.config(bg="white", image="", width=4, height=2)
                    

       
        messagebox.showinfo("Limpiar Camino", "El camino ha sido limpiado.")
        
    def crear_matriz_predeterminada(self):
 
        filas, columnas = 4, 4
        self._crear_matriz(filas, columnas)
        
        # Definir posiciones predeterminadas para queso, obstáculo y ratón
        # Asignamos 1 para obstáculo, 2 para ratón, 3 para queso
        self.posicion_raton = (1, 1)
        self.posicion_queso = (0, 2)
        self.posicion_ratonera = (2, 0)
        
        # Marcamos las celdas en la interfaz gráfica
        self.poner_queso(1, 3)  # Poner queso en (0, 2)
        self.marcar_obstaculo(1, 1)  # Poner obstáculo en (2, 0)
        self.marcar_obstaculo(2, 1)  # Poner obstáculo en (2, 0)
        self.marcar_obstaculo(1, 2)  # Poner obstáculo en (2, 0)
        self.marcar_obstaculo(3, 3)  # Poner obstáculo en (2, 0)
        self.poner_raton(2, 0)  # Poner ratón en (1, 1)
        
    def crear_matriz_aleatoria(self):
        # Generar un tamaño aleatorio para la matriz
        filas = random.randint(3, 5)
        columnas = random.randint(3, 5)
        self._crear_matriz(filas, columnas)

        # Función para verificar si una celda está libre (vacía, no es un obstáculo ni el ratón ni el queso)
        def es_celda_libre(fila, columna):
            # Verificamos que la celda no esté ocupada por un ratón, queso o un obstáculo
            return self.matriz[fila][columna] == 0  # 0 significa vacía

        # Poner el queso en una celda aleatoria vacía
        fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
        while not es_celda_libre(fila, columna):
            fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
        self.poner_queso(fila, columna)

        # Poner el ratón en una celda aleatoria vacía
        fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
        while not es_celda_libre(fila, columna):
            fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
        self.poner_raton(fila, columna)

        # Poner obstáculos en celdas aleatorias vacías
        for _ in range(5):  # Número de obstáculos
            fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
            while not es_celda_libre(fila, columna):  # Verifica si la celda está libre
                fila, columna = random.randint(0, filas-1), random.randint(0, columnas-1)
            self.marcar_obstaculo(fila, columna)

     
        
                
      
        

if __name__ == "__main__":
    
    root = tk.Tk()

    app = InterfazLaberinto(root)
    root.mainloop()

