import streamlit as st
from paquete.api_xml import obtener_datos_bce
from paquete.logica import calcular_conversion

# Configuración básica de la página
st.set_page_config(page_title="Conversor de Divisas (BCE)", page_icon="€", layout="centered")

st.title("€ Conversor de Divisas (BCE)")
st.write("Esta aplicación consume XML en tiempo real del Banco Central Europeo.")


# Carga automática con caché para no saturar el servidor del BCE en cada clic
@st.cache_data(ttl=3600)
def cargar_datos():
    return obtener_datos_bce()


try:
    fecha_oficial, tasas, xml_crudo = cargar_datos()

    # Desplegable opcional para inspeccionar el XML descargado (Raw Data)
    with st.expander("Ver Estructura XML recibida (Raw Data)"):
        st.code(xml_crudo, language="xml")

    # Fecha de actualización visible exigida por el enunciado
    st.success(f"Datos cargados. Fecha oficial: **{fecha_oficial}**")

    # Campo de texto para permitir probar la validación frente a letras en la defensa
    cantidad_str = st.text_input("Cantidad", value="100.00")

    # Selectores de moneda de origen y destino en dos columnas
    lista_monedas = list(tasas.keys())
    col1, col2 = st.columns(2)

    with col1:
        moneda_origen = st.selectbox("De:", options=lista_monedas, index=0)  # EUR por defecto
    with col2:
        indice_usd = lista_monedas.index("USD") if "USD" in lista_monedas else 1
        moneda_destino = st.selectbox("A:", options=lista_monedas, index=indice_usd)

    # Botón que dispara el cálculo
    if st.button("Calcular Conversión", type="primary"):
        try:
            resultado, tasa_unitaria = calcular_conversion(
                cantidad_str, moneda_origen, moneda_destino, tasas
            )
            st.metric(
                label=f"Valor en {moneda_destino}",
                value=f"{resultado:.2f} {moneda_destino}",
                delta=f"Tipo de cambio: 1 {moneda_origen} = {tasa_unitaria:.4f} {moneda_destino}",
            )
        except ValueError as err_valor:
            st.error(f"Error en el importe: {err_valor}")
        except KeyError as err_moneda:
            st.error(f"Error de divisa: {err_moneda}")

    # Tabla de referencia con todas las tasas base EUR
    st.subheader("Tabla de Tipos de Cambio (Base EUR)")
    tabla_tasas = [{"Moneda": moneda, "Tasa": tasa} for moneda, tasa in tasas.items()]
    st.dataframe(tabla_tasas, use_container_width=True)

except Exception as e:
    st.error(f"No se pudo iniciar la aplicación: {e}")