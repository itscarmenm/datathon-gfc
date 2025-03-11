# query_handler.py - Consultas a los datos
import pandas as pd

def obtener_medicacion(dataframes, paciente_id):
    df = dataframes["medicacion"]
    medicacion = df[df["PacienteID"] == paciente_id]
    if medicacion.empty:
        return "No se encontraron datos de medicación para este paciente."
    return medicacion.to_string(index=False)

def obtener_laboratorio(dataframes, paciente_id):
    df = dataframes["lab"]
    lab = df[df["PacienteID"] == paciente_id]
    if lab.empty:
        return "No hay resultados de laboratorio para este paciente."
    return lab.to_string(index=False)

def obtener_procedimientos(dataframes, paciente_id):
    df = dataframes["procedimientos"]
    proc = df[df["PacienteID"] == paciente_id]
    if proc.empty:
        return "No hay procedimientos registrados para este paciente."
    return proc.to_string(index=False)

def obtener_notas(dataframes, paciente_id):
    df = dataframes["notas"]
    notas = df[df["PacienteID"] == paciente_id]
    if notas.empty:
        return "No hay notas médicas para este paciente."
    return notas.to_string(index=False)

def obtener_evolucion(dataframes, paciente_id):
    df = dataframes["evolucion"]
    evolucion = df[df["PacienteID"] == paciente_id]
    if evolucion.empty:
        return "No hay registros de evolución para este paciente."
    return evolucion.to_string(index=False)

def obtener_temperatura(dataframes, paciente_id, fecha, hora=None):
    df = dataframes["notas"]  # Suponiendo que las temperaturas están en las notas

    # Filtramos por el paciente y la fecha
    registros = df[(df["PacienteID"] == paciente_id) & (df["Fecha"] == str(fecha))]
    
    if registros.empty:
        return "No se encontraron registros de temperatura para este paciente en esa fecha."

    # Si se proporciona hora, buscamos registros más específicos
    if hora:
        registros = registros[registros["Hora"] == hora]

    if registros.empty:
        return f"No se encontraron registros de temperatura a las {hora}."

    # Devolvemos el registro de temperatura
    return registros["Temperatura"].to_string(index=False)
