#`conversation.py`: Interpreta la pregunta y genera una respuesta.

import spacy
import re
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
    "medicacion": ["medicacion", "medicación", "medicinas", "fármacos", "tratamiento", "receta"],
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
    categoria = detectar_categoria(pregunta)
    fecha, hora = extraer_fecha_hora(pregunta)
    nombre_paciente = obtener_nombre_paciente_por_id(paciente_id, pacientes_dict)

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

def formatear_medicacion(df_medicacion):
    """Genera un resumen narrativo de la medicación del paciente."""
    if df_medicacion.empty:
        return "No hay medicación registrada para este paciente."

    # Empezamos el resumen con una introducción.
    resumen = "El paciente está tomando la siguiente medicación: "

    # Agregamos los medicamentos en formato narrativo
    tratamientos = []
    for _, row in df_medicacion.iterrows():
        # Formato más narrativo
        tratamiento = f"{row['Medicamento']} de {row['Dosis']} mg, administrado por vía {row['Via']}"
        tratamientos.append(tratamiento)

    # Usamos 'y' para unir el último medicamento con los anteriores, si hay más de uno
    if len(tratamientos) > 1:
        resumen += ", y ".join(tratamientos[:-1]) + " y " + tratamientos[-1] + "."
    else:
        resumen += tratamientos[0] + "."

    return resumen

def obtener_nombre_paciente_por_id(paciente_id, pacientes_dict):
    """Obtiene el nombre del paciente a partir del ID."""
    for nombre, id_paciente in pacientes_dict.items():
        if id_paciente == paciente_id:
            return nombre.title() # Devolver el nombre con la primera letra en mayúscula
    return "Paciente Desconocido"