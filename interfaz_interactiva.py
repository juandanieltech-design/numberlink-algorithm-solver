# interfaz_interactiva.py
import tkinter as tk
import os
import time
from tablero import Tablero
from jugadores.backtracking_player import BacktrackingPlayer
from jugadores.greedy_player import GreedyPlayer
from jugadores.csp_player import CSPPlayer

COLORES = ["red", "green", "blue", "orange", "purple", "brown", "teal", "gold", "pink", "cyan"]

class InterfazInteractiva:
    def __init__(self, tablero, rutas):
        self.tablero = tablero
        self.rutas = rutas
        self.n = tablero.n
        self.celda_size = 50
        self.root = tk.Tk()
        self.root.title("Animación del algoritmo")
        self.canvas = tk.Canvas(self.root, width=self.n*self.celda_size, height=self.n*self.celda_size)
        self.canvas.pack()
        self.dibujar_tablero()
        self.pasos = self.obtener_pasos_rutas()
        self.paso_actual = 0

    def dibujar_tablero(self):
        for i in range(self.n):
            for j in range(self.n):
                x0 = j * self.celda_size
                y0 = i * self.celda_size
                x1 = x0 + self.celda_size
                y1 = y0 + self.celda_size
                valor = self.tablero.matriz[i][j]
                color = "white" if valor == 0 else "lightgray"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                if valor != 0:
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(valor), font=("Arial", 14, "bold"))

    def obtener_pasos_rutas(self):
        pasos = []
        for k, camino in self.rutas.items():
            pasos.append((k, camino))  # cada paso es una ruta completa
        return pasos

    def dibujar_ruta_con_linea(self, camino, color, index=0):
        if index >= len(camino) - 1:
            self.paso_actual += 1
            self.root.after(300, self.dibujar_rutas_una_a_una)
            return

        (x1, y1) = camino[index]
        (x2, y2) = camino[index + 1]

        x1_pix = y1 * self.celda_size + self.celda_size // 2
        y1_pix = x1 * self.celda_size + self.celda_size // 2
        x2_pix = y2 * self.celda_size + self.celda_size // 2
        y2_pix = x2 * self.celda_size + self.celda_size // 2

        self.canvas.create_line(x1_pix, y1_pix, x2_pix, y2_pix, fill=color, width=4)

        self.root.after(150, lambda: self.dibujar_ruta_con_linea(camino, color, index + 1))

    def dibujar_rutas_una_a_una(self):
        if self.paso_actual >= len(self.pasos):
            return
        k, camino = self.pasos[self.paso_actual]
        color = COLORES[(k - 1) % len(COLORES)]
        self.dibujar_ruta_con_linea(camino, color)

    def ejecutar_con_animacion(self):
        self.root.after(500, self.dibujar_rutas_una_a_una)
        self.root.mainloop()


def seleccionar_archivo():
    archivos = [f for f in os.listdir("recursos") if f.endswith(".txt")]
    print("Tableros disponibles:")
    for idx, nombre in enumerate(archivos, start=1):
        print(f"{idx}. {nombre}")
    idx = int(input("\nSelecciona un tablero por número: ")) - 1
    return os.path.join("recursos", archivos[idx])

def seleccionar_algoritmo():
    print("\nSelecciona un algoritmo:")
    print("1. Backtracking")
    print("2. Greedy")
    print("3. CSP")
    opc = int(input("> "))
    if opc == 1:
        return BacktrackingPlayer(), "Backtracking"
    elif opc == 2:
        return GreedyPlayer(), "Greedy"
    elif opc == 3:
        return CSPPlayer(), "CSP"
    else:
        raise ValueError("Opción inválida.")

def main():
    path = seleccionar_archivo()
    algoritmo, nombre = seleccionar_algoritmo()

    tablero = Tablero(n=7)
    tablero.cargar_desde_archivo(path)

    print(f"\nEjecutando {nombre} sobre {os.path.basename(path)}...")

    inicio = time.perf_counter()
    rutas = algoritmo.resolver(tablero)
    fin = time.perf_counter()

    if rutas is None:
        print(f"{nombre}: ❌ No encontró solución.")
        return

    print(f"{nombre} encontró solución en {fin - inicio:.2f} segundos.")
    app = InterfazInteractiva(tablero, rutas)
    app.ejecutar_con_animacion()

if __name__ == "__main__":
    main()
