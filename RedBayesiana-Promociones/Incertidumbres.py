import numpy as np
from scipy.stats import norm
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD

modelo = DiscreteBayesianNetwork(
    [
        ("HistorialCompras", "Compra"),  # El historial influye en la compra
        ("TiempoEnSitio", "Compra"),  # El tiempo en el sitio influye en la compra
        ("ClicoPromocion", "Compra"),  # Clicar en promoción influye en la compra
    ]
)

cpd_historial = TabularCPD(
    variable="HistorialCompras",
    variable_card=2,  # 2 valores posibles: 0 o 1
    values=[[0.7], [0.3]],  # P(HistorialCompras=0) = 70%  # P(HistorialCompras=1) = 30%
)

cpd_tiempo = TabularCPD(
    variable="TiempoEnSitio",
    variable_card=2,  # 2 valores posibles: 0 o 1
    values=[[0.6], [0.4]],  # P(TiempoEnSitio=0) = 60%  # P(TiempoEnSitio=1) = 40%
)

cpd_promocion = TabularCPD(
    variable="ClicoPromocion",
    variable_card=2,  # 2 valores posibles: 0 o 1
    values=[[0.8], [0.2]],  # P(ClicoPromocion=0) = 80%  # P(ClicoPromocion=1) = 20%
)

cpd_compra = TabularCPD(
    variable="Compra",
    variable_card=2,  # 2 valores: 0 (no compra) o 1 (compra)
    values=[
        # Probabilidades de NO comprar (Compra=0)
        [0.9, 0.7, 0.8, 0.4, 0.6, 0.2, 0.3, 0.1],
        # Probabilidades de SÍ comprar (Compra=1)
        [0.1, 0.3, 0.2, 0.6, 0.4, 0.8, 0.7, 0.9],
    ],
    evidence=[
        "HistorialCompras",
        "TiempoEnSitio",
        "ClicoPromocion",
    ],  # Variables que influyen
    evidence_card=[2, 2, 2],  # Cada una tiene 2 valores posibles
)

modelo.add_cpds(cpd_historial, cpd_tiempo, cpd_promocion, cpd_compra)

assert modelo.check_model(), "¡Error! El modelo tiene inconsistencias"
print("✓ Modelo validado correctamente")

from pgmpy.inference import VariableElimination

inferencia = VariableElimination(modelo)

resultado = inferencia.query(
    variables=["Compra"],  # Variable que queremos predecir
    evidence={
        "HistorialCompras": 0,  # El cliente SÍ tiene historial de compras
        "TiempoEnSitio": 1,  # El cliente pasó POCO tiempo en el sitio
        "ClicoPromocion": 1,  # El cliente SÍ clicó en una promoción
    },
)

print("\n" + "=" * 50)
print("PREDICCIÓN: Probabilidad de compra")
print("n" * 50)
print("Evidencia observada:")
print(" - Historial de compras: Sí")
print(" - Tiempo en el sitio: POCO")
print(" - Clicó en promoción: Sí")
print("\nResultado:")
print(resultado)
print("n"*50)

media_tiempo = 5
desviacion_estandar = 2
tiempo_observado = 6

probabilidad_tiempo = norm.cdf(
    tiempo_observado, loc=media_tiempo, scale=desviacion_estandar
)


print(f"\n\nANÁLISIS DE TIEMPO EN EL SITIO")
print(f"Tiempo observado: {tiempo_observado} minutos")
print(f"Media esperada: {media_tiempo} minutos")
print(f"Desviación estándar: {desviacion_estandar} minutos")
print(
    f"Probabilidad de pasar menos de {tiempo_observado} minutos: {probabilidad_tiempo:.2%}"
)
print(
    f"Esto significa que el {(probabilidad_tiempo):.1%} de clientes pasan menos tiempo."
)
