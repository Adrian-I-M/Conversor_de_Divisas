import requests
import xml.etree.ElementTree as ET

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

def obtener_datos_bce():
    response = requests.get(URL_BCE)
    if response.status_code != 200:
        return None, None, None

    xml_crudo = response.content.decode("utf-8")
    raiz = ET.fromstring(response.content)

    fecha = ""
    tasas = {"EUR": 1.0}  # Añadimos el Euro manualmente como moneda base

    for nodo in raiz.iter():
        if "time" in nodo.attrib:
            fecha = nodo.attrib["time"]
        elif "currency" in nodo.attrib and "rate" in nodo.attrib:
            moneda = nodo.attrib["currency"]
            tasas[moneda] = float(nodo.attrib["rate"])

    return fecha, tasas, xml_crudo