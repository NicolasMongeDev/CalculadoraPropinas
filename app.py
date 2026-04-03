import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Calculadora Pro", page_icon="🧮")

st.title("🧮 Calculadora de Gastos y Propinas")
st.markdown("Añade tus consumos y calcula la división de la cuenta fácilmente.")

# Inicializamos una lista para los productos si no existe
if 'productos' not in st.session_state:
    st.session_state.productos = []

col3, col4 = st.columns([2, 1])

with col3:
    # --- SECCIÓN 1: AÑADIR PRODUCTOS ---
    with st.expander("➕ Añadir consumos", expanded=True):
        col1, col2 = st.columns([2, 1])
        nombre = col1.text_input("Producto/Servicio", placeholder="Ej. Pizza, Bebida..."
                                 ,max_chars=25,help="Máximo 25 caracteres para mantener el ticket ordenado")
        precio = col2.number_input("Precio ($)", min_value=0.0, step=0.50)
        
        if st.button("Agregar a la cuenta"):
            if nombre and precio > 0:
                st.session_state.productos.append({"nombre": nombre, "precio": precio})
                st.rerun()
    

with col4:
    # --- SECCIÓN 2: LISTADO DE CUENTA ---
    subtotal = 0.0
    if st.session_state.productos:
        with st.container(height=200):
            st.subheader("📋 Resumen")
            
            for i, p in enumerate(st.session_state.productos):
                st.write(f"{p['nombre']}: **${p['precio']:.2f}**")
                subtotal += p['precio']
        
        if st.button("Limpiar cuenta"):
                st.session_state.productos = []
                st.rerun()
    else:
        st.info("Aún no hay productos en la cuenta.")


st.divider()

# --- SECCIÓN 3: CÁLCULO FINAL ---
st.subheader("💰 Total y Propina")
col_prop, col_pers = st.columns(2)

porcentaje_propina = col_prop.slider("Porcentaje de propina (%)", 0, 30, 10)
num_personas = col_pers.number_input("Número de personas", min_value=1, value=1)

# Cálculos
monto_propina = subtotal * (porcentaje_propina / 100)
total_general = subtotal + monto_propina
pago_por_persona = total_general / num_personas

# Mostrar resultados destacados
st.success(f"### Total a pagar: ${total_general:.2f}")

c1, c2, c3 = st.columns(3)
c1.metric("Subtotal", f"${subtotal:.2f}")
c2.metric("Propina", f"${monto_propina:.2f}")
c3.metric("Por persona", f"${pago_por_persona:.2f}")