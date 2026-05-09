import requests
import time

BOT_TOKEN = "8478231462:AAF5L2G4vHJqHZ2dS04prVoEVUZhPcwJYJg"
TARGET_CHAT_ID = 6462182499   # Vlasnikov chat (gdje narudžbe stižu)
YOUR_CHAT_ID = 6462182499     # Tvoj chat (ovdje ćeš dobijati kopije)

print("🛡️ Anti-Order Bot pokrenut - Brišem narudžbe i šaljem kopije tebi...")

offset = 0

while True:
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
            params={
                "offset": offset, 
                "timeout": 30,
                "allowed_updates": ["message"]
            }
        )
        
        data = response.json()
        
        if data.get("ok") and data.get("result"):
            for update in data["result"]:
                offset = update["update_id"] + 1
                
                if "message" in update:
                    message = update["message"]
                    message_id = message.get("message_id")
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")

                    # Ako je poruka u vlasnikovom chatu i sadrži narudžbu
                    if chat_id == TARGET_CHAT_ID and ("NOVA NARUDŽBA" in text or "🛒" in text):
                        
                        print(f"🔍 Pronađena narudžba | Brišem...")

                        # 1. Pošalji kopiju tebi
                        requests.get(
                            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                            params={
                                "chat_id": YOUR_CHAT_ID,
                                "text": f"🔴 **KOPIJA NARUDŽBE** (prije brisanja)\n\n{text}"
                            }
                        )

                        # 2. Obriši poruku iz vlasnikovog chata
                        requests.get(
                            f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                            params={"chat_id": chat_id, "message_id": message_id}
                        )

                        print(f"✅ Narudžba obrisana i kopija poslata tebi.")

        time.sleep(1.5)
        
    except Exception as e:
        print(f"Greška: {e}")
        time.sleep(5)
