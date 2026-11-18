def validar_importe(valor):
    """Convierte la entrada a float positivo y captura errores si contiene letras."""
    try:
        # Permitimos tanto punto como coma decimal
        if isinstance(valor, str):
            valor = valor.replace(",", ".").strip()
        importe = float(valor)
    except (ValueError, TypeError):
        raise ValueError("El importe debe ser un valor numérico válido.")

    if importe < 0:
        raise ValueError("El importe no puede ser negativo.")

    return importe


def calcular_conversion(importe, moneda_origen, moneda_destino, tasas):
    """
    Calcula la conversión cruzada usando el Euro como moneda puente.
    Devuelve (cantidad_final, tasa_unitaria).
    """
    importe_valido = validar_importe(importe)

    if moneda_origen not in tasas or moneda_destino not in tasas:
        raise KeyError("Una de las divisas seleccionadas no está disponible.")

    tasa_origen = tasas[moneda_origen]
    tasa_destino = tasas[moneda_destino]

    # Fórmula de conversión cruzada: (Importe / TasaOrigen) * TasaDestino
    cantidad_final = (importe_valido / tasa_origen) * tasa_destino
    
    # Tasa directa entre ambas monedas (ej. 1 EUR = 1.1648 USD)
    tasa_unitaria = tasa_destino / tasa_origen

    return cantidad_final, tasa_unitaria


# Bloque de prueba en consola
if __name__ == "__main__":
    tasas_prueba = {"EUR": 1.0, "USD": 1.1648, "JPY": 179.22}

    # 1. Prueba directa (EUR -> USD)
    res, tasa = calcular_conversion(100, "EUR", "USD", tasas_prueba)
    print(f"100 EUR -> {res:.2f} USD (1 EUR = {tasa:.4f} USD)")

    # 2. Prueba cruzada (USD -> JPY)
    res_cruzada, _ = calcular_conversion(50, "USD", "JPY", tasas_prueba)
    print(f"50 USD -> {res_cruzada:.2f} JPY")

    # 3. Prueba de error con letras
    try:
        calcular_conversion("abc", "EUR", "USD", tasas_prueba)
    except ValueError as e:
        print(f"Control de error correcto: {e}")