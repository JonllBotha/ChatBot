#!/usr/bin/env python3
import logging
import spacy
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TimedOut
import time

nlp = spacy.load("en_core_web_sm")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_medal_data():
    medals = {
        "gold": [("Tatjana Smith", "100m Breaststroke")],
        "silver": [("Tatjana Smith", "200m Breaststroke"), 
                   ("Akani Simbine, Shaun Maswanganyi, Sinesipho Dambile, Bradley Nkoana and Bayanda Walaza", "Men’s 4x100m relay"), 
                   ("Jo-Ane van Wyk", "Javelin")],
        "bronze": [("Blitz Bokke", "7s Rugby"), ("Alan Hatherly", "Men’s Cross-Country Cycling Mountain Bike race")]
    }
    return medals

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! I can tell you about South Africa\'s Olympic medals. Use /medals to get the latest info.')

async def medals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Please type the type of medal you want to see (gold, silver, bronze, or all).')

async def medal_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_input = update.message.text.lower()
        medals = get_medal_data()
        if user_input in medals or user_input == "all":
            message = "South Africa's Olympic Medals:\n"
            if user_input == "all":
                for medal_type, winners in medals.items():
                    count = len(winners)
                    message += f"\n{medal_type.capitalize()} Medals: {count}\n"
                    for athlete, sport in winners:
                        message += f"- {athlete} in {sport}\n"
            else:
             winners = medals[user_input]
            count = len(winners)
            message += f"\n{user_input.capitalize()} Medals: {count}\n"
            for athlete, sport in winners:
                message += f"- {athlete} in {sport}\n"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text('Invalid input. Please type gold, silver, bronze, or all.')
    except TimedOut:
        await handle_timeout(update)

async def handle_timeout(update: Update) -> None:
    await update.message.reply_text("The request timed out. Please try again later.")

def main() -> None:
    application = Application.builder().token("7350630932:AAE5k-4YKBdTOOxrwoRWqWFuaccnVN1YXw8").read_timeout(20).write_timeout(20).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("medals", medals))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, medal_type))
    
    application.run_polling()

if __name__ == "__main__":
    main()
