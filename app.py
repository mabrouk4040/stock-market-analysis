import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="StockLens",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}

.main-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
}

.main-title {
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #38bdf8, #818cf8, #e879f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin-bottom: 0.3rem;
}

.main-subtitle {
    color: #64748b;
    font-size: 1rem;
    font-weight: 400;
}

.metric-card {
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: border-color 0.2s;
}

.metric-card:hover { border-color: #38bdf8; }

.metric-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 600;
    color: #f1f5f9;
}

.metric-change-pos {
    font-size: 0.85rem;
    color: #22c55e;
    font-weight: 600;
}

.metric-change-neg {
    font-size: 0.85rem;
    color: #ef4444;
    font-weight: 600;
}

.stock-name-badge {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.2rem 2rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.section-title {
    color: #94a3b8;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
    margin-bottom: 1rem;
    margin-top: 2rem;
}

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #1e293b;
    font-size: 0.9rem;
}

.info-label { color: #64748b; }
.info-value { color: #e2e8f0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }

div[data-testid="stTextInput"] input {
    background: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.1rem !important;
    padding: 0.75rem 1rem !important;
    text-transform: uppercase;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important;
}

div[data-testid="stSelectbox"] > div {
    background: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    width: 100%;
    transition: opacity 0.2s !important;
}

.stButton > button:hover { opacity: 0.85 !important; }

.error-box {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #fca5a5;
    margin: 1rem 0;
}

.warning-box {
    background: rgba(234,179,8,0.1);
    border: 1px solid rgba(234,179,8,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #fde047;
    margin: 1rem 0;
}

.success-box {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #86efac;
    margin: 1rem 0;
}

.footer {
    text-align: center;
    color: #334155;
    font-size: 0.8rem;
    padding: 3rem 0 1rem 0;
    border-top: 1px solid #1e293b;
    margin-top: 3rem;
}

[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# Import modules
from backend import fetch_stock_data, validate_symbol, get_stock_info
from data_processing import process_stock_data, compute_indicators
from visualization import (
    plot_price_trend,
    plot_candlestick,
    plot_volume,
    plot_moving_averages
)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-title">📈 StockLens</div>
    <div class="main-subtitle">Real-time stock market analysis & visualization</div>
</div>
""", unsafe_allow_html=True)

# ─── Search Bar ────────────────────────────────────────────────────────────────
col_input, col_period, col_btn = st.columns([3, 2, 1])

with col_input:
    symbol = st.text_input(
        "Stock Symbol",
        placeholder="e.g. AAPL, TSLA, GOOGL",
        label_visibility="collapsed"
    ).strip().upper()

with col_period:
    period_map = {
        "1 Week": "7d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
    }
    period_label = st.selectbox(
        "Period",
        list(period_map.keys()),
        index=1,
        label_visibility="collapsed"
    )
    period = period_map[period_label]

with col_btn:
    search = st.button("Analyze", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Main Logic ────────────────────────────────────────────────────────────────
if search or symbol:
    if not symbol:
        st.markdown('<div class="warning-box">⚠️ Please enter a stock symbol to get started.</div>', unsafe_allow_html=True)
    elif not validate_symbol(symbol):
        st.markdown(f'<div class="error-box">❌ <strong>"{symbol}"</strong> doesn\'t look like a valid stock symbol. Use 1–5 uppercase letters (e.g. AAPL, TSLA).</div>', unsafe_allow_html=True)
    else:
        with st.spinner(f"Fetching data for {symbol}..."):
            hist, error = fetch_stock_data(symbol, period)
            info, info_error = get_stock_info(symbol)

        if error:
            st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
        else:
            # Process data
            processed = process_stock_data(hist)
            indicators = compute_indicators(processed)

            # ── Company Header ──────────────────────────────────────────────
            company_name = info.get("longName", symbol) if info else symbol
            sector = info.get("sector", "N/A") if info else "N/A"
            exchange = info.get("exchange", "N/A") if info else "N/A"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:1px solid #334155;
                        border-radius:16px;padding:1.5rem 2rem;margin-bottom:2rem;">
                <div style="font-size:1.6rem;font-weight:700;color:#f1f5f9;">{company_name}</div>
                <div style="color:#64748b;font-size:0.9rem;margin-top:0.3rem;">
                    <span style="color:#38bdf8;font-family:'JetBrains Mono',monospace;font-weight:600;">{symbol}</span>
                    &nbsp;·&nbsp; {sector} &nbsp;·&nbsp; {exchange}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Key Metrics ─────────────────────────────────────────────────
            latest = processed.iloc[-1]
            prev   = processed.iloc[-2] if len(processed) > 1 else latest

            current_price = latest["Close"]
            prev_close    = prev["Close"]
            day_change    = current_price - prev_close
            day_pct       = (day_change / prev_close) * 100
            change_color  = "#22c55e" if day_change >= 0 else "#ef4444"
            change_arrow  = "▲" if day_change >= 0 else "▼"

            period_high = processed["High"].max()
            period_low  = processed["Low"].min()
            avg_volume  = processed["Volume"].mean()

            m1, m2, m3, m4 = st.columns(4)

            def metric_card(label, value, sub=None, sub_color="#64748b"):
                sub_html = f'<div style="color:{sub_color};font-size:0.85rem;font-weight:600;margin-top:0.3rem;">{sub}</div>' if sub else ""
                return f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    {sub_html}
                </div>"""

            with m1:
                st.markdown(metric_card(
                    "Current Price",
                    f"${current_price:,.2f}",
                    f"{change_arrow} ${abs(day_change):.2f} ({day_pct:+.2f}%)",
                    change_color
                ), unsafe_allow_html=True)

            with m2:
                st.markdown(metric_card(
                    f"{period_label} High",
                    f"${period_high:,.2f}"
                ), unsafe_allow_html=True)

            with m3:
                st.markdown(metric_card(
                    f"{period_label} Low",
                    f"${period_low:,.2f}"
                ), unsafe_allow_html=True)

            with m4:
                vol_str = f"{avg_volume/1e6:.1f}M" if avg_volume >= 1e6 else f"{avg_volume/1e3:.1f}K"
                st.markdown(metric_card(
                    "Avg Daily Volume",
                    vol_str
                ), unsafe_allow_html=True)

            # ── Charts ──────────────────────────────────────────────────────
            st.markdown('<div class="section-title">📊 Price Trend</div>', unsafe_allow_html=True)
            tab1, tab2, tab3, tab4 = st.tabs(["Line Chart", "Candlestick", "Volume", "Moving Averages"])

            with tab1:
                fig = plot_price_trend(processed, symbol, period_label)
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                fig = plot_candlestick(processed, symbol)
                st.plotly_chart(fig, use_container_width=True)

            with tab3:
                fig = plot_volume(processed, symbol)
                st.plotly_chart(fig, use_container_width=True)

            with tab4:
                fig = plot_moving_averages(indicators, symbol)
                st.plotly_chart(fig, use_container_width=True)

            # ── Historical Data Table ────────────────────────────────────────
            st.markdown('<div class="section-title">📋 Historical Data</div>', unsafe_allow_html=True)
            display_df = processed[["Open","High","Low","Close","Volume","Daily Change %"]].copy()
            display_df = display_df.sort_index(ascending=False)
            display_df.index = display_df.index.strftime("%Y-%m-%d")
            display_df = display_df.round(2)
            st.dataframe(display_df, use_container_width=True, height=300)

            # ── Company Info ─────────────────────────────────────────────────
            if info and not info_error:
                st.markdown('<div class="section-title">🏢 Company Information</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                fields_left = [
                    ("Market Cap",      f"${info.get('marketCap', 0)/1e9:.2f}B" if info.get('marketCap') else "N/A"),
                    ("P/E Ratio",       f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get('trailingPE'), float) else "N/A"),
                    ("52W High",        f"${info.get('fiftyTwoWeekHigh', 'N/A')}"),
                    ("52W Low",         f"${info.get('fiftyTwoWeekLow', 'N/A')}"),
                    ("Dividend Yield",  f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A"),
                ]
                fields_right = [
                    ("Industry",        info.get("industry", "N/A")),
                    ("Country",         info.get("country", "N/A")),
                    ("Currency",        info.get("currency", "N/A")),
                    ("Beta",            f"{info.get('beta', 'N/A')}"),
                    ("Employees",       f"{info.get('fullTimeEmployees', 'N/A'):,}" if isinstance(info.get('fullTimeEmployees'), int) else "N/A"),
                ]

                def render_info(fields):
                    html = ""
                    for label, val in fields:
                        html += f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">{val}</span></div>'
                    st.markdown(f'<div style="background:#111827;border:1px solid #1e293b;border-radius:12px;padding:1rem 1.5rem;">{html}</div>', unsafe_allow_html=True)

                with c1: render_info(fields_left)
                with c2: render_info(fields_right)

else:
    # Landing state
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;color:#334155;">
        <div style="font-size:4rem;margin-bottom:1rem;">🔍</div>
        <div style="font-size:1.2rem;color:#475569;margin-bottom:0.5rem;">Enter a stock symbol above to get started</div>
        <div style="font-size:0.85rem;">Try AAPL · TSLA · GOOGL · MSFT · AMZN</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    StockLens · Data provided by Yahoo Finance via yfinance · For educational purposes only<br>
    Built with Streamlit · Python · Plotly
</div>
""", unsafe_allow_html=True)
