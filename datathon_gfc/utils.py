import unicodedata
import re
import spacy
from datetime import datetime

nlp = spacy.load("es_core_news_sm")

def normalizar_texto(texto):
    """Convierte texto a minúsculas, elimina tildes y caracteres especiales."""
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def limpiar_texto(texto):
    """Elimina caracteres especiales y espacios adicionales."""
    return re.sub(r'[^\w\s]', '', texto).strip()

def formatear_respuesta(texto):
    """Formatea la respuesta para mejor presentación."""
    return f"\n---\n{texto}\n---\n"

def extraer_palabras_clave(texto):
    """Extrae palabras clave eliminando palabras comunes y usando spaCy."""
    texto = normalizar_texto(texto)  # Normalizamos el texto antes de extraer palabras clave
    doc = nlp(texto)
    palabras_importantes = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return palabras_importantes

def extraer_fecha_hora(texto):
    """Extrae fecha y hora de la pregunta si están presentes."""
    # Formatos de fecha comunes (dd/mm/yyyy, dd-mm-yyyy)
    fecha_regex = r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
    hora_regex = r"(\d{1,2}:\d{2}(:\d{2})?)"

    fecha = None
    hora = None

    # Buscar fecha y hora en el texto
    match_fecha = re.search(fecha_regex, texto)
    match_hora = re.search(hora_regex, texto)

    if match_fecha:
        fecha = match_fecha.group(1)  # Obtener la fecha detectada

    if match_hora:
        hora = match_hora.group(1)  # Obtener la hora detectada

    # Si no se encuentra una fecha, tomamos la fecha actual
    if fecha:
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y").date()  # Convierte la fecha a formato datetime
        except ValueError:
            fecha = None

    return fecha, hora
