from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<string:symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        # Custom session banayein taaki Rate Limit na aaye
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, impervious) Chrome/120.0.0.0 Safari/537.36'
        })
        
        ticker = yf.Ticker(symbol, session=session)
        
        # 1-day fast period fetch
        data = ticker.history(period="1d")
        
        if data.empty:
            # Fallback agar history empty aaye
            data = ticker.history(period="5d")
            if data.empty:
                return jsonify({"error": "Data fetch nahi ho pa raha"}), 404

        current_price = float(data['Close'].iloc[-1])
        open_price = float(data['Open'].iloc[-1])
        change = current_price - open_price

        return jsonify({
            "symbol": symbol,
            "price": round(current_price, 2),
            "change": round(change, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500