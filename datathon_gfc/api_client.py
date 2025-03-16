#- `api_client.py`: conecta con la API


import openai

client = openai.OpenAI(
    api_key="sk-8BMaX7HOyMAcqcZdnjY7IQ",
    base_url="https://litellm.dccp.pbu.dedalus.com") # set proxy to base_url

def obtener_respuesta_api(contexto):
    """Envía la información a la API para obtener una respuesta más natural y explicativa."""
    response = client.chat.completions.create(
        model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=[
            {"role": "user", "content": contexto}
        ]
    )
    return response.choices[0].message.content