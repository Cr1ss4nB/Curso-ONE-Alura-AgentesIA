from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY, COHERE_API_KEY
from langchain_core.globals import set_debug
from langsmith import Client
from langchain_classic.agents import create_react_agent, Tool
from herramienta_analisis_imagen import HerramientaAnalisisImagen

set_debug(False)

class AgenteOrquestador:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=GEMINI_FLASH
        )
        
        herramienta_analisis_imagen = HerramientaAnalisisImagen()
        
        self.tools = [
            Tool(
                name = herramienta_analisis_imagen.name,
                func = herramienta_analisis_imagen.run,
                description = herramienta_analisis_imagen.description,
                return_direct = herramienta_analisis_imagen.return_direct
            )
        ]
        
        # Inicializa el cliente oficial y descarga con el flag de seguridad nativo
        client = Client()
        prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

        
        self.agente = create_react_agent(self.llm, self.tools,prompt)