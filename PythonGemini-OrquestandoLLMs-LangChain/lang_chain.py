from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY, COHERE_API_KEY
from my_helper import encode_image

llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model=GEMINI_FLASH
)

respuesta = llm.invoke("Cuáles canales colombianos de youtube me recomiendas para saber más sobre teléfonos inteligentes?")
contenido_limpio = respuesta.content[0]['text'] if isinstance(respuesta.content, list) else respuesta.content
print("Gemini: ", contenido_limpio)


llm = ChatCohere(
    cohere_api_key=COHERE_API_KEY
)

respuesta = llm.invoke([HumanMessage(content="Cuáles canales colombianos de youtube me recomiendas para saber más sobre teléfonos inteligentes?")])

print(f"Cohere: ",respuesta.content)


# imagen = encode_image('datos/ejemplo_grafico.jpg')

# pregunta = "Describe la imagen:"

# mensaje = HumanMessage(
#     content = [
#         {
#             "type": "text",
#             "text": pregunta
#         },
#         {
#             "type": "image_url",
#             "image_url": f"data:image/jpeg;base64,{imagen}"
#         }
#     ]
# )

# respuesta = llm.invoke([mensaje])
# print(respuesta)