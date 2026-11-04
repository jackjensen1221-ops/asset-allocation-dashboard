import streamlit as st
import pandas as pd
import plotly.express as px
from macro_engine import fetch_fred_data

st.set_page_config(page_title="Macro Regime & Asset Allocation Monitor", layout="wide")

st.title("🌐 Macroeconomic Regime & Tactical Asset Allocation Monitor")
st.markdown("Designed for Wealth & Asset Management Advisory: Connecting Fed Policy & Yield Curves to Portfolio Positioning.")

@st.cache_data(ttl=86400) # Cache data for 24 hours
def load_data():
    return fetch_fred_data()

with st.spinner("Fetching live economic data from FRED..."):
    df = load_data()

# Get latest available data point
latest = df.iloc[-1]
prev_spread = df['Yield_Spread'].iloc[-2]
current_spread = latest['Yield_Spread']

# Layout metrics
st.header("📊 Current Macro Snapshot")
col1, col2, col3, col4 = st.columns(4)
col1.metric("10Y-2Y Treasury Spread", f"{current_spread:.2f}%", delta=f"{current_spread - prev_spread:.2f}%")
col2.metric("Federal Funds Rate", f"{latest['Fed_Funds_Rate']:.2f}%")
col3.metric("Inflation (YoY)", f"{latest['Inflation_YoY']:.1f}%" if not pd.isna(latest['Inflation_YoY']) else "N/A")
col4.metric("Unemployment Rate", f"{latest['Unemployment_rate'] if 'Unemployment_rate' in latest else latest['Unemployment']:.1f}%")

# Yield Curve Inversion Warning Banner
if current_spread < 0:
    st.error("⚠️ **ALERT: Yield Curve Inversion Detected.** Historically, a negative 10Y-2Y spread signals heightened recession risk within 6–18 months. Defensive asset rebalancing recommended.")
else:
    st.success("✅ **Yield Curve is Normal (Upward Sloping).** Expansionary environment favored.")

# Interactive Historical Charting
st.header("📈 Historical Economic Indicators")
indicator_choice = st.selectbox(
    "Select Indicator to Visualize:",
    ["Yield_Spread", "Fed_Funds_Rate", "Inflation_YoY", "Unemployment"]
)

fig = px.line(df, x=df.index, y=indicator_choice, title=f"Historical Trend: {indicator_choice}")
fig.update_layout(xaxis_title="Date", yaxis_title="Percent (%)", hovermode="x")
st.plotly_chart(fig, use_container_width=True)

# Tactical Asset Allocation Recommendation Engine
st.header("⚖️ Tactical Asset Allocation Model")
st.markdown("Based on current macroeconomic regime indicators, the model suggests the following tactical tilt for private wealth clients:")

# Simple heuristic rule for allocation
if current_spread < 0:
    # Recession Watch: Defend Capital
    allocation = {"Equities": 40, "Fixed Income (Long Duration Treasuries)": 40, "Cash / Equivalents": 20}
    regime = "Late Cycle / Defensive (Inverted Yield Curve)"
elif latest['Fed_Funds_Rate'] > 4.5:
    # Tight Monetary Policy
    allocation = {"Equities (Value/Quality)": 50, "Fixed Income (Short-Term Credit)": 30, "Cash / Equivalents": 20}
    regime = "Restrictive Monetary Policy (High Fed Funds)"
else:
    # Expansion
    allocation = {"Equities (Growth/Cyclicals)": 70, "Fixed Income (Aggregate Bonds)": 20, "Cash / Equivalents": 10}
    regime = "Economic Expansion"

st.info(f"**Detected Market Regime:** {regime}")
df_alloc = pd.DataFrame(list(allocation.items()), columns=["Asset Class", "Tactical Weight (%)"])
st.dataframe(df_alloc, use_container_width=True)
