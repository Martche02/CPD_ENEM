import math

def calcular_taxa_acerto(a: float, b: float, c: float) -> float:
    """
    Aproxima a taxa de acerto esperada para uma questão com parâmetros TRI (3PL),
    sem dependências externas e com precisão limitada.
    """

    def logistic(z):
        return 1 / (1 + math.exp(-z))

    def normal_pdf(x):
        return math.exp(-x**2 / 2) / math.sqrt(2 * math.pi)

    def integrand(theta):
        z = a * (theta - b)
        p = c + (1 - c) * logistic(z)
        return p * normal_pdf(theta)

    # Integração por trapézios simples no intervalo [-4, 4]
    n = 1000
    start = -4
    end = 4
    step = (end - start) / n

    area = 0.0
    for i in range(n):
        x0 = start + i * step
        x1 = x0 + step
        y0 = integrand(x0)
        y1 = integrand(x1)
        area += (y0 + y1) * step / 2

    return round(area, 3)

def safe_float(valor, default=0.0):
    try:
        return float(valor)
    except ValueError:
        return default