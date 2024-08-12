import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import spacy

nlp = spacy.load("en_core_web_sm")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_medals():
    url = "https://olympics.com/en/news/olympic-games-paris-2024-south-africa-s-medal-winners-full-list"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    medals = {"gold": [], "silver": [], "bronze": []}

    for medal_type in medals.keys():
        medal_elements = soup.find_all("div", class_=f"medal-{medal_type}")
        for element in medal_elements:
            athlete = element.find("span", class_="athlete-name").text
            sport = element.find("span", class_="sport-name").text
            medals[medal_type].append((athlete, sport))
    
    return medals

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! I can tell you about South Africa\'s Olympic medals. Use /medals to get the latest info.')

async def medals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    medals = scrape_medals()
    message = "South Africa's Olympic Medals:\n"
    for medal_type, winners in medals.items():
        message += f"\n{medal_type.capitalize()} Medals:\n"
        for athlete, sport in winners:
            message += f"- {athlete} in {sport}\n"
    await update.message.reply_text(message)

def main() -> None:
    application = Application.builder().token("7350630932:AAE5k-4YKBdTOOxrwoRWqWFuaccnVN1YXw8").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("medals", medals))
    
    application.run_polling()

if __name__ == '__main__':
    main()
