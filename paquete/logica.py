def calcular_conversion(cantidad_texto, origen, destino, tasas):
    """Calcula la conversión entre dos divisas usando el Euro como moneda puente."""
    # Convertimos el texto a decimal (admitiendo coma o punto)
    # Si el usuario escribe letras, float() lanza automáticamente un ValueError
    importe = float(cantidad_texto.replace(",", ".").strip())

    if importe < 0:
        raise ValueError("El importe no puede ser negativo.")

    # Fórmula de conversión cruzada: (Importe / TasaOrigen) * TasaDestino
    resultado = (importe / tasas[origen]) * tasas[destino]

    # Tipo de cambio unitario entre ambas monedas (1 Origen = X Destino)
    tasa_unitaria = tasas[destino] / tasas[origen]

    return resultado, tasa_unitaria