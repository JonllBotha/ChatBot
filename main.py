import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TimedOut
import spacy
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
    try:
        medals = get_medal_data()
        message = "South Africa's Olympic Medals:\n"
        for medal_type, winners in medals.items():
            count = len(winners)
            message += f"\n{medal_type.capitalize()} Medals: {count}\n"
            for athlete, sport in winners:
                message += f"- {athlete} in {sport}\n"
        await update.message.reply_text(message)
        time.sleep(1)
    except TimedOut:
        await update.message.reply_text("The request timed out. Please try again later.")

def main() -> None:
    application = Application.builder().token("7350630932:AAE5k-4YKBdTOOxrwoRWqWFuaccnVN1YXw8").read_timeout(20).write_timeout(20).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("medals", medals))
    
    application.run_polling()

if __name__ == '__main__':
    main()

