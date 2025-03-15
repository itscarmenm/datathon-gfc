import pandas as pd
import spacy

nlp = spacy.load("es_core_news_sm")

def generar_resumen_spacy(notas_paciente):
    """Genera un resumen útil de las notas médicas de un paciente usando palabras clave en lugar de entidades de spaCy."""
    if not notas_paciente:
        return "No hay notas médicas registradas."

    texto_completo = " ".join(notas_paciente)
    doc = nlp(texto_completo)

    # Listas de palabras clave (puedes ampliarlas)
    palabras_sintomas = ["fiebre", "dolor", "cansancio", "mareo"]
    palabras_diagnostico = ["diabetes", "hipertensión", "infección", "asma"]
    palabras_tratamiento = ["paracetamol", "ibuprofeno", "reposo", "fisioterapia"]

    sintomas = [token.text for token in doc if token.text.lower() in palabras_sintomas]
    diagnosticos = [token.text for token in doc if token.text.lower() in palabras_diagnostico]
    tratamientos = [token.text for token in doc if token.text.lower() in palabras_tratamiento]

    resumen = "Resumen de notas médicas:\n"
    if sintomas:
        resumen += f"- **Síntomas reportados:** {', '.join(set(sintomas))}\n"
    if diagnosticos:
        resumen += f"- **Diagnósticos:** {', '.join(set(diagnosticos))}\n"
    if tratamientos:
        resumen += f"- **Tratamientos indicados:** {', '.join(set(tratamientos))}\n"

    if not (sintomas or diagnosticos or tratamientos):
        resumen += "No se encontraron detalles específicos en las notas."

    return resumen


def obtener_notas(dataframes, paciente_id):
    df = dataframes["notas"]
    notas_paciente = df[df["PacienteID"] == paciente_id]["Nota"].tolist()
    
    return generar_resumen_spacy(notas_paciente) if notas_paciente else "No hay notas médicas registradas."


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

def obtener_resumen_medicacion(dataframes, paciente_id):
    medicacion = obtener_medicacion(dataframes, paciente_id)
    
    if medicacion is None or medicacion.empty:
        return "No hay medicación registrada para este paciente."
    
    lista_medicacion = [
        f"{fila['Medicamento']} ({fila['Dosis']} mg), vía {fila['Via']}"
        for _, fila in medicacion.iterrows()
    ]

    resumen = "El paciente está recibiendo la siguiente medicación: " + "; ".join(lista_medicacion) + "."
    return resumen
