import os
import re
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv, find_dotenv


# define path for .env that located in sentiment-dkk-semarang/.env
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ENV_PATH, '.env'), find_dotenv())

USERNAME = os.environ.get("INSTAGRAM_USERNAME")  # Set your INSTAGRAM_USERNAME in .env
PASSWORD = os.environ.get("INSTAGRAM_PASSWORD")  # Set your INSTAGRAM_PASSWORD in .env

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.instagram.com/")
time.sleep(3)

# login
time.sleep(5)
username = driver.find_element_by_css_selector("input[name='username']")
password = driver.find_element_by_css_selector("input[name='password']")
username.clear()
password.clear()
username.send_keys(USERNAME)  # input username
password.send_keys(PASSWORD)  # input password
login = driver.find_element_by_css_selector("button[type='submit']").click()

# close pop up
time.sleep(5)
notnow = driver.find_element_by_xpath(
    "//button[contains(text(), 'Not Now')]").click()

# open for each batch
n_batch = 11
batch_post = open(f"batch/{n_batch}.txt", "r").read().split('\n')

# scrape comment
raw_comment = []
raw_datetime = []
count = 1
for post in batch_post:
    # print(post)
    if not post: continue
    driver.get(post)
    # click button plus to get all comments
    while True:
        try:
            # driver.find_element_by_xpath("//button/span[@aria-label='Load more comments']").click()
            driver.find_element_by_xpath(
                '//button[@class="wpO6b  "]/div[@class="QBdPU "]/*[name()="svg"][@aria-label="Load more comments"]').click()
            time.sleep(3)
        except:
            break
    # get data
    try:
        data = driver.find_elements_by_xpath('//ul[@class="Mr508 "]')
        waktu = driver.find_elements_by_xpath('//div/li/div/div[1]/div[2]/div/div/a/time')
        for i in range(len(data)):
            raw_comment.append(data[i].text)
            raw_datetime.append(waktu[i].get_attribute("datetime"))
        print(f"Get data post-{count}: found {len(data)} comments")
        count += 1
    except:
        print('Tidak bisa ambil komentar!')
    # break
    time.sleep(5)
driver.close()

# PREPROCESS
df_data = pd.DataFrame(raw_comment, columns=['data'])
df_waktu = pd.DataFrame(raw_datetime, columns=['waktu'])

# split data to get view_reply
for i in df_data.index:
    view_reply = df_data['data'][i].split('\n')
    if re.search('View replies.+', view_reply[-1]):
        view_reply.pop(-1)
        df_data['data'][i] = view_reply
    else:
        df_data['data'][i] = view_reply

# split data into comments, username, and likes
usernames = []
comments = []
likes = []
for data in df_data.index:
    usernames.append(df_data['data'][data][0])
    comments.append(df_data['data'][data][1:-1])
    likes.append(df_data['data'][data][-1])

# extract likes
count = 0
for l in range(len(likes)):
    count += 1
    # print(count)
    try:
        like = likes[l].split('w')[1].split(' ')[0]
        if like == 'Reply':
            likes[l] = '0'
        else:
            likes[l] = like
    except:
        try:
            like = likes[l].split('d')[1].split(' ')[0]
            if like == 'Reply':
                likes[l] = '0'
            else:
                likes[l] = like
        except:
            try:
                like = likes[l].split('m')[1].split(' ')[0]
                if like == 'Reply':
                    likes[l] = '0'
                else:
                    likes[l] = like
            except:
                like = likes[l].split('h')[1].split(' ')[0]
                if like == 'Reply':
                    likes[l] = '0'
                else:
                    likes[l] = like

# join comments
for i in range(len(comments)):
    com_str = " ".join(comments[i])
    comments[i] = com_str

# extract time
waktu = []
for w in df_waktu.index:
    waktu_split = df_waktu['waktu'][w].split('T')[0]
    waktu.append(waktu_split)

# output
dict = {'usernames': usernames, 'comments': comments,
        'likes': likes, 'datetime': waktu}

df_output = pd.DataFrame(dict)

# create folder batch_csv
if not os.path.exists('batch_csv'):
    os.makedirs('batch_csv')

# export csv
df_output.to_csv(f"batch_csv/{n_batch}.csv", index=False)

print("Finished!")