#- `query_handler.py`: Busca en los datos según la pregunta del usuario.
import pandas as pd
import spacy
from api_client import obtener_respuesta_api  # Importa la función de la API

nlp = spacy.load("es_core_news_sm")

def generar_resumen_spacy(notas_paciente):
    """Genera un resumen útil de las notas médicas de un paciente usando palabras clave."""
    if not notas_paciente:
        return None  # Devuelve None si no hay notas

    texto_completo = " ".join(notas_paciente)
    doc = nlp(texto_completo)

    palabras_sintomas = ["fiebre", "dolor", "cansancio", "mareo"]
    palabras_diagnostico = ["diabetes", "hipertensión", "infección", "asma"]
    palabras_tratamiento = ["paracetamol", "ibuprofeno", "reposo", "fisioterapia"]

    sintomas = [token.text for token in doc if token.text.lower() in palabras_sintomas]
    diagnosticos = [token.text for token in doc if token.text.lower() in palabras_diagnostico]
    tratamientos = [token.text for token in doc if token.text.lower() in palabras_tratamiento]

    resumen_spacy = ""
    if sintomas:
        resumen_spacy += f"- **Síntomas reportados:** {', '.join(set(sintomas))}\n"
    if diagnosticos:
        resumen_spacy += f"- **Diagnósticos:** {', '.join(set(diagnosticos))}\n"
    if tratamientos:
        resumen_spacy += f"- **Tratamientos indicados:** {', '.join(set(tratamientos))}\n"

    if not resumen_spacy:
        return None

    return resumen_spacy

def obtener_notas(dataframes, paciente_id):
    df = dataframes["notas"]
    notas_paciente = df[df["PacienteID"] == paciente_id]["Nota"].tolist()

    resumen_spacy = generar_resumen_spacy(notas_paciente)

    if resumen_spacy:
        pregunta_medico = "¿Cuáles son sus notas clínicas?" # Reconstruimos la pregunta original
        contexto_ia = f"El médico preguntó: '{pregunta_medico}'. Basado en las siguientes notas clínicas resumidas:\n{resumen_spacy}\n\nProporciona un resumen redactado y coherente de las notas clínicas del paciente."
        return obtener_respuesta_api(contexto_ia)
    else:
        return "No hay notas médicas registradas."

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

def obtener_datos_paciente_lab(dataframes, paciente_id):
    """Obtiene todos los datos de laboratorio iniciales de un paciente."""
    df = dataframes.get("lab")
    if df is not None and not df.empty:
        datos_paciente = df[df["PacienteID"] == paciente_id]
        if not datos_paciente.empty:
            return datos_paciente.to_string(index=False)
    return None

def obtener_datos_paciente_notas(dataframes, paciente_id, fecha=None):
    """Obtiene todas las notas de un paciente, filtradas por fecha si se proporciona."""
    df = dataframes.get("notas")
    
    if df is None or df.empty:
        return None

    # Filtrar por PacienteID
    df_paciente = df[df["PacienteID"] == paciente_id]

    # Si se proporciona fecha, filtrar también por fecha específica
    if fecha:
        df_paciente = df_paciente[df_paciente["Fecha"] == fecha]

    # Si después del filtrado no hay datos, devolver None
    if df_paciente.empty:
        return None

    # Ordenar por fecha (asumiendo que la columna 'Fecha' tiene formato adecuado)
    df_paciente = df_paciente.sort_values(by="Fecha")

    # Unir notas en un solo string
    notas = "\n".join(f"{row['Fecha']}: {row['Nota']}" for _, row in df_paciente.iterrows())
    
    return notas


def obtener_datos_paciente_evolucion(dataframes, paciente_id):
    """Obtiene todos los datos de evolución de un paciente."""
    df = dataframes.get("evolucion")
    if df is not None and not df.empty:
        datos_paciente = df[df["PacienteID"] == paciente_id]
        if not datos_paciente.empty:
            return datos_paciente.to_string(index=False)
    return None