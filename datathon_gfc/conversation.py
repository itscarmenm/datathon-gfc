# conversation.py - Manejo de memoria y contexto
import spacy
import re
from datetime import datetime
from query_handler import obtener_medicacion, obtener_laboratorio, obtener_procedimientos, obtener_notas, obtener_evolucion, obtener_temperatura
from utils import normalizar_texto, extraer_palabras_clave

paciente_actual = None  # Almacena el último paciente consultado

nlp = spacy.load("es_core_news_sm")
memoria = []  # Lista para almacenar la conversación

def responder_pregunta(pregunta, paciente_id=None, dataframes=None):
    global paciente_actual

    # Si no se da un paciente ID, usamos el último registrado
    if paciente_id is None:
        if paciente_actual is None:
            return "Por favor, indica el ID del paciente la primera vez."
        paciente_id = paciente_actual
    else:
        paciente_actual = paciente_id  # Guardamos el último paciente usado

    pregunta = normalizar_texto(pregunta)
    categoria = detectar_categoria(pregunta)
    fecha, hora = extraer_fecha_hora(pregunta)

    if categoria == "medicacion":
        respuesta = obtener_medicacion(dataframes, paciente_id)
    elif categoria == "laboratorio":
        respuesta = obtener_laboratorio(dataframes, paciente_id)
    elif categoria == "procedimientos":
        respuesta = obtener_procedimientos(dataframes, paciente_id)
    elif categoria == "notas":
        respuesta = obtener_notas(dataframes, paciente_id)
    elif categoria == "evolucion":
        respuesta = obtener_evolucion(dataframes, paciente_id)
    elif "temperatura" in categoria:  # Verificar que se está pidiendo temperatura
        if fecha:
            respuesta = obtener_temperatura(dataframes, paciente_id, fecha, hora)
        else:
            respuesta = "Por favor, indica una fecha para buscar la temperatura."
    else:
        respuesta = "No tengo información sobre eso."

    return respuesta


def obtener_historial():
    return memoria

SINONIMOS = {
    "medicacion": ["medicacion", "medicación", "medicinas", "fármacos", "tratamiento", "receta"],
    "laboratorio": ["laboratorio", "análisis", "pruebas", "exámenes"],
    "procedimientos": ["procedimientos", "intervenciones", "cirugías", "operaciones"],
    "notas": ["notas", "historial", "registros", "comentarios"],
    "evolucion": ["evolución", "estado", "seguimiento", "progreso"],
    "temperatura": ["temperatura", "fiebre", "calor", "termómetro"]
}


def detectar_categoria(pregunta):
    """Determina la categoría basada en palabras clave y sinónimos."""
    pregunta = normalizar_texto(pregunta)
    palabras_clave = extraer_palabras_clave(pregunta)

    for categoria, palabras in SINONIMOS.items():
        if any(palabra in palabras_clave for palabra in palabras):
            return categoria
    return None

def extraer_fecha_hora(pregunta):
    """Busca una fecha y hora en la pregunta."""
    fecha = None
    hora = None

    # Buscar fechas en formato dd/mm/aaaa o aaaa-mm-dd
    fecha_match = re.search(r'(\d{2}/\d{2}/\d{4})|(\d{4}-\d{2}-\d{2})', pregunta)
    if fecha_match:
        fecha = fecha_match.group(0)
        fecha = datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d") if "/" in fecha else fecha

    # Buscar horas en formato hh:mm o hh:mm:ss
    hora_match = re.search(r'(\d{1,2}:\d{2}(:\d{2})?)', pregunta)
    if hora_match:
        hora = hora_match.group(0) + (":00" if len(hora_match.group(0)) == 5 else "")  # Asegurar hh:mm:ss

    return fecha, hora

def responder_pregunta(pregunta, paciente_id, dataframes):
    pregunta = normalizar_texto(pregunta)
    categoria = detectar_categoria(pregunta)
    fecha, hora = extraer_fecha_hora(pregunta)

    if categoria == "medicacion":
        respuesta = obtener_medicacion(dataframes, paciente_id)
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
    else:
        respuesta = "No tengo información sobre eso."

    return respuesta


