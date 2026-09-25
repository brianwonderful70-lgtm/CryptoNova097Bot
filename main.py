import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", "8080"))
RAILWAY_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN")

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I am CryptoNova097Bot. 🚀\n"
        "Ready for advanced crypto management and security."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "More advanced features coming soon..."
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Placeholder for crypto price checking."""
    await update.message.reply_text("Crypto price integration is pending. Add your CoinGecko or Binance API logic here.")

def main() -> None:
    """Start the bot using webhooks."""
    if not TOKEN:
        logging.error("TELEGRAM_BOT_TOKEN environment variable is missing.")
        return

    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("price", price))

    # Set webhook if running on Railway
    if RAILWAY_URL:
        webhook_url = f"https://{RAILWAY_URL}/webhook"
        logging.info(f"Setting webhook to {webhook_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="webhook",
            webhook_url=webhook_url,
            secret_token=os.environ.get("WEBHOOK_SECRET"),
            drop_pending_updates=True
        )
    else:
        # Fallback for local testing (uses polling)
        logging.warning("RAILWAY_PUBLIC_DOMAIN not found. Falling back to polling.")
        application.run_polling()

if __name__ == "__main__":
    main()
