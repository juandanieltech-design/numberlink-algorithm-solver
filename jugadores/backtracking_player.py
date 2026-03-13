class BacktrackingPlayer:
    def __init__(self):
        self.tablero = None
        self.n = 0
        self.solucion = {}

    def resolver(self, tablero):
        from copy import deepcopy
        self.tablero = tablero
        self.n = tablero.n
        parejas = tablero.obtener_parejas()
        return self._backtrack(0, parejas, {}, set())

    def _backtrack(self, idx, parejas, rutas, ocupadas):
        if idx == len(parejas):
            return rutas

        (x1, y1), (x2, y2) = parejas[idx]
        caminos = self._buscar_caminos((x1, y1), (x2, y2), ocupadas)

        for camino in caminos:
            nuevas_ocupadas = ocupadas | set(camino[1:-1])
            rutas[self.tablero.matriz[x1][y1]] = camino  # ← CORREGIDO
            resultado = self._backtrack(idx + 1, parejas, rutas.copy(), nuevas_ocupadas)
            if resultado:
                return resultado

        return None

    def _buscar_caminos(self, inicio, fin, ocupadas):
        from collections import deque
        caminos = []
        queue = deque()
        queue.append((inicio, [inicio]))
        visitado = set()

        while queue:
            actual, camino = queue.popleft()
            if actual == fin:
                caminos.append(camino)
                continue
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = actual[0]+dx, actual[1]+dy
                if 0 <= nx < self.n and 0 <= ny < self.n:
                    if (nx, ny) not in camino and (nx, ny) not in ocupadas:
                        if self.tablero.matriz[nx][ny] == 0 or (nx, ny) == fin:
                            queue.append(((nx, ny), camino + [ (nx, ny) ]))
        return caminos
