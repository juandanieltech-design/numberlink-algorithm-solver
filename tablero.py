# -----------------------------
# archivo: tablero.py
# -----------------------------
from collections import deque

class Tablero:
    def __init__(self, n):
        self.n = n
        self.matriz = [[0 for _ in range(n)] for _ in range(n)]
        self.pares = []

    def cargar_desde_archivo(self, path):
        with open(path, 'r') as f:
            lineas = [line.strip() for line in f if line.strip()]
        self.n = int(lineas[0].split(',')[0])
        self.matriz = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.pares = []

        for linea in lineas[1:]:
            x, y, val = map(int, linea.split(','))
            if self.matriz[x][y] != 0:
                raise ValueError(f"Celda duplicada: ({x},{y})")
            self.matriz[x][y] = val
            self.pares.append((x, y))

    def obtener_parejas(self):
        etiquetas = {}
        for x, y in self.pares:
            val = self.matriz[x][y]
            etiquetas.setdefault(val, []).append((x, y))
        return [(coords[0], coords[1]) for coords in etiquetas.values() if len(coords) == 2]

    def esta_lleno_logico(self, rutas):
        parejas_reales = self.obtener_parejas()
        etiquetas_conectadas = set(rutas.keys())
        return len(etiquetas_conectadas) == len(parejas_reales)
