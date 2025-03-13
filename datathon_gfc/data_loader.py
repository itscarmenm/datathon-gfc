import pandas as pd

def cargar_datos():
    file_paths = {
        "medicacion": "csvs/resumen_medicacion.csv",
        "lab": "csvs/resumen_lab_iniciales.csv",
        "notas": "csvs/resumen_notas.csv",
        "pacientes": "csvs/resumen_pacientes.csv",
        "procedimientos": "csvs/resumen_procedimientos.csv",
        "evolucion": "csvs/resumen_evolucion.csv"
    }
    
    dataframes = {}
    pacientes_dict = {}  # Diccionario para mapear nombres a IDs

    for key, path in file_paths.items():
        try:
            df = pd.read_csv(path, encoding="utf-8", on_bad_lines="skip")
            df.columns = df.columns.str.strip()
            dataframes[key] = df

            # Guardamos la relación Nombre - PacienteID si es el CSV de pacientes
            if key == "pacientes":
                for _, row in df.iterrows():
                    nombre = row["Nombre"].strip().lower()  # Normalizamos el nombre
                    pacientes_dict[nombre] = row["PacienteID"]

        except Exception as e:
            print(f"Error al cargar {key}: {e}")

    print("Datos cargados correctamente.")
    return dataframes, pacientes_dict
