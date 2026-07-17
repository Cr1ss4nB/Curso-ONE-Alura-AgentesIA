from pydantic import BaseModel, Field
from typing import List

class DetallesImagen(BaseModel):
    titulo: str = Field(
        description = "Define el título adecuado para la imagen analizada."
    )
    descripcion: str = Field(
        description = "Coloca aquí una descripción detallada del análisis de la imagen."
    )
    etiquetas: List[str] = Field(
        description = "Define tres palabras clave para la imagen analizada."
    )