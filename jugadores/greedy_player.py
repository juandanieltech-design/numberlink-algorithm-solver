class GreedyPlayer:
    def resolver(self, tablero):
        rutas = {}
        ocupadas = set()  # Guarda celdas ya utilizadas para evitar solapamientos

        for (a, b) in tablero.obtener_parejas():
            camino = self.camino_mas_corto(tablero, a, b, ocupadas)
            if not camino:
                print(f"[Greedy] Falló al conectar {a} -> {b}")  # Log de fallo
                return None  # Falla si no puede conectar una pareja
            rutas[tablero.matriz[a[0]][a[1]]] = camino
            ocupadas.update(camino[1:-1])  # Marca las celdas como ocupadas, sin contar los extremos

        return rutas

    def camino_mas_corto(self, tablero, inicio, fin, ocupadas):
        from collections import deque
        n = tablero.n
        queue = deque([(inicio, [inicio])])
        visitado = set([inicio])

        while queue:
            actual, camino = queue.popleft()
            if actual == fin:
                return camino

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # Movimientos ortogonales
                nx, ny = actual[0] + dx, actual[1] + dy
                if 0 <= nx < n and 0 <= ny < n:
                    sig = (nx, ny)
                    # Condición para continuar: no visitado, no ocupado, o es destino
                    if sig not in visitado and (tablero.matriz[nx][ny] == 0 or sig == fin) and sig not in ocupadas:
                        queue.append((sig, camino + [sig]))
                        visitado.add(sig)

        return None  # No hay camino posible