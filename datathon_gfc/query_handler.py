import pandas as pd

def obtener_medicacion(dataframes, paciente_id):
    df = dataframes["medicacion"]
    medicacion = df[df["PacienteID"] == paciente_id]
    return medicacion if not medicacion.empty else None

def obtener_laboratorio(dataframes, paciente_id):
    df = dataframes["lab"]
    lab = df[df["PacienteID"] == paciente_id]
    return lab.to_string(index=False) if not lab.empty else "No hay resultados de laboratorio."

def obtener_procedimientos(dataframes, paciente_id):
    df = dataframes["procedimientos"]
    proc = df[df["PacienteID"] == paciente_id]
    return proc.to_string(index=False) if not proc.empty else "No hay procedimientos registrados."

def obtener_notas(dataframes, paciente_id):
    df = dataframes["notas"]
    notas = df[df["PacienteID"] == paciente_id]
    return notas.to_string(index=False) if not notas.empty else "No hay notas médicas."

def obtener_evolucion(dataframes, paciente_id):
    df = dataframes["evolucion"]
    evolucion = df[df["PacienteID"] == paciente_id]
    return evolucion.to_string(index=False) if not evolucion.empty else "No hay registros de evolución."

def obtener_temperatura(dataframes, paciente_id, fecha, hora=None):
    df = dataframes["notas"]  # Suponiendo que las temperaturas están en las notas
    registros = df[(df["PacienteID"] == paciente_id) & (df["Fecha"] == str(fecha))]

    if registros.empty:
        return "No se encontraron registros de temperatura."

    if hora:
        registros = registros[registros["Hora"] == hora]
    
    return registros["Temperatura"].to_string(index=False) if not registros.empty else "No hay registros de temperatura a esa hora."
