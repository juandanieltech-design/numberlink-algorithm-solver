# run_experimentos.py
import time
import sys
import os
import csv
from multiprocessing import Process, Queue
from tablero import Tablero
from jugadores.backtracking_player import BacktrackingPlayer
from jugadores.greedy_player import GreedyPlayer
from jugadores.csp_player import CSPPlayer

TIEMPO_LIMITE = 120  # segundos

def ejecutar_algoritmo(queue, algoritmo, path):
    try:
        tablero = Tablero(n=7)
        tablero.cargar_desde_archivo(path)
        rutas = algoritmo.resolver(tablero)
        queue.put(("ok", rutas))
    except Exception as e:
        queue.put(("error", str(e)))

def evaluar(algoritmo, nombre, path):
    queue = Queue()
    proceso = Process(target=ejecutar_algoritmo, args=(queue, algoritmo, path))
    inicio = time.perf_counter()
    proceso.start()
    proceso.join(timeout=TIEMPO_LIMITE)
    fin = time.perf_counter()
    duracion = fin - inicio

    if proceso.is_alive():
        proceso.terminate()
        proceso.join()
        print(f"{nombre}: ❌⏰ Tiempo excedido ({TIEMPO_LIMITE}s)")
        return (nombre, 0, TIEMPO_LIMITE)
    elif not queue.empty():
        estado, resultado = queue.get()
        if estado == "ok" and resultado is not None:
            print(f"{nombre}: ✔️ en {duracion:.4f} segundos")
            return (nombre, 1, round(duracion, 4))
        else:
            print(f"{nombre}: ❌ Error en ejecución ({resultado})")
            return (nombre, 0, round(duracion, 4))
    else:
        print(f"{nombre}: ❌ Error desconocido (sin resultado)")
        return (nombre, 0, round(duracion, 4))

def guardar_csv(nombre_tablero, resultados):
    os.makedirs("resultados", exist_ok=True)
    archivo_salida = os.path.join("resultados", f"experimento_{nombre_tablero}.csv")
    with open(archivo_salida, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Éxito", "Tiempo (segundos)"])
        for fila in resultados:
            writer.writerow(fila)
    print(f"\n📄 Resultados guardados en: {archivo_salida}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python run_experimentos.py <nombre_archivo>")
        return

    nombre_archivo = sys.argv[1]
    ruta_archivo = os.path.join("recursos", nombre_archivo)

    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return

    print(f"\n🧪 Evaluando tablero: {nombre_archivo}\n")

    resultados = []
    resultados.append(evaluar(BacktrackingPlayer(), "Backtracking", ruta_archivo))
    resultados.append(evaluar(GreedyPlayer(), "Greedy", ruta_archivo))
    resultados.append(evaluar(CSPPlayer(), "CSP", ruta_archivo))

    guardar_csv(nombre_tablero=nombre_archivo.replace(".txt", ""), resultados=resultados)

if __name__ == "__main__":
    main()