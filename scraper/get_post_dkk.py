from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from instascrape import Profile
import requests
import os
from dotenv import load_dotenv, find_dotenv

# define path for .env that located in sentiment-dkk-semarang/.env
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ENV_PATH, '.env'), find_dotenv())


# Creating our webdriver
driver = Chrome(ChromeDriverManager().install())
session: requests.Session = None
SESSIONID = os.environ.get("INSTAGRAM_SESSIONID")  # Set your INSTAGRAM_SESSIONID in .env
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
           "cookie": f"sessionid={SESSIONID};"}

dkk = Profile("dkksemarang")
dkk.scrape(headers=headers)

# get posts
posts = dkk.get_posts(webdriver=driver, login_first=True, login_pause=15, scrape_pause=10)

# save result to text file
print('write post url to text..')
with open("instagram_posts.txt", 'a') as output:
    for i, post in enumerate(posts):
        output.write(f"https://www.instagram.com/p/{post.source}" + "\n")
print('success!')