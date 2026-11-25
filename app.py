import streamlit as st
from paquete.api_xml import obtener_datos_bce
from paquete.logica import calcular_conversion

st.title("€ Conversor de Divisas (BCE)")
st.write("Esta aplicación consume XML en tiempo real del Banco Central Europeo.")

try:
    fecha, tasas, xml_crudo = obtener_datos_bce()

    if tasas:
        with st.expander("Ver Estructura XML recibida (Raw Data)"):
            st.code(xml_crudo, language="xml")

        st.success(f"Datos cargados. Fecha oficial: **{fecha}**")

        cantidad = st.text_input("Cantidad", value="100,00")

        monedas = list(tasas.keys())
        col1, col2 = st.columns(2)
        with col1:
            origen = st.selectbox("De:", monedas, index=0)   # EUR
        with col2:
            destino = st.selectbox("A:", monedas, index=1)  # USD

        if st.button("Calcular Conversión", type="primary"):
            try:
                resultado, tasa_unitaria = calcular_conversion(cantidad, origen, destino, tasas)
                st.metric(
                    label=f"Valor en {destino}",
                    value=f"{resultado:.2f} {destino}",
                    delta=f"Tipo de cambio: 1 {origen} = {tasa_unitaria:.4f} {destino}"
                )
            except ValueError:
                st.error("Por favor, introduce un valor numérico válido.")

        st.subheader("Tabla de Tipos de Cambio (Base EUR)")
        st.dataframe(
            [{"Moneda": m, "Tasa": t} for m, t in tasas.items()],
            use_container_width=True
        )
    else:
        st.error("Error al conectar con el servidor del BCE.")

except Exception as e:
    st.error(f"Ha ocurrido un error: {e}")