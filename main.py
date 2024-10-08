#!/usr/bin/env python3
import logging
import spacy
import requests
import python-telegram-bot
from bs4 import BeautifulSoup
from telegram import Update
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TimedOut

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
    await update.message.reply_text(
        'Hi! I can tell you about South Africa\'s Olympic medals. '
        'Use /medals to get the latest info. '
    )

async def medals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Please type the type of medal you want to see (gold, silver, bronze, or all).')

async def medal_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_input = update.message.text.lower()
        logger.info(f"User input: {user_input}")
        doc = nlp(user_input)
        medal_type = None
        for token in doc:
            if token.lemma_ in ["gold", "silver", "bronze", "all"]:
                medal_type = token.lemma_
                break
        
        medals = get_medal_data()
        logger.info(f"Medals data: {medals}")
        if medal_type in medals or medal_type == "all":
            message = "South Africa's Olympic Medals:\n"
            if medal_type == "all":
                for medal_type, winners in medals.items():
                    count = len(winners)
                    message += f"\n{medal_type.capitalize()} Medals: {count}\n"
                    for athlete, sport in winners:
                        message += f"- {athlete} in {sport}\n"
            else:
                winners = medals[medal_type]
                count = len(winners)
                message += f"\n{medal_type.capitalize()} Medals: {count}\n"
                for athlete, sport in winners:
                    message += f"- {athlete} in {sport}\n"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text('Invalid input. Please type gold, silver, bronze, or all.')
    except TimedOut:
        await handle_timeout(update)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

async def handle_timeout(update: Update) -> None:
    await update.message.reply_text("The request timed out. Please try again later.")

async def extract_entities(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    doc = nlp(user_input)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if entities:
        response = "I found the following entities:\n"
        response += "\n".join([f"{text} ({label})" for text, label in entities])
    else:
        response = "I didn't find any entities."
    await update.message.reply_text(response)

def main() -> None:
    application = Application.builder().token("7350630932:AAE5k-4YKBdTOOxrwoRWqWFuaccnVN1YXw8").read_timeout(20).write_timeout(20).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("medals", medals))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, medal_type))
    
    application.run_polling()

if __name__ == "__main__":
    main()    
