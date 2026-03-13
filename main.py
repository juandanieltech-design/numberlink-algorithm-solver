# -----------------------------
# archivo: main.py
# -----------------------------
from tablero import Tablero
from interfaz import InterfazJuego
import os
import sys

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <nombre_archivo>")
        print("Ejemplo: python main.py tablero_inicial.txt")
        return

    nombre_archivo = sys.argv[1]
    ruta_archivo = os.path.join("recursos", nombre_archivo)

    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return

    tablero = Tablero(n=7)
    tablero.cargar_desde_archivo(ruta_archivo)
    app = InterfazJuego(tablero)
    app.ejecutar()

if __name__ == "__main__":
    main()
