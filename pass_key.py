import secrets
import string

def generar_llaves(cantidad, longitud):
    """
    Genera una lista de llaves de activación aleatorias.

    Args:
        cantidad: Número de llaves a generar.
        longitud: Longitud de cada llave.

    Returns:
        Una lista de cadenas, cada una representando una llave de activación.
    """

    caracteres = string.ascii_letters + string.digits
    llaves = []
    for _ in range(cantidad):
        llave = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        llaves.append(llave)
    return llaves

# Generar 100 llaves de 20 caracteres
llaves_generadas = generar_llaves(100, 20)

# Imprimir las llaves en el formato deseado
print(llaves_generadas)