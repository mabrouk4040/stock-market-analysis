"""
Member 3 – Visualization Developer
Responsibilities: Plotly charts — line, candlestick, volume, moving averages
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# ── Shared theme ─────────────────────────────────────────────────────────────
THEME = dict(
    bg        = "#0a0e1a",
    paper     = "#111827",
    grid      = "#1e293b",
    text      = "#94a3b8",
    accent    = "#38bdf8",
    green     = "#22c55e",
    red       = "#ef4444",
    purple    = "#818cf8",
    orange    = "#fb923c",
    font_mono = "JetBrains Mono, monospace",
)

LAYOUT_BASE = dict(
    paper_bgcolor = THEME["paper"],
    plot_bgcolor  = THEME["bg"],
    font          = dict(family="Space Grotesk, sans-serif", color=THEME["text"], size=12),
    margin        = dict(l=10, r=10, t=50, b=10),
    xaxis         = dict(gridcolor=THEME["grid"], showgrid=True, zeroline=False, linecolor=THEME["grid"]),
    yaxis         = dict(gridcolor=THEME["grid"], showgrid=True, zeroline=False, linecolor=THEME["grid"]),
    legend        = dict(bgcolor="rgba(0,0,0,0)", bordercolor=THEME["grid"]),
    hovermode     = "x unified",
)


def _apply_base(fig, title=""):
    layout = LAYOUT_BASE.copy()
    layout["title"] = dict(text=title, font=dict(size=14, color="#e2e8f0"), x=0)
    fig.update_layout(**layout)
    return fig


# ── 1. Line Chart ─────────────────────────────────────────────────────────────
def plot_price_trend(df: pd.DataFrame, symbol: str, period_label: str) -> go.Figure:
    """Gradient-filled line chart of closing prices."""
    fig = go.Figure()

    # Fill area
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        fill="tozeroy",
        fillcolor="rgba(56,189,248,0.08)",
        line=dict(color=THEME["accent"], width=2.5),
        name="Close Price",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Close: $%{y:,.2f}<extra></extra>",
    ))

    _apply_base(fig, f"{symbol} — Closing Price ({period_label})")
    fig.update_layout(showlegend=False)
    fig.update_yaxes(tickprefix="$", tickformat=",.2f")
    return fig


# ── 2. Candlestick Chart ──────────────────────────────────────────────────────
def plot_candlestick(df: pd.DataFrame, symbol: str) -> go.Figure:
    """OHLC candlestick with volume bars as a subplot."""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.03,
    )

    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"],  close=df["Close"],
        increasing=dict(line=dict(color=THEME["green"]), fillcolor=THEME["green"]),
        decreasing=dict(line=dict(color=THEME["red"]),   fillcolor=THEME["red"]),
        name="OHLC",
    ), row=1, col=1)

    # Volume bars
    colors = [THEME["green"] if c >= o else THEME["red"]
              for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"],
        marker_color=colors,
        opacity=0.6,
        name="Volume",
    ), row=2, col=1)

    _apply_base(fig, f"{symbol} — OHLC Candlestick")
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_yaxes(tickprefix="$", row=1)
    fig.update_yaxes(title_text="Volume", row=2)
    return fig


# ── 3. Volume Chart ───────────────────────────────────────────────────────────
def plot_volume(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Bar chart of trading volume with colour coding."""
    colors = [THEME["green"] if chg >= 0 else THEME["red"]
              for chg in df["Daily Change"].fillna(0)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        marker_color=colors,
        opacity=0.8,
        name="Volume",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Volume: %{y:,.0f}<extra></extra>",
    ))

    # Average line
    avg = df["Volume"].mean()
    fig.add_hline(
        y=avg,
        line=dict(color=THEME["purple"], width=1.5, dash="dot"),
        annotation_text=f"Avg: {avg/1e6:.1f}M",
        annotation_font_color=THEME["purple"],
    )

    _apply_base(fig, f"{symbol} — Trading Volume")
    fig.update_layout(showlegend=False)
    return fig


# ── 4. Moving Averages Chart ──────────────────────────────────────────────────
def plot_moving_averages(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Price with MA7, MA20, MA50 overlaid."""
    fig = go.Figure()

    # Close price (faint)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        line=dict(color="rgba(148,163,184,0.35)", width=1.5),
        name="Close",
        hovertemplate="$%{y:,.2f}<extra>Close</extra>",
    ))

    ma_cfg = [
        ("MA7",  THEME["accent"],  1.8),
        ("MA20", THEME["green"],   1.8),
        ("MA50", THEME["orange"],  1.8),
    ]
    for col, color, width in ma_cfg:
        if col in df.columns and df[col].notna().sum() > 1:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[col],
                line=dict(color=color, width=width),
                name=col,
                hovertemplate=f"$%{{y:,.2f}}<extra>{col}</extra>",
            ))

    # Bollinger Bands (subtle fill)
    if "BB_Upper" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_Upper"],
            line=dict(color="rgba(129,140,248,0.3)", width=1, dash="dot"),
            name="BB Upper",
            hovertemplate="$%{y:,.2f}<extra>BB Upper</extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_Lower"],
            line=dict(color="rgba(129,140,248,0.3)", width=1, dash="dot"),
            fill="tonexty",
            fillcolor="rgba(129,140,248,0.04)",
            name="BB Lower",
            hovertemplate="$%{y:,.2f}<extra>BB Lower</extra>",
        ))

    _apply_base(fig, f"{symbol} — Moving Averages & Bollinger Bands")
    fig.update_yaxes(tickprefix="$", tickformat=",.2f")
    return fig
