import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Felipe Financials", layout="wide", initial_sidebar_state="expanded")

st.title("🦅 Centro de Comando Financiero")
st.markdown("---")

# --- ARCHIVOS ---
archivo_db = "inversiones.db"
# IMPORTANTE: En el repo público, esto debe apuntar al archivo DEMO
archivo_master = "Reporte_Inversiones_DEMO.xlsx" 

try:
    # --- LÓGICA DE CARGA INTELIGENTE ---
    # 1. ¿Es Modo Demo?
    if "DEMO" in archivo_master:
        # Si es Demo, nos saltamos la conexión SQL para evitar el error en la nube
        df_historia = pd.DataFrame() 
    else:
        # 2. Si es Modo Real (tu PC), cargamos SQL normalmente
        conn = sqlite3.connect(archivo_db)
        query = "SELECT * FROM historial_transacciones"
        df_historia = pd.read_sql(query, conn)
        conn.close()
        
        # Estandarización de nombres SQL -> Dashboard
        df_historia.rename(columns={
            'tipo_de_movimiento': 'Tipo de Movimiento',
            'monto_total': 'Monto Total',
            'fecha': 'Fecha',
            'instrumento': 'Instrumento',
            'precio': 'Precio',
            'cantidad': 'Cantidad',
            'comision': 'Comision'
        }, inplace=True)
        
        df_historia['Fecha'] = pd.to_datetime(df_historia['Fecha'])
    
    # 3. Carga de Master (Excel) - ESTO SIEMPRE SE EJECUTA
    df_master = pd.read_excel(archivo_master)
    df_master['Valor Mercado'] = df_master['Stock'] * df_master['Precio Mercado']
    
    if 'RETORNO TOTAL %' in df_master.columns:
        df_master['RETORNO_NUM'] = df_master['RETORNO TOTAL %'].astype(str).str.replace('%','').astype(float)
        
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuración")
meta_mensual = st.sidebar.number_input("Meta: Gastos Mensuales ($)", value=800000, step=50000)

if "DEMO" in archivo_master:
    st.sidebar.warning("⚠️ MODO DEMO (WEB)")
else:
    st.sidebar.success("✅ MODO REAL (LOCAL)")

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🏆 Tablero Principal", "📊 Detalle & Rentabilidad", "🔮 Simulador"])

# --- TAB 1: ESTRATEGIA ---
with tab1:
    st.subheader("🔥 Progreso LF")
    
    ingreso_anual_proyectado = df_master['Proyección Anual ($)'].sum()
    ingreso_mensual_real = ingreso_anual_proyectado / 12
    porcentaje_libertad = (ingreso_mensual_real / meta_mensual)
    if porcentaje_libertad > 1: porcentaje_libertad = 1.0
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.progress(porcentaje_libertad)
        st.caption(f"Cobertura: **{porcentaje_libertad:.1%}**")
    with c2:
        st.metric("Sueldo Pasivo", f"${ingreso_mensual_real:,.0f}")

    st.divider()

    c1, c2, c3 = st.columns(3)
    total_valor = df_master['Valor Mercado'].sum()
    
    if 'RETORNO_NUM' in df_master.columns and total_valor > 0:
        rentabilidad_promedio = (df_master['RETORNO_NUM'] * df_master['Valor Mercado']).sum() / total_valor
    else:
        rentabilidad_promedio = 0

    c1.metric("Patrimonio", f"${total_valor:,.0f}")
    c2.metric("Dividendos Anuales", f"${ingreso_anual_proyectado:,.0f}")
    c3.metric("Rentabilidad Ponderada", f"{rentabilidad_promedio:.2f}%")

    fig_pie = px.pie(df_master, values='Valor Mercado', names='Ticker', hole=0.5)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: DETALLE ---
with tab2:
    st.subheader("🔍 Radiografía")
    
    # Lógica inteligente: ¿Mostramos SQL Real o Falsificamos?
    if "DEMO" in archivo_master:
        # Falsificación de datos para la Demo (Basado en el Excel Demo)
        df_top = df_master[['Ticker', 'Proyección Anual ($)']].copy()
        df_top.rename(columns={'Ticker': 'Empresa', 'Proyección Anual ($)': 'Total_Cobrado'}, inplace=True)
        df_top['Total_Cobrado'] = df_top['Total_Cobrado'] * 1.5 # Simulamos histórico mayor
        df_top = df_top.sort_values('Total_Cobrado', ascending=False).head(5)
    else:
        # Datos Reales desde SQL (Solo funciona en tu PC local)
        # Re-creamos la conexión porque la cerramos arriba
        conn = sqlite3.connect(archivo_db)
        query_top = """
        SELECT instrumento AS Empresa, SUM(monto_total) AS Total_Cobrado
        FROM historial_transacciones
        WHERE tipo_de_movimiento = 'DIVIDENDO'
        GROUP BY instrumento
        ORDER BY Total_Cobrado DESC
        """
        df_top = pd.read_sql(query_top, conn)
        conn.close()
    
    c1, c2 = st.columns([2, 1])
    with c1:
        fig_sql = px.bar(df_top, x='Total_Cobrado', y='Empresa', orientation='h', text_auto='.2s')
        fig_sql.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_sql, use_container_width=True)
    with c2:
        top_company = df_top.iloc[0]['Empresa']
        top_amount = df_top.iloc[0]['Total_Cobrado']
        st.info(f"Top Pagador: **{top_company}** (${top_amount:,.0f})")

    st.divider()
    
    if 'RETORNO_NUM' in df_master.columns:
        fig_bar = px.bar(df_master, x='Ticker', y='RETORNO_NUM', color='RETORNO_NUM', color_continuous_scale='RdYlGn', text_auto='.1f')
        st.plotly_chart(fig_bar, use_container_width=True)

    cols = ['Ticker', 'Stock', 'PPP (Tu Precio)', 'Precio Mercado', 'Yield s/Costo (YoC)', 'Plusvalía Capital', 'RETORNO TOTAL %']
    valid_cols = [c for c in cols if c in df_master.columns]
    st.dataframe(df_master[valid_cols], use_container_width=True)

# --- TAB 3: SIMULADOR ---
with tab3:
    st.subheader("🚀 Simulador")
    c1, c2 = st.columns([1, 2])
    
    with c1:
        aporte = st.slider("Aporte Mensual", 0, 2000000, 500000)
        tasa = st.slider("Tasa Anual (%)", 4.0, 15.0, 7.0)
        anios = st.slider("Años", 5, 30, 16)
        
    with c2:
        data = []
        saldo = total_valor
        aporte_anual = aporte * 12
        
        for i in range(anios + 1):
            if i > 0: saldo = (saldo + aporte_anual) * (1 + (tasa/100))
            data.append({"Año": 2025 + i, "Saldo": int(saldo)})
            
        df_sim = pd.DataFrame(data)
        st.markdown(f"Proyección: **${saldo:,.0f}**")
        fig = px.line(df_sim, x="Año", y="Saldo", markers=True)
        fig.update_traces(fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)
