import spacy
import re
from datetime import datetime
from query_handler import (
    obtener_medicacion, obtener_laboratorio, obtener_procedimientos, 
    obtener_notas, obtener_evolucion, obtener_temperatura
)
from utils import normalizar_texto, extraer_palabras_clave, extraer_fecha_hora

nlp = spacy.load("es_core_news_sm")
memoria = []  # Lista para almacenar la conversación

SINONIMOS = {
    "medicacion": ["medicacion", "medicación", "medicinas", "fármacos", "tratamiento", "receta"],
    "laboratorio": ["laboratorio", "análisis", "pruebas", "exámenes"],
    "procedimientos": ["procedimientos", "intervenciones", "cirugías", "operaciones"],
    "notas": ["notas", "historial", "registros", "comentarios"],
    "evolucion": ["evolución", "estado", "seguimiento", "progreso"],
    "temperatura": ["temperatura", "fiebre", "calor", "termómetro"]
}

def responder_pregunta(pregunta, paciente_id, dataframes):
    pregunta = normalizar_texto(pregunta)
    categoria = detectar_categoria(pregunta)
    fecha, hora = extraer_fecha_hora(pregunta)

    respuesta = "No tengo información sobre eso."

    if categoria == "medicacion":
        datos_medicacion = obtener_medicacion(dataframes, paciente_id)
        if datos_medicacion is not None:  # Verifica que no sea None
            respuesta = formatear_medicacion(datos_medicacion)
        else:
            respuesta = "No hay información de medicación para este paciente."

    elif categoria == "laboratorio":
        respuesta = obtener_laboratorio(dataframes, paciente_id)

    elif categoria == "procedimientos":
        respuesta = obtener_procedimientos(dataframes, paciente_id)

    elif categoria == "notas":
        respuesta = obtener_notas(dataframes, paciente_id)

    elif categoria == "evolucion":
        respuesta = obtener_evolucion(dataframes, paciente_id)

    elif categoria == "temperatura":
        if fecha:
            respuesta = obtener_temperatura(dataframes, paciente_id, fecha, hora)
        else:
            respuesta = "Por favor, indica una fecha para buscar la temperatura."

    memoria.append({"pregunta": pregunta, "respuesta": respuesta})  # Guardar en memoria
    return respuesta

def detectar_categoria(pregunta):
    pregunta = normalizar_texto(pregunta)
    palabras_clave = extraer_palabras_clave(pregunta)

    for categoria, palabras in SINONIMOS.items():
        if any(palabra in palabras_clave for palabra in palabras):
            return categoria
    return None

def formatear_medicacion(df_medicacion):
    tratamientos = []
    for _, row in df_medicacion.iterrows():
        tratamiento = f"{row['Medicamento']} {row['Dosis']} mg por {row['Via']}"
        tratamientos.append(tratamiento)
    
    return "; ".join(tratamientos)
