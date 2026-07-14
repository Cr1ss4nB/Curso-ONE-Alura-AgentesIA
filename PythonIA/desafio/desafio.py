# Etapa 1: Leer el archivo de reviews

import json
from llamada_a_llm import recibe_linea_devuelve_json

lista_de_reviews = []

with open('reviewsChatGPT.txt', 'r', encoding='utf-8') as archivo:
    for linea in archivo:
        lista_de_reviews.append(linea.strip())

    # print(lista_de_reviews[2])

# Etapa 2 y 3: Mandar al modelo de IA la review en formato JSON donde habrá usuario, reseña original, reseña_es y evaluación (positiva, negativa o neutra)

lista_de_reviews_json = []

for review in lista_de_reviews:
    review_json = recibe_linea_devuelve_json(review)
    review_dic = json.loads(review_json)
    lista_de_reviews_json.append(review_dic)

print(lista_de_reviews_json)

# Etapa 4: Función que dada la lista de diccionarios retorne la cantidad de reseñas positivas, negativas y neutras.

def contador_y_juntador(lista_de_diccionarios):
    contador_positivas = 0
    contador_negativas = 0
    contador_neutras = 0

    for diccionario in lista_de_diccionarios:
        if diccionario['evaluacion'] == 'Positiva':
            contador_positivas += 1
        elif diccionario['evaluacion'] == 'Negativa':
            contador_negativas += 1
        else:
            contador_neutras += 1
        
    lista_de_diccionarios_str = [str(diccionario) for diccionario in lista_de_diccionarios]
    textos_unidos = "####".join(lista_de_diccionarios_str)

    return contador_positivas, contador_negativas, contador_neutras, textos_unidos

pos, neg, neut, textos = contador_y_juntador(lista_de_reviews_json)

print(f"Positivas: {pos}")
print(f"Negativas: {neg}")
print(f"Neutras: {neut}")
print("--------------------------------")
print(textos)