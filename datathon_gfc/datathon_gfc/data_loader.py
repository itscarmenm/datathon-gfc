# data_loader.py - Cargar datos desde CSV
import pandas as pd

def cargar_datos():
    file_paths = {
        "medicacion": "resumen_medicacion.csv",
        "lab": "resumen_lab_iniciales.csv",
        "notas": "resumen_notas.csv",
        "pacientes": "resumen_pacientes.csv",
        "procedimientos": "resumen_procedimientos.csv",
        "evolucion": "resumen_evolucion.csv"
    }
    
    dataframes = {}
    for key, path in file_paths.items():
        try:
            df = pd.read_csv(path, encoding="utf-8", on_bad_lines="skip")
            df.columns = df.columns.str.strip()
            dataframes[key] = df
        except Exception as e:
            print(f"Error al cargar {key}: {e}")
    
    print("Datos cargados correctamente.")
    return dataframes
