from fastapi import FastAPI, Form
import os, requests, datetime

app = FastAPI()

@app.post("/send")
async def send(
    name: str = Form(...),
    car: str = Form(...),
    works: str = Form(...),
    phone: str = Form(...)
):
    msg = f"""
📢 <b>НОВАЯ ЗАЯВКА НА СЕРВИС!</b>

👤 <b>Клиент:</b> {name}
🚗 <b>Автомобиль:</b> {car}
🔧 <b>Работы:</b> {works}
📞 <b>Телефон:</b> <code>{phone}</code>

⏰ <i>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</i>

⚠️ <b>Требуется срочная обработка!</b>
"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
    return {"ok": r.ok}
