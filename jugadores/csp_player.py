class CSPPlayer:
    def resolver(self, tablero):
        # Versión simplificada de CSP: se delega al backtracking tradicional.
        # Se sugiere como extensión futura con heurísticas (ej. MRV, forward-checking).
        from jugadores.backtracking_player import BacktrackingPlayer
        return BacktrackingPlayer().resolver(tablero)
