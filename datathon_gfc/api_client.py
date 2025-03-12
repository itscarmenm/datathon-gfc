import openai

# Aquí debes colocar tu propia API Key
openai.api_key = "sk-8BMaX7HOyMAcqcZdnjY7IQ"  # Cambia esto por tu API Key real

def obtener_respuesta_api(pregunta):
    # Aquí haces la llamada a la API con el mensaje de la pregunta
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # O el modelo que quieras usar
        prompt=pregunta,
        max_tokens=150
    )
    return response.choices[0].text.strip()  # Devuelve la respuesta generada
