import pandas as pd
# import openai

# Configuración de la API (pero no la usamos todavía)
# API_KEY = "VirtualAPIKey"
# BASE_URL = "https://litellm.dccp.pbu.dedalus.com"
# client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Cargar datos CSV con manejo de errores y limpieza
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
            df.columns = df.columns.str.strip()  # Limpiar nombres de columnas
            dataframes[key] = df
        except Exception as e:
            print(f"Error al cargar {key}: {e}")
    
    print("Datos cargados correctamente.")
    return dataframes

dataframes = cargar_datos()
memoria = []  # Lista para almacenar la conversación

# Funciones para obtener datos
def obtener_medicacion(paciente_id):
    df = dataframes["medicacion"]
    medicacion = df[df["PacienteID"] == paciente_id]
    if medicacion.empty:
        return "No se encontraron datos de medicación para este paciente."
    return medicacion.to_string(index=False)

def obtener_laboratorio(paciente_id):
    df = dataframes["lab"]
    lab = df[df["PacienteID"] == paciente_id]
    if lab.empty:
        return "No hay resultados de laboratorio para este paciente."
    return lab.to_string(index=False)

def obtener_procedimientos(paciente_id):
    df = dataframes["procedimientos"]
    proc = df[df["PacienteID"] == paciente_id]
    if proc.empty:
        return "No hay procedimientos registrados para este paciente."
    return proc.to_string(index=False)

def obtener_notas(paciente_id):
    df = dataframes["notas"]
    notas = df[df["PacienteID"] == paciente_id]
    if notas.empty:
        return "No hay notas médicas para este paciente."
    return notas.to_string(index=False)

def obtener_evolucion(paciente_id):
    df = dataframes["evolucion"]
    evolucion = df[df["PacienteID"] == paciente_id]
    if evolucion.empty:
        return "No hay registros de evolución para este paciente."
    return evolucion.to_string(index=False)

# Función para manejar la conversación
def responder_pregunta(pregunta, paciente_id):
    pregunta = pregunta.lower()
    if "medicación" in pregunta:
        respuesta = obtener_medicacion(paciente_id)
    elif "laboratorio" in pregunta:
        respuesta = obtener_laboratorio(paciente_id)
    elif "procedimientos" in pregunta:
        respuesta = obtener_procedimientos(paciente_id)
    elif "notas" in pregunta:
        respuesta = obtener_notas(paciente_id)
    elif "evolución" in pregunta or "evolucion" in pregunta:
        respuesta = obtener_evolucion(paciente_id)
    else:
        respuesta = "No tengo información sobre eso."
    
    memoria.append({"pregunta": pregunta, "respuesta": respuesta})  # Guardar en memoria
    return respuesta

# Bucle de interacción
while True:
    pregunta = input("Médico: ")
    if pregunta.lower() == "salir":
        break
    
    paciente_id = int(input("Ingrese ID del paciente: "))
    respuesta = responder_pregunta(pregunta, paciente_id)
    print(f"Asistente IA: {respuesta}")