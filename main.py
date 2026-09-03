import threading
import time
import requests
import random
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# App Global State
app_state = {
    "is_bot_running": False,
    "trading_mode": "PAPER",  # PAPER or LIVE
    "telegram_token": "",
    "telegram_chat_id": "",
    "virtual_balance": 100000.0,
    "active_position": None,  # None or dict
    "order_history": [],
    "dhan_client_id": "",
    "dhan_access_token": ""
}

class SettingsModel(BaseModel):
    telegram_token: str
    telegram_chat_id: str
    dhan_client_id: str = ""
    dhan_access_token: str = ""

def send_telegram(message):
    """Sends Instant Trade Alerts to Mobile Phone via Telegram"""
    if not app_state["telegram_token"] or not app_state["telegram_chat_id"]:
        return
    url = f"https://api.telegram.org/bot{app_state['telegram_token']}/sendMessage"
    payload = {
        "chat_id": app_state["telegram_chat_id"],
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Alert Error:", e)

def paper_trading_engine():
    """Simulated Live Algo Trading Bot Engine"""
    send_telegram("🚀 *DHAN AUTO-BOT STARTED*\nMode: Paper Trading (Virtual Funds)\nBalance: ₹1,00,000")
    
    symbols = ["NIFTY 50", "BANKNIFTY", "TATA MOTORS", "RELIANCE"]
    
    while app_state["is_bot_running"]:
        try:
            symbol = random.choice(symbols)
            simulated_price = round(random.uniform(24000, 24500), 2)
            
            # Simulated Algo Logic
            if app_state["active_position"] is None:
                # BUY CONDITION TRIGGERED
                app_state["active_position"] = {
                    "symbol": symbol,
                    "buy_price": simulated_price,
                    "qty": 25,
                    "time": time.strftime("%H:%M:%S")
                }
                
                msg = (
                    f"🟢 *DHAN BOT: VIRTUAL BUY ORDER*\n"
                    f"───────────────────────────\n"
                    f"📈 Stock/Index: *{symbol}*\n"
                    f"💰 Buy Price: ₹{simulated_price}\n"
                    f"📊 Quantity: 25 Lots\n"
                    f"⚡ Mode: Virtual Paper Trade"
                )
                send_telegram(msg)
                app_state["order_history"].append({"type": "BUY", "symbol": symbol, "price": simulated_price, "qty": 25})
                
            else:
                # SELL CONDITION TRIGGERED
                pos = app_state["active_position"]
                sell_price = round(simulated_price + random.uniform(-50, 80), 2)
                pnl = round((sell_price - pos["buy_price"]) * pos["qty"], 2)
                app_state["virtual_balance"] += pnl
                
                pnl_symbol = "🟩 Profit" if pnl >= 0 else "🟥 Loss"
                msg = (
                    f"🔴 *DHAN BOT: VIRTUAL SELL / EXIT*\n"
                    f"───────────────────────────\n"
                    f"📉 Stock/Index: *{pos['symbol']}*\n"
                    f"💵 Buy Price: ₹{pos['buy_price']}\n"
                    f"💵 Sell Price: ₹{sell_price}\n"
                    f"📈 P&L: *{pnl_symbol} ₹{pnl}*\n"
                    f"💼 Total Balance: ₹{round(app_state['virtual_balance'], 2)}"
                )
                send_telegram(msg)
                app_state["order_history"].append({"type": "SELL", "symbol": pos['symbol'], "price": sell_price, "qty": 25, "pnl": pnl})
                app_state["active_position"] = None

            time.sleep(15)  # Interval
        except Exception as e:
            print("Engine Error:", e)
            time.sleep(5)

@app.post("/api/save-settings")
def save_settings(data: SettingsModel):
    app_state["telegram_token"] = data.telegram_token
    app_state["telegram_chat_id"] = data.telegram_chat_id
    app_state["dhan_client_id"] = data.dhan_client_id
    app_state["dhan_access_token"] = data.dhan_access_token
    
    if data.telegram_token and data.telegram_chat_id:
        send_telegram("✅ *Telegram Alerts Connected!* Dhan Bot Ready.")
    return {"status": "success", "message": "Settings Saved"}

@app.post("/api/bot/start")
def start_bot():
    if not app_state["is_bot_running"]:
        app_state["is_bot_running"] = True
        thread = threading.Thread(target=paper_trading_engine)
        thread.start()
        return {"status": "started"}
    return {"status": "already_running"}

@app.post("/api/bot/stop")
def stop_bot():
    if app_state["is_bot_running"]:
        app_state["is_bot_running"] = False
        send_telegram("🛑 *DHAN BOT PAUSED*\nPaper Trading Session Ended.")
    return {"status": "stopped"}

@app.get("/api/dashboard-data")
def get_dashboard_data():
    return {
        "bot_running": app_state["is_bot_running"],
        "balance": round(app_state["virtual_balance"], 2),
        "active_position": app_state["active_position"],
        "history": app_state["order_history"][-5:]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    