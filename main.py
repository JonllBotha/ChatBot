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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching medals data: {e}")
        return {"gold": [], "silver": [], "bronze": []}
    
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
