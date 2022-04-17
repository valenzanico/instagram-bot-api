import sys

sys.path.insert(1, '/home/eagle/sdnico/myapp/cassinelli/instagram-bot-api/src')

from instagrambotapi.login import login
from instagrambotapi.scraper import get_users_from_like
from dotenv import load_dotenv
import requests
import os
load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
session = login(username, password, headless=False, path={
            "browser": "./firefox/firefox",
            "driver": "./geckodriver"
        })

driver = session["driver"] 
sessionid = session["sessionid"]


print(str(get_users_from_like("https://www.instagram.com/p/CcbXl2yMtgF/", sessionid)))