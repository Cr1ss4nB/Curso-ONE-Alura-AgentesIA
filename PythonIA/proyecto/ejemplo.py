from openai import OpenAI

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

respuesta_de_llm = client_openai.chat.completions.create(
    model="google/gemma-3-1b",
    messages = [
        {"role": "system", "content": "Eres un asistente de IA que responde todo en forma irónica"},
        {"role": "user", "content": "¿Qué es la IA generativa?"}
    ],
    temperature=0.7,
)

print(respuesta_de_llm.choices[0].message.content)