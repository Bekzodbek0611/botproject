# Telegram Kalkulyator Bot

Telegram uchun kalkulyator boti. Inline tugmalar orqali yoki to'g'ridan-to'g'ri matematik ifoda yozib hisoblash mumkin.

## Xususiyatlari

- Inline kalkulyator (tugmali)
- To'g'ridan-to'g'ri matematik ifoda yozib hisoblash
- Qo'shish, ayirish, ko'paytirish, bo'lish
- Qavslarni qo'llab-quvvatlaydi
- Xavfsiz hisoblash (faqat arifmetik amallar)

## O'rnatish

```bash
pip install -r requirements.txt
cp .env.example .env
# .env faylga @BotFather dan olingan tokenni yozing
python bot.py
```

## Buyruqlar

- `/start` - Botni boshlash
- `/calc` - Kalkulyatorni ochish (inline tugmalar)
- `/help` - Yordam
