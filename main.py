import logging
import requests
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

server = Flask('')

@server.route('/')
def home():
    return "Bot is Online and Running!"

def run():

    port = int(os.environ.get("PORT", 8080))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()


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
    
    # Sora Link ဟုတ်မဟုတ် စစ်မယ်
    if user_text.startswith("http") and "sora" in user_text.lower():
        status_msg = await update.message.reply_text("🚀 Processing your Sora video link, please wait...")
        
        api_url = "https://online.fliflik.com/get-video-link"
        payload = {"url": user_text}

        try:
          
            response = requests.post(api_url, json=payload, timeout=120)
            data = response.json()
            
            video_url = data.get('download_url') or data.get('url') or data.get('data')

            if video_url:
                await update.message.reply_video(video=video_url, caption="✅ Your Sora video is ready!")
            else:
                await update.message.reply_text("❌ Sorry, the API could not extract the video link. It might be private.")
        except Exception as e:
            await update.message.reply_text("❌ System Error: Server is busy or connection timeout. Please try again in 1 minute.")
        
        await status_msg.delete()
    
    elif user_text == "/start":
        await start(update, context)
    else:
       
        if not user_text.startswith("/"):
            await update.message.reply_text("⚠️ Please send a valid Sora video URL.\n\nContact: @Rowan_Elliss")

def main():
    keep_alive()
    
    print("Bot is starting with Web Server...")
    bot_app = Application.builder().token(BOT_TOKEN).build()
    
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    bot_app.run_polling()
if __name__ == "__main__":
    main()
