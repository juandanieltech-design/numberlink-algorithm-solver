# -----------------------------
# archivo: interfaz.py
# -----------------------------
import tkinter as tk

class InterfazJuego:
    def __init__(self, tablero):
        self.tablero = tablero
        self.n = tablero.n
        self.celda_size = 50
        self.root = tk.Tk()
        self.root.title("NumberLink - Interfaz del Juego")

        self.canvas = tk.Canvas(self.root, width=self.n * self.celda_size,
                                           height=self.n * self.celda_size)
        self.canvas.pack()

        self.status = tk.Label(self.root, text="Haz clic en una celda para comenzar")
        self.status.pack(pady=3)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Mostrar Conexiones", command=self.dibujar_conexiones).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Reiniciar Juego", command=self.reiniciar_tablero).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Verificar Juego", command=self.verificar_juego).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Deshacer Última Ruta", command=self.deshacer_ultima_ruta).pack(side=tk.LEFT, padx=5)

        self.origen = None
        self.camino_actual = []
        self.lineas_trazadas = []  # lista de (line_id, etiqueta)
        self.ocupado = {}          # celda (x,y): etiqueta
        self.rutas = {}            # etiqueta: lista de celdas
        self.colores_etiquetas = {}
        self.colores_disponibles = ["red", "blue", "green", "orange", "purple", "brown", "cyan", "magenta"]

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.deshacer_click_derecho)
        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * self.celda_size
                y1 = i * self.celda_size
                x2 = x1 + self.celda_size
                y2 = y1 + self.celda_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="#f0f0f0")
                val = self.tablero.matriz[i][j]
                if val != 0:
                    self.canvas.create_text(x1 + 25, y1 + 25, text=str(val), font=("Arial", 16))

    def on_click(self, event):
        fila, col = event.y // self.celda_size, event.x // self.celda_size
        if fila >= self.n or col >= self.n:
            return

        if self.origen is None:
            if self.tablero.matriz[fila][col] != 0:
                self.origen = (fila, col)
                self.camino_actual = [self.origen]
                self.status.config(text=f"Iniciando desde {self.origen}")
        else:
            nuevo = (fila, col)
            if self.es_vecino(self.camino_actual[-1], nuevo) and (nuevo not in self.ocupado):
                self.camino_actual.append(nuevo)
                self.trazar_segmento(self.camino_actual[-2], nuevo)

                if self.tablero.matriz[nuevo[0]][nuevo[1]] == self.tablero.matriz[self.origen[0]][self.origen[1]] and nuevo != self.origen:
                    if self.validar_camino_completo(self.camino_actual):
                        etiqueta = self.tablero.matriz[nuevo[0]][nuevo[1]]
                        for celda in self.camino_actual:
                            self.ocupado[celda] = etiqueta
                        self.rutas[etiqueta] = list(self.camino_actual)
                        self.status.config(text=f"✔️ Conectado par {etiqueta}")
                        self.origen = None
                        self.camino_actual.clear()
                    else:
                        self.status.config(text="❌ Ruta inválida: colisión o paso incorrecto")
                        self.marcar_error()
            else:
                self.status.config(text="⚠️ Movimiento inválido: no adyacente o ya ocupado")

    def es_vecino(self, a, b):
        return (abs(a[0] - b[0]) == 1 and a[1] == b[1]) or (abs(a[1] - b[1]) == 1 and a[0] == b[0])

    def trazar_segmento(self, a, b):
        etiqueta = self.tablero.matriz[self.origen[0]][self.origen[1]]
        if etiqueta not in self.colores_etiquetas:
            idx = len(self.colores_etiquetas) % len(self.colores_disponibles)
            self.colores_etiquetas[etiqueta] = self.colores_disponibles[idx]
        color = self.colores_etiquetas[etiqueta]

        x1 = a[1] * self.celda_size + self.celda_size // 2
        y1 = a[0] * self.celda_size + self.celda_size // 2
        x2 = b[1] * self.celda_size + self.celda_size // 2
        y2 = b[0] * self.celda_size + self.celda_size // 2
        line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        self.lineas_trazadas.append((line, etiqueta))

    def validar_camino_completo(self, camino):
        inicio, fin = camino[0], camino[-1]
        valor = self.tablero.matriz[inicio[0]][inicio[1]]
        if self.tablero.matriz[fin[0]][fin[1]] != valor:
            return False
        for x, y in camino[1:-1]:
            if self.tablero.matriz[x][y] != 0 or (x, y) in self.ocupado:
                return False
        return True

    def marcar_error(self):
        for line_id, _ in self.lineas_trazadas:
            self.canvas.itemconfig(line_id, fill="red", width=3)
        self.root.after(1000, self.limpiar_ruta_actual)

    def limpiar_ruta_actual(self):
        for line_id, _ in self.lineas_trazadas:
            self.canvas.delete(line_id)
        self.lineas_trazadas.clear()
        self.camino_actual.clear()
        self.origen = None

    def verificar_juego(self):
        if self.tablero.esta_lleno_logico(self.rutas):
            self.status.config(text="🎉 ¡Juego completado correctamente!")
        else:
            self.status.config(text="Faltan rutas o hay errores")

    def reiniciar_tablero(self):
        self.ocupado.clear()
        self.rutas.clear()
        self.lineas_trazadas.clear()
        self.origen = None
        self.camino_actual.clear()
        self.dibujar_tablero()
        self.status.config(text="Tablero reiniciado")

    def dibujar_conexiones(self):
        self.dibujar_tablero()
        colores = self.colores_disponibles
        for idx, ((x1, y1), (x2, y2)) in enumerate(self.tablero.obtener_parejas()):
            x1c = y1 * self.celda_size + self.celda_size // 2
            y1c = x1 * self.celda_size + self.celda_size // 2
            x2c = y2 * self.celda_size + self.celda_size // 2
            y2c = x2 * self.celda_size + self.celda_size // 2
            self.canvas.create_line(x1c, y1c, x2c, y2c, fill=colores[idx % len(colores)], width=2)
        self.status.config(text="Conexiones automáticas mostradas (lineales)")

    def deshacer_ultima_ruta(self):
        if not self.rutas:
            self.status.config(text="⚠️ No hay rutas para deshacer")
            return

        ultima = max(self.rutas.keys())  # Última etiqueta agregada
        celdas = self.rutas.pop(ultima)
        self.ocupado = {k: v for k, v in self.ocupado.items() if v != ultima}
        self.lineas_trazadas = [(lid, etq) for lid, etq in self.lineas_trazadas if etq != ultima]

        self.dibujar_tablero()

        # Redibujar todas las rutas activas
        for etiqueta, camino in self.rutas.items():
            color = self.colores_etiquetas.get(etiqueta, "black")
            for i in range(1, len(camino)):
                a, b = camino[i - 1], camino[i]
                x1 = a[1] * self.celda_size + self.celda_size // 2
                y1 = a[0] * self.celda_size + self.celda_size // 2
                x2 = b[1] * self.celda_size + self.celda_size // 2
                y2 = b[0] * self.celda_size + self.celda_size // 2
                lid = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
                self.lineas_trazadas.append((lid, etiqueta))

        self.status.config(text=f"↩️ Ruta {ultima} deshecha")

    def deshacer_click_derecho(self, event):
        self.deshacer_ultima_ruta()

    def ejecutar(self):
        self.root.mainloop()