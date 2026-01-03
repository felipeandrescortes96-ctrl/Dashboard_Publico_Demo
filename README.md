# 🦅 Centro de Comando Financiero (Financial Freedom Dashboard)

> Herramienta de control de gestión automatizada para el seguimiento de inversiones, dividendos y proyección de Libertad Financiera.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]((https://dashboardpublicodemo-64bvwfsnd6vgtf4avbwgry.streamlit.app/))
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/Status-Production-green)

## 🎯 Objetivo del Proyecto
Este dashboard fue desarrollado para solucionar la falta de visibilidad en tiempo real de un portafolio de inversiones diversificado. Permite pasar de planillas de Excel manuales y estáticas a un sistema dinámico conectado a bases de datos.

## 🛠️ Tecnologías Utilizadas
* **Python:** Lógica de negocio y procesamiento de datos.
* **Streamlit:** Framework para la visualización web interactiva.
* **SQL (SQLite):** Almacenamiento histórico de transacciones y dividendos.
* **Pandas:** Manipulación y limpieza de datos financieros (ETL).
* **Plotly:** Gráficos interactivos.

## 🚀 Funcionalidades Clave
1.  **Modo Híbrido (Real/Demo):** El sistema detecta automáticamente si está en entorno local (mostrando datos reales SQL) o en web pública (generando datos ficticios para protección de privacidad).
2.  **Cálculo de LF:** KPI en tiempo real sobre el porcentaje de gastos cubiertos por ingresos pasivos.
3.  **Análisis Histórico:** Conexión a Base de Datos para analizar "Top Pagadores" históricos.
4.  **Simulador de Interés Compuesto:** Proyección a futuro basada en variables ajustables (Tasa, Aporte, Años).

## 📂 Estructura del Proyecto
* `mi_dashboard.py`: Código fuente principal de la aplicación.
* `inversiones.db`: Base de datos SQL (Local solamente).
* `generar_datos_demo.py`: Script generador de datos sintéticos para pruebas públicas.

---
*Desarrollado por Felipe Cortés - 2026*
