#`conversation.py`: Interpreta la pregunta y genera una respuesta.

import spacy
import re
import unicodedata
from datetime import datetime
from query_handler import (
    obtener_medicacion, obtener_laboratorio, obtener_procedimientos,
    obtener_notas, obtener_evolucion, obtener_temperatura,
    obtener_datos_paciente_evolucion, obtener_datos_paciente_lab, obtener_datos_paciente_notas
)
from utils import normalizar_texto, extraer_palabras_clave, extraer_fecha_hora
from api_client import obtener_respuesta_api

nlp = spacy.load("es_core_news_sm")
memoria = []  # Lista para almacenar la conversación

SINONIMOS = {
    "medicacion": ["medicacion", "medicación", "medicinas", "fármacos", "tratamiento", "receta", "medicaciones", "medicamentos"],
    "laboratorio": ["laboratorio", "análisis", "pruebas", "exámenes", "laboratorios iniciales", "lab"],
    "procedimientos": ["procedimientos", "intervenciones", "cirugías", "operaciones"],
    "notas": ["nota", "notas", "historial", "registros", "comentarios", "notas clínicas", "clínica", "anotaciones", "clinica"], 
    "evolucion_resumen": ["como esta paciente", "cual evolucion", "hazme resumen estado",
                          "resumen evolucion", "estado evolucion", "evolucion paciente", "resumen paciente",
                          "evolucion", "resumen", "estado",
                          "resumen completo", "paciente completo", "estado general",
                          "resumen general", "informacion paciente"],
    "temperatura": ["temperatura", "fiebre", "calor", "termómetro"]
}

# ... (resto del archivo conversation.py sin cambios)
def responder_pregunta(pregunta, paciente_id, dataframes, pacientes_dict):
    pregunta = normalizar_texto(pregunta)

    if isinstance(paciente_id, str):  
        paciente_id = obtener_id_paciente_por_nombre(paciente_id, pacientes_dict)
    
    if paciente_id is None:
        return "No se encontró el paciente en la base de datos."

    categoria = detectar_categoria(pregunta)
    fecha, hora = extraer_fecha_hora(pregunta)
    nombre_paciente = obtener_nombre_paciente_por_id(paciente_id, pacientes_dict)

    respuesta = "No tengo información sobre eso."


    if categoria == "medicacion":
        datos_medicacion = obtener_medicacion(dataframes, paciente_id)
        if datos_medicacion is not None:  # Verifica que no sea None
            contexto_ia = f"El paciente {nombre_paciente} tiene la siguiente medicación registrada:\n{datos_medicacion}\n\nGenera un resumen narrativo explicando qué medicamentos toma y para qué podrían servir."
            respuesta = obtener_respuesta_api(contexto_ia)
        else:
            respuesta = "No hay información de medicación para este paciente."

    elif categoria == "laboratorio":
        datos_lab = obtener_datos_paciente_lab(dataframes, paciente_id)
        if datos_lab:
            contexto_ia = f"Los valores de laboratorio iniciales del paciente {nombre_paciente} son:\n{datos_lab}\n\nExplica brevemente qué indican estos valores y si presentan alguna anomalía."
            respuesta = obtener_respuesta_api(contexto_ia)
        else:
            respuesta = "No se encontraron resultados de laboratorio para este paciente."

    elif categoria == "procedimientos":
        respuesta = obtener_procedimientos(dataframes, paciente_id)

    elif categoria == "notas":
        respuesta = obtener_notas(dataframes, paciente_id)

    elif categoria == "evolucion_resumen": # Usamos la nueva categoría
        datos_evolucion = obtener_datos_paciente_evolucion(dataframes, paciente_id)
        if datos_evolucion:
            contexto_ia = f"Analiza los siguientes datos de evolución del paciente {nombre_paciente}:\n{datos_evolucion}\n\nProporciona un resumen conciso del estado del paciente y justifica tu análisis basándote en los datos proporcionados."
            respuesta = obtener_respuesta_api(contexto_ia)
        else:
            respuesta = "No se encontraron datos de evolución para generar un resumen del paciente."

    elif categoria == "evolucion": # Mantener la funcionalidad anterior si la necesitas
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
        for palabra_sinonimo in palabras:
            if palabra_sinonimo in palabras_clave:
                return categoria
    return None


def normalizar_nombre(nombre):
    # Convertir a minúsculas y eliminar tildes
    nombre = nombre.lower()
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    return nombre.strip()

def obtener_id_paciente_por_nombre(nombre_ingresado, pacientes_dict):
    """Busca un paciente sin importar mayúsculas, minúsculas ni tildes."""
    nombre_ingresado = normalizar_nombre(nombre_ingresado)

    return pacientes_dict.get(nombre_ingresado, None)  # Retorna el ID o None si no lo encuentra

def obtener_nombre_paciente_por_id(paciente_id, nombres_originales):
    """Obtiene el nombre original del paciente a partir de su ID."""
    return nombres_originales.get(paciente_id)


