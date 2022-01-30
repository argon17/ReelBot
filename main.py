from pyrogram import Client, filters
from constant import BOT_TOKEN, TELEGRAM_USERNAME, CHROME_DRIVER_PATH, API_ID, API_HASH
from scrapeTools import getText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

bot = Client(
    "noobBot",
    api_id = API_ID,
    api_hash = API_HASH,
    bot_token = BOT_TOKEN
)

def getDriver():
    """
    return webdriver object
    """

    options = webdriver.ChromeOptions()
    s = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service = s, options = options)
    return driver


@bot.on_message(filters.command('getTop') & filters.chat(TELEGRAM_USERNAME))
async def handleGet(bot, message):
    """
    Handles getTop command
    """

    driver = getDriver()
    keyword = message.text[30:message.text.find('?utm_medium=copy_link')]
    textMessage = getText(driver, keyword)
    driver.close()
    await message.reply(textMessage)


@bot.on_message(filters.command('getAll') & filters.chat(TELEGRAM_USERNAME))
async def handleGet(bot, message):
    """
    Handles getAll command
    """

    driver = getDriver()
    keyword = message.text[30:message.text.find('?utm_medium=copy_link')]
    textMessage = getText(driver, keyword, allMillion = True)
    driver.close()
    await message.reply(textMessage)

if __name__=='__main__':
    bot.run()
