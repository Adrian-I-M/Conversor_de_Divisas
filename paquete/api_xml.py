import requests
import xml.etree.ElementTree as ET

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


def obtener_datos_bce():
    """
    Descarga el XML diario del BCE, extrae la fecha y las tasas de cambio,
    e incluye el Euro como moneda base (1.0).
    """
    try:
        # 1. Petición GET al servidor del BCE
        response = requests.get(URL_BCE, timeout=10)
        
        if response.status_code != 200:
            raise ConnectionError(f"Error al conectar con el servidor. Código HTTP: {response.status_code}")

        # Guardamos el texto original por si queremos mostrarlo en la interfaz (Raw Data)
        xml_crudo = response.content.decode("utf-8")

        # 2. Parseamos el contenido binario a un árbol XML
        raiz = ET.fromstring(response.content)

        fecha = ""
        # 4. Inicializamos el diccionario con el Euro manualmente a 1.0
        tasas = {"EUR": 1.0}

        # 3. Recorremos todos los nodos del árbol XML
        for elemento in raiz.iter():
            # Buscamos el nodo <Cube time="YYYY-MM-DD">
            if "time" in elemento.attrib:
                fecha = elemento.attrib["time"]
            
            # Buscamos los nodos <Cube currency="XXX" rate="0.0000"/>
            elif "currency" in elemento.attrib and "rate" in elemento.attrib:
                moneda = elemento.attrib["currency"]
                tasa = float(elemento.attrib["rate"])
                tasas[moneda] = tasa

        return fecha, tasas, xml_crudo

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Error de red al intentar descargar el XML: {e}")
    except ET.ParseError as e:
        raise ValueError(f"El archivo descargado no tiene un formato XML válido: {e}")


# Bloque de prueba independiente (solo se ejecuta si lanzas este archivo directamente)
if __name__ == "__main__":
    fecha_oficial, diccionario_tasas, _ = obtener_datos_bce()
    print(f"Conexión exitosa. Fecha oficial: {fecha_oficial}")
    print(f"Monedas cargadas: {len(diccionario_tasas)}")