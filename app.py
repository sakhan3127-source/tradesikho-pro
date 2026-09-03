import os
from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
# Enable CORS for all domains so your mobile/web client can access it
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Online",
        "message": "Dhan Bot API Server is Running Live!"
    })

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        formatted_symbol = f"{symbol.upper().strip()}.NS"
        ticker = yf.Ticker(formatted_symbol)
        
        # 1-day minute candles fetch
        df = ticker.history(period="1d", interval="1m")
        if df.empty:
            df = ticker.history(period="5d", interval="1d")
            
        if df.empty:
            return jsonify({"error": "Stock symbol not found"}), 404

        latest = df.iloc[-1]
        price = round(float(latest['Close']), 2)
        high = round(float(latest['High']), 2)
        low = round(float(latest['Low']), 2)
        volume = int(latest['Volume'])
        
        prev_close = ticker.info.get('previousClose', price)
        chg_val = round(price - prev_close, 2)
        chg_pct = round((chg_val / prev_close) * 100, 2) if prev_close else 0.0
        is_up = chg_val >= 0

        return jsonify({
            "name": symbol.upper(),
            "ex": "NSE",
            "ltp": f"{price:,.2f}",
            "chg": f"{'+' if is_up else ''}₹{chg_val} ({'+' if is_up else ''}{chg_pct}%)",
            "isUp": is_up,
            "vol": f"{volume:,}",
            "high": f"₹{high:,.2f}",
            "low": f"₹{low:,.2f}",
            "vwap": f"₹{price:,.2f}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Cloud environments use dynamic PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)