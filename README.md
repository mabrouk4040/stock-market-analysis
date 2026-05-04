# 📈 StockLens — Stock Market Analysis System

> **Course**: Current Issues in IT
> **University**: Canadian International College (C.I.C)
> **Supervisor**: Dr. Mohamed Khalaf

---

## 👥 Team Members

| Name | Student ID | Role |
|------|-----------|------|
| Mohamed Abo-Bakr Ahmed | 202207062 | Backend Developer & Project Lead — API integration, validation, error handling, Streamlit UI |
| Ahmed Khaled Ahmed | 202206515 | Data & Visualization Developer — Data processing, indicators, Plotly charts |

---

## 🚀 Quick Setup

### 1. Install dependencies
```bash
pip install streamlit yfinance pandas plotly numpy
```

### 2. Run the app
```bash
python -m streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## 📁 Project Structure

```
stock_app/
├── app.py              # Streamlit UI + main entry point
├── backend.py          # API integration, validation, error handling
├── data_processing.py  # Data cleaning, indicators (MA, RSI, MACD...)
├── visualization.py    # All Plotly charts
└── README.md
```

---

## ✨ Features

- 🔍 **Stock search** by symbol (AAPL, TSLA, GOOGL, etc.)
- ⏱️ **5 time periods**: 1 Week · 1 Month · 3 Months · 6 Months · 1 Year
- 📊 **4 interactive charts**: Line · Candlestick · Volume · Moving Averages + Bollinger Bands
- 📋 **Historical data table** with daily OHLCV + change %
- 🏢 **Company info**: Market cap, P/E ratio, sector, 52W high/low, employees
- ⚠️ **Error handling**: invalid symbols, API failures, empty data
- 🌙 **Dark themed UI**

---

## 🧪 Testing

Test with valid symbols:
```
AAPL   → Apple Inc.
TSLA   → Tesla
GOOGL  → Alphabet
MSFT   → Microsoft
AMZN   → Amazon
```

Test with invalid inputs:
```
XXXXXX   → Too long — validation error
123      → Numbers — validation error
""       → Empty — warning message
FAKESYM  → Valid format but no data — API error
```

---

## 🛠️ Tools & Technologies

| Library | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `yfinance` | Yahoo Finance stock data API |
| `pandas` | Data handling and processing |
| `plotly` | Interactive charts |
| `numpy` | Numerical computations |

---

## ⚠️ Disclaimer
This application is for **educational purposes only**. It is not financial advice.
Data is provided by Yahoo Finance and may be delayed.
