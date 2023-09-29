from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from passwords import password
from passwords import username
import time

user = input('enter twitter username: @')

web = 'https://twitter.com/'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(web)
driver.maximize_window()
# time.sleep(5)

# login btn
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div').click()
# gives model time to load
time.sleep(5)

# find user login field and enter username then press next
user_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
user_field.send_keys(username)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div').click()
# gives model time to load
time.sleep(5)

# enter password in the password field then press login
password_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
password_field.send_keys(password)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()
# give time for site to load
time.sleep(10)

search_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")
search_field.send_keys(user)
search_field.send_keys(Keys.ENTER)
time.sleep(5)

# clicks people btn to ensure bot presses a user
people_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span')
people_btn.click()
time.sleep(5)

# clicks user and lands on page to begin scraping.
user_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div[1]')
user_btn.click()
time.sleep(5)

user_data = []
text_data = []

# scraper
tweets = driver.find_elements(By.XPATH,"//article[@role='article']")

for tweet in tweets:
    x_name = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
    text = tweet.find_element(By.XPATH, './/div[@lang]').text
    text = " ".join(text.split())
    user_data.append(x_name)
    text_data.append(text)

driver.quit()

df_tweets = pd.DataFrame({'user': user_data, 'tweet': text_data})
df_tweets.to_csv(user+'_tweets.csv', index=False)
print(df_tweets)
