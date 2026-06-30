import numpy as np

# ==================== CADENA DE MARKOV PARA PREDICCIÓN DEL CLIMA ====================
"""
Una Cadena de Markov es un modelo matemático que predice eventos futuros basándose
ÚNICAMENTE en el estado actual, sin considerar el historial pasado.

Principio clave: "El futuro depende solo del presente, no del pasado"

Ejemplo: Si hoy está soleado, la probabilidad de que mañana llueva depende solo
del hecho de que HOY está soleado, no importa qué clima hubo hace 3 días.
"""


# ==================== DEFINICIÓN DE ESTADOS ====================
"""
Estados posibles del clima. Cada día solo puede estar en UNO de estos estados.
"""
estados = ["Soleado", "Nublado", "Lluvioso"]


# ==================== MATRIZ DE TRANSICIÓN ====================
"""
La matriz de transición define las PROBABILIDADES de pasar de un estado a otro.

Estructura:
           Hacia →  [Soleado, Nublado, Lluvioso]
    Desde Soleado:  [  0.8,    0.15,     0.05   ]  ← Fila 0
    Desde Nublado:  [  0.2,    0.6,      0.2    ]  ← Fila 1
    Desde Lluvioso: [  0.25,   0.25,     0.5    ]  ← Fila 2

Lectura de la matriz:
- Fila 0 (Soleado): Si HOY está soleado:
  • 80% de probabilidad de que MAÑANA esté soleado
  • 15% de probabilidad de que MAÑANA esté nublado
  • 5% de probabilidad de que MAÑANA esté lluvioso

- Fila 1 (Nublado): Si HOY está nublado:
  • 20% probabilidad → soleado mañana
  • 60% probabilidad → nublado mañana (se mantiene)
  • 20% probabilidad → lluvioso mañana

- Fila 2 (Lluvioso): Si HOY está lluvioso:
  • 25% probabilidad → soleado mañana
  • 25% probabilidad → nublado mañana
  • 50% probabilidad → lluvioso mañana (se mantiene)

REGLA IMPORTANTE: Cada fila DEBE sumar 1.0 (100%)
"""
matriz_transicion = [
    [0.8, 0.15, 0.05],  # Transiciones desde "Soleado"
    [0.2, 0.6, 0.2],  # Transiciones desde "Nublado"
    [0.25, 0.25, 0.5],  # Transiciones desde "Lluvioso"
]


# ==================== PARÁMETROS DE LA SIMULACIÓN ====================

# Estado del clima HOY (punto de partida)
estado_inicial = "Soleado"

# Cantidad de días que queremos predecir
numero_dias = 10


# ==================== FUNCIONES ====================


def obtener_indice_estado(estado):
    """
    Convierte el nombre de un estado (texto) a su índice numérico en la lista.

    Los índices son necesarios para acceder a la matriz de transición.

    Parámetros:
        estado (str): Nombre del estado ("Soleado", "Nublado", "Lluvioso")

    Retorna:
        int: Índice del estado (0, 1, o 2)

    Ejemplos:
        >>> obtener_indice_estado("Soleado")
        0
        >>> obtener_indice_estado("Nublado")
        1
        >>> obtener_indice_estado("Lluvioso")
        2
    """
    return estados.index(estado)


def predecir_clima(estado_inicial, numero_dias):
    """
    Predice el clima para los próximos días usando una Cadena de Markov.

    Algoritmo:
    1. Comenzamos con el estado inicial
    2. Para cada día:
       a. Miramos las probabilidades de transición del estado actual
       b. Elegimos aleatoriamente el siguiente estado según esas probabilidades
       c. El estado elegido se convierte en el estado actual para el próximo día
    3. Repetimos hasta completar todos los días

    Parámetros:
        estado_inicial (str): Estado del clima HOY
        numero_dias (int): Cantidad de días a predecir (incluyendo hoy)

    Retorna:
        list: Lista con los estados predichos para cada día

    Ejemplo:
        >>> predecir_clima("Soleado", 5)
        ['Soleado', 'Soleado', 'Nublado', 'Lluvioso', 'Lluvioso']
    """
    # Estado actual comienza siendo el estado inicial
    estado_actual = estado_inicial

    # Lista que almacenará el pronóstico (incluye el día inicial)
    pronostico = [estado_actual]

    # Simulamos día por día (numero_dias - 1 porque ya tenemos el día inicial)
    for _ in range(numero_dias - 1):
        # Obtenemos el índice del estado actual (0, 1, o 2)
        indice_actual = obtener_indice_estado(estado_actual)

        # Obtenemos las probabilidades de transición desde el estado actual
        probabilidades = matriz_transicion[indice_actual]

        # Elegimos aleatoriamente el siguiente estado según las probabilidades
        """
        np.random.choice() selecciona un elemento de 'estados' de forma aleatoria,
        pero respetando las probabilidades dadas en 'p'.
        
        Ejemplo: Si estado_actual = "Soleado" (índice 0):
        - probabilidades = [0.8, 0.15, 0.05]
        - Tiene 80% de chance de elegir "Soleado"
        - Tiene 15% de chance de elegir "Nublado"
        - Tiene 5% de chance de elegir "Lluvioso"
        """
        siguiente_estado = np.random.choice(
            estados,  # Opciones: ["Soleado", "Nublado", "Lluvioso"]
            p=probabilidades,  # Probabilidades para cada opción
        )

        # Agregamos el estado predicho a nuestro pronóstico
        pronostico.append(siguiente_estado)

        # El siguiente estado se convierte en el actual para la próxima iteración
        estado_actual = siguiente_estado

    return pronostico


# ==================== EJECUCIÓN DEL PROGRAMA ====================

# Realizamos la predicción del clima
pronostico = predecir_clima(estado_inicial, numero_dias)

# Mostramos los resultados de forma clara
print("=" * 50)
print("🌤️  PREDICCIÓN DEL CLIMA - CADENA DE MARKOV")
print("=" * 50)
print(f"\n📍 Estado inicial: {estado_inicial}")
print(f"📅 Días a predecir: {numero_dias}\n")
print("Pronóstico para los próximos días:")
print("-" * 50)

# Mostramos cada día con su predicción
for dia, estado in enumerate(pronostico, start=1):
    # Agregamos emojis para hacer la salida más visual
    emoji = "☀️" if estado == "Soleado" else "☁️" if estado == "Nublado" else "🌧️"
    print(f"  Día {dia:2d}: {emoji}  {estado}")

print("=" * 50)


# ==================== ANÁLISIS ADICIONAL (OPCIONAL) ====================
"""
Podemos calcular estadísticas sobre el pronóstico generado
"""
print("\n📊 Estadísticas del pronóstico:")
print("-" * 50)

# Contamos cuántos días de cada tipo hay
for estado in estados:
    cantidad = pronostico.count(estado)
    porcentaje = (cantidad / numero_dias) * 100
    print(f"  {estado}: {cantidad} días ({porcentaje:.1f}%)")

print("=" * 50)


# ==================== CONCEPTOS CLAVE PARA PROGRAMADORES JUNIOR ====================
"""
1. CADENA DE MARKOV:
   - Modelo probabilístico para predecir secuencias
   - El futuro depende SOLO del estado presente
   - Se usa en: predicción del clima, análisis de texto, finanzas, videojuegos

2. MATRIZ DE TRANSICIÓN:
   - Tabla que almacena probabilidades de pasar de un estado a otro
   - Cada fila representa un estado de origen
   - Cada columna representa un estado de destino
   - La suma de cada fila DEBE ser 1.0

3. PROCESO ESTOCÁSTICO:
   - "Estocástico" = aleatorio pero con probabilidades definidas
   - No sabemos exactamente qué pasará, pero conocemos las probabilidades
   - np.random.choice() nos permite simular este comportamiento aleatorio

4. APLICACIONES REALES:
   - Predicción meteorológica
   - Análisis de mercados financieros
   - Generación de texto (como ChatGPT usa modelos similares)
   - Modelado de comportamiento de usuarios
   - Predicción de fallas en sistemas
"""
