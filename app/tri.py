import numpy as np
from scipy.stats import norm
from scipy.integrate import quad

def safe_float(valor, default=0.0):
    try:
        return float(valor)
    except ValueError:
        return default
    
def calcular_taxa_acerto(a: float, b: float, c: float) -> float:
    """
    Calcula a taxa de acerto esperada para uma questão com os parâmetros TRI (3PL).
    """

    def integrand(theta):
        z = a * (theta - b)
        ez = np.exp(-np.abs(z))
        logistic = np.where(z >= 0, 1 / (1 + ez), ez / (1 + ez))
        return (c + (1 - c) * logistic) * norm.pdf(theta)

    resultado, _ = quad(integrand, -np.inf, np.inf)
    return resultado
