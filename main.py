import logging
import requests
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# --- FLASK WEB SERVER (KEEP-ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Online and Running!"

def run():
    # Render က Port ကို အလိုလိုပေးလိမ့်မယ်
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- TELEGRAM BOT LOGIC ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "8330993145:AAHyY-REuWa2P1YrcUyW26cs7-85vCjjYkY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Welcome to Sora Video Downloader!\n\n"
        "Please send me a Sora video link (e.g., sora.chatgpt.com) to download.\n\n"
        "📩 Contact Info: @Rowan_Elliss"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text.startswith("http"):
        if "sora" in user_text.lower():
            status_msg = await update.message.reply_text("🚀 Processing your Sora video link, please wait...")
            api_url = "https://online.fliflik.com/get-video-link"
            payload = {"url": user_text}

            try:
                response = requests.post(api_url, json=payload, timeout=45)
                data = response.json()
                video_url = data.get('download_url') or data.get('url') or data.get('data')

                if video_url:
                    await update.message.reply_video(video=video_url, caption="✅ Your Sora video is ready!")
                else:
                    await update.message.reply_text("❌ Sorry, I couldn't download this Sora link.")
            except Exception as e:
                await update.message.reply_text("❌ System Error: Server is busy. Try again later.")
            
            await status_msg.delete()
        else:
            await update.message.reply_text("⚠️ This downloader only supports Sora links.")
    elif user_text == "/start":
        await start(update, context)
    else:
        await update.message.reply_text("⚠️ Please send a valid Sora video URL.\n\nContact: @Rowan_Elliss")

def main():
    # ၁။ Web Server ကို အရင်စနှိုးမယ်
    keep_alive()
    
    # ၂။ Bot ကို စနှိုးမယ်
    print("Bot is starting with Keep-Alive Server...")
    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.run_polling()

if __name__ == "__main__":
    main()