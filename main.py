from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import os, requests, datetime

app = FastAPI()

# Разрешаем запросы с любых источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send")
async def send(
    name: str = Form(...),
    car: str = Form(...),
    works: str = Form(...),
    phone: str = Form(...)
):
    if name.strip().lower() in ["ping", "пинг"]:
        return {"ok": True, "message": "Ping detected. No notification sent."}

   msg = f"""
📢 <b>НОВАЯ ЗАЯВКА НА СЕРВИС!</b>

👤 <b>Клиент:</b> {name}
🚗 <b>Автомобиль:</b> {car}
🔧 <b>Работы:</b> {works}
📞 <b>Телефон:</b> <code>{phone}</code>

⏰ <i>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</i>

⚠️ <b>Требуется срочная обработка!</b>
""".encode('utf-8').decode()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "HTML"
        }, timeout=10)
        return {"ok": True}
    except Exception as e:
        print("Ошибка при отправке в Telegram:", e)
        return {"ok": True}
