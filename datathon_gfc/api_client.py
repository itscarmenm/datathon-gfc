import openai

# Configuración del cliente OpenAI con el proxy LiteLLM
client = openai.OpenAI(
    api_key="sk-8BMaX7HOyMAcqcZdnjY7IQ",
    base_url="https://litellm.dccp.pbu.dedalus.com") # set proxy to base_url

def consultar_api(pregunta, contexto=""):
    """
    Envía la pregunta a la API junto con un contexto opcional.

    :param pregunta: Texto de la consulta del usuario.
    :param contexto: Información adicional que puede ayudar a generar una mejor respuesta.
    :return: Respuesta generada por la API.
    """
    mensajes = [{"role": "user", "content": f"{contexto}\n\n{pregunta}"}]

    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=mensajes
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"Error al consultar la API: {e}")
        return "No se pudo obtener respuesta en este momento."
