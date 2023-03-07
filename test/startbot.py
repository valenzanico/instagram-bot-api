from instagrambotapi import Bot


BROWSER_PATH = "D:\\myapp\\cassinelli\\instagram-direct-bot_dekstop\\dist\\Firefox_bin\\firefox.exe"
DRIVER_PATH = "D:\\myapp\\cassinelli\\instagram-direct-bot_dekstop\\dist\\webdriver\\geckodriver.exe"
HEADLESS = False
PROXY = None
USERNAME = ""
PASSWORD = ""

if __name__ == "__main__":
    bot = Bot(headless=HEADLESS, proxy=PROXY, path={"browser": BROWSER_PATH, "driver": DRIVER_PATH})
    bot.login(USERNAME, PASSWORD)
    bot.send_dm("cassinellimarco.official", "Sono un cazzo di bot, è funziono zio porco")