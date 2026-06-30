import heapq


# ==================== CLASE PRODUCTO ====================
class Producto:
    """
    Representa un producto en el sistema de recomendación.

    Atributos:
        nombre (str): Nombre del producto
        categoria (str): Categoría a la que pertenece el producto
        probabilidad_conversion (float): Probabilidad de que el usuario compre este producto (0.0 a 1.0)

    Ejemplo:
        >>> producto = Producto("Laptop", "Electrónica", 0.85)
    """

    def __init__(self, nombre, categoria, probabilidad_conversion):
        self.nombre = nombre
        self.categoria = categoria
        self.probabilidad_conversion = probabilidad_conversion

    def __repr__(self):
        """
        Representación en texto del producto para imprimirlo en consola.
        Retorna: String con formato "Nombre (Categoría)"
        """
        return f"{self.nombre} ({self.categoria})"


# ==================== CLASE SISTEMA DE RECOMENDACIÓN ====================
class RecomendacionAStar:
    """
    Sistema de recomendación que utiliza el algoritmo A* para encontrar
    la mejor ruta entre productos basándose en probabilidades de conversión.

    El algoritmo A* es un algoritmo de búsqueda que encuentra el camino más corto
    entre dos puntos, utilizando una función heurística para optimizar la búsqueda.

    Atributos:
        productos (list): Lista de objetos Producto disponibles
        heuristica (function): Función que evalúa qué tan "bueno" es un producto
        grafo (dict): Estructura de datos que conecta productos entre sí
    """

    def __init__(self, productos, heuristica):
        self.productos = productos
        self.heuristica = heuristica  # Función que evalúa la calidad del producto
        self.grafo = self.crear_grafo()


    def crear_grafo(self):
        """
        Crea un grafo donde cada producto está conectado con todos los demás.

        Un grafo es una estructura de datos que representa conexiones entre elementos.
        En este caso, cada producto puede "conectarse" (recomendarse) con cualquier otro.

        Retorna:
            dict: Diccionario donde cada clave es un producto y el valor es una lista
                de productos a los que se puede conectar (todos excepto él mismo)
        """
        grafo = {}
        for producto in self.productos:
            # Conectamos cada producto con todos los demás (excepto consigo mismo)
            grafo[producto] = [p for p in self.productos if p != producto]
        return grafo


    def a_star(self, inicio, objetivo):
        """
        Implementación del algoritmo A* para encontrar la mejor ruta de recomendación.

        El algoritmo funciona así:
        1. Comienza desde el producto 'inicio'
        2. Explora productos vecinos, priorizando los más prometedores
        3. Usa la heurística para decidir qué productos explorar primero
        4. Termina cuando encuentra el producto 'objetivo'

        Parámetros:
            inicio (Producto): Producto desde donde comenzar la búsqueda
            objetivo (Producto): Producto que queremos alcanzar

        Retorna:
            list: Lista de productos que forman el camino recomendado

        Conceptos clave:
            - g: Costo acumulado (número de pasos dados hasta ahora)
            - h: Heurística (estimación de qué tan bueno es este producto)
            - f: g + h (costo total estimado)
        """

        # Cola de prioridad: almacena productos ordenados por su valor f (más bajo = mejor)
        cola_prioridad = []

        # Agregamos el producto inicial con f = 0 + heuristica(inicio)
        heapq.heappush(cola_prioridad, (0 + self.heuristica(inicio), 0, inicio))

        # Conjunto para recordar qué productos ya visitamos (evita ciclos infinitos)
        visitados = set()

        # Diccionario para recordar de dónde vino cada producto (para reconstruir el camino)
        caminos = {}

        # Mientras haya productos por explorar
        while cola_prioridad:

            # Extraemos el producto con menor valor f (el más prometedor)
            _, g, actual = heapq.heappop(cola_prioridad)

            # Si ya visitamos este producto, lo saltamos
            if actual in visitados:
                continue

            # Marcamos el producto como visitado
            visitados.add(actual)

            # Si llegamos al objetivo, terminamos la búsqueda
            if actual == objetivo:
                break

            # Exploramos todos los productos vecinos (conectados)
            for vecino in self.grafo[actual]:
                if vecino not in visitados:
                    # Calculamos la heurística del vecino
                    h = self.heuristica(vecino)

                    # g + 1 porque damos un paso más, h es la heurística
                    heapq.heappush(cola_prioridad, (g + 1 + h, g + 1, vecino))

                    # Recordamos que llegamos a 'vecino' desde 'actual'
                    caminos[vecino] = actual

        # === RECONSTRUCCIÓN DEL CAMINO ===
        # Ahora que encontramos el objetivo, reconstruimos el camino desde el inicio
        camino = []
        producto = objetivo

        # Vamos hacia atrás desde el objetivo hasta el inicio
        while producto in caminos:
            camino.insert(0, producto)  # Insertamos al principio de la lista
            producto = caminos[producto]  # Retrocedemos al producto anterior

        return camino


# ==================== FUNCIÓN HEURÍSTICA ====================
def heuristica(producto):
    """
    Función heurística que evalúa qué tan "bueno" es un producto.

    En este caso, usamos la probabilidad de conversión como heurística:
    - Productos con ALTA probabilidad de conversión son MÁS atractivos
    - Retornamos el valor NEGATIVO porque A* busca MINIMIZAR el costo
    - Ejemplo: probabilidad 0.9 -> heurística -0.9 (mejor que -0.5)

    Parámetros:
        producto (Producto): El producto a evaluar

    Retorna:
        float: Valor negativo de la probabilidad de conversión
    """
    # Negativo porque A* minimiza, y queremos MAXIMIZAR la probabilidad
    return -producto.probabilidad_conversion


# ==================== EJEMPLO DE USO ====================
if __name__ == "__main__":
    # Creamos una lista de productos de ejemplo
    productos = [
        Producto("Producto A", "Categoría 1", 0.9),  # Alta probabilidad de conversión
        Producto("Producto B", "Categoría 1", 0.8),
        Producto("Producto C", "Categoría 2", 0.7),
        Producto("Producto D", "Categoría 2", 0.6),  # Baja probabilidad de conversión
    ]

    # Creamos el sistema de recomendación con los productos y la función heurística
    recomendador = RecomendacionAStar(productos, heuristica)

    # Definimos el producto inicial y el producto objetivo
    inicio = productos[0]  # Producto A
    objetivo = productos[2]  # Producto C

    # Buscamos el mejor camino de recomendación
    camino_recomendado = recomendador.a_star(inicio, objetivo)

    # Mostramos el resultado
    print("Camino recomendado:")
    for p in camino_recomendado:
        print(p)
