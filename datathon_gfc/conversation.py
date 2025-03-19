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
import matplotlib
matplotlib.use("Agg")  # Evita problemas con hilos secundarios
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import pandas as pd
from sklearn.preprocessing import MinMaxScaler  # Para normalizar los valores
from sklearn.preprocessing import StandardScaler
import matplotlib.ticker as ticker


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
        if "grafica" in pregunta or "gráfico" in pregunta:  # Si el usuario pidió un gráfico
            return generar_grafico_laboratorio(dataframes, paciente_id)
        
        datos_lab = obtener_datos_paciente_lab(dataframes, paciente_id)
        if datos_lab:
            contexto_ia = f"Los valores de laboratorio iniciales del paciente {nombre_paciente} son:\n{datos_lab}\n\nExplica brevemente qué indican estos valores y si presentan alguna anomalía."
            respuesta = obtener_respuesta_api(contexto_ia)
        else:
            respuesta = "No se encontraron resultados de laboratorio para este paciente."

    elif categoria == "procedimientos":
        respuesta = obtener_procedimientos(dataframes, paciente_id)

    elif categoria == "notas":
        datos_notas = obtener_datos_paciente_notas(dataframes, paciente_id, fecha)

        if datos_notas:
            if fecha:
                contexto_ia = f"Las notas médicas del paciente {nombre_paciente} el día {fecha} son:\n{datos_notas}\n\nResume la información de este día en un párrafo claro y conciso."
            else:
                contexto_ia = f"A continuación se presentan las notas médicas del paciente {nombre_paciente} a lo largo de su estancia:\n{datos_notas}\n\nGenera un resumen explicativo destacando los cambios en su estado y los eventos importantes."

            respuesta = obtener_respuesta_api(contexto_ia)
        else:
            respuesta = f"No hay notas registradas para {nombre_paciente}" + (f" el {fecha}" if fecha else "") + "."

    elif categoria == "evolucion_resumen": # Usamos la nueva categoría

        if "grafica" in pregunta or "gráfico" in pregunta:  # Si el usuario pidió un gráfico
            return generar_grafico_evolucion(dataframes, paciente_id)

        datos_evolucion = obtener_datos_paciente_evolucion(dataframes, paciente_id)
        if datos_evolucion:
            contexto_ia = f"Analiza los siguientes datos de evolución del paciente {nombre_paciente}:\n{datos_evolucion}\n\nProporciona un resumen conciso del estado del paciente y justifica tu análisis basándote en los datos proporcionados."
            respuesta = obtener_respuesta_api(contexto_ia)
        else:
            respuesta = "No se encontraron datos de evolución para generar un resumen del paciente."


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
    """Busca el ID del paciente sin importar mayúsculas, tildes o espacios."""
    nombre_ingresado = normalizar_nombre(nombre_ingresado)

    for nombre, id_paciente in pacientes_dict.items():
        if normalizar_nombre(nombre) == nombre_ingresado:
            return id_paciente

    return None  # No encontrado

def obtener_nombre_paciente_por_id(paciente_id, pacientes_dict):
    """Obtiene el nombre original del paciente a partir de su ID."""
    for nombre, id_paciente in pacientes_dict.items():
        if id_paciente == paciente_id:
            return nombre  # Devuelve el nombre original sin normalizar
    return None

def generar_grafico_laboratorio(dataframes, paciente_id):
    """Genera un gráfico de barras con valores de laboratorio escalados para mejor visualización."""
    df_lab = dataframes.get("lab", None)

    if df_lab is None or df_lab.empty:
        return "No hay datos de laboratorio disponibles para este paciente."

    # Filtrar los datos del paciente
    df_paciente = df_lab[df_lab["PacienteID"] == paciente_id].drop(columns=["PacienteID"])
    
    if df_paciente.empty:
        return "Este paciente no tiene registros de laboratorio."

    # Promediar los valores si hay varias filas
    valores_medios = df_paciente.mean()

    # Crear gráfico de barras
    fig, ax = plt.subplots(figsize=(5, 3))
    valores_medios.plot(kind="bar", ax=ax, color="skyblue", edgecolor="black")

    ax.set_xlabel("Parámetro", fontsize=8)
    ax.set_ylabel("Valor Normalizado", fontsize=8)
    ax.set_title("Valores de Laboratorio", fontsize=10)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()

    return MatplotlibChart(fig, expand=False)

def generar_grafico_evolucion(dataframes, paciente_id):
    """Genera un gráfico de barras agrupadas con la evolución del paciente."""
    df_evolucion = dataframes.get("evolucion", None)
    
    if df_evolucion is None or df_evolucion.empty:
        return "No hay datos de evolución disponibles para este paciente."
    
    # Filtrar por paciente y seleccionar las columnas relevantes
    df_paciente = df_evolucion[df_evolucion["PacienteID"] == paciente_id]
    columnas_interes = ["Fecha", "PresionSistolica", "PresionDiastolica", "FrecuenciaCardiaca",
                        "Temperatura", "FrecuenciaRespiratoria", "SaturacionOxigeno", "Glucosa"]
    df_paciente = df_paciente[columnas_interes]
    
    if df_paciente.empty:
        return "Este paciente no tiene registros de evolución."
    
    df_paciente.set_index("Fecha", inplace=True)
    df_paciente.sort_index(inplace=True)

    # Crear gráfico con barras más anchas y separadas
    fig, ax = plt.subplots(figsize=(12, 6))  # Aumentamos el tamaño del gráfico
    df_paciente.plot(kind="bar", ax=ax, edgecolor="black", colormap="tab10", width=0.7)

    ax.set_xlabel("Fecha", fontsize=10)
    ax.set_ylabel("Valor", fontsize=10)
    ax.set_title("Evolución de Parámetros Clínicos", fontsize=12)
    
    # Reducir la cantidad de fechas mostradas en el eje X para que no se amontonen
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=8))  # Máximo 8 etiquetas en X
    ax.tick_params(axis="x", rotation=45, labelsize=9, pad=5)
    ax.tick_params(axis="y", labelsize=9)
    
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Mover la leyenda fuera de la gráfica
    ax.legend(title="Parámetros", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()

    return MatplotlibChart(fig, expand=False)