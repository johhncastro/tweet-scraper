from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from passwords import password
from passwords import username
import time

# running headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")


user = input('enter twitter username: @')

web = 'https://twitter.com/'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get(web)
driver.maximize_window()
print('initializing startup..')

# login btn
loginBtn = WebDriverWait(driver, 5).until(ec.presence_of_element_located(
    (By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div')))
loginBtn.click()
print('logging in...')

# find user login field and enter username then press next
user_field = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH,
                                                                            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')))
user_field.send_keys(username)
user_field.send_keys(Keys.ENTER)

# enter password in the password field then press login
password_field = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH,
                                                                                '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)

search_field = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                               "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")))
search_field.send_keys(user)
search_field.send_keys(Keys.ENTER)

# clicks people btn to ensure bot presses a user
people_btn = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH,
                                                                            '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span')))
people_btn.click()
print('login success....')

# clicks user and lands on page to begin scraping.
user_btn = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH,
                                                                          '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div[1]')))
user_btn.click()
print('profile loaded.....')

def get_tweet(element):
    try:
        x_name = element.find_element(By.XPATH, './/span[contains(text(), "@")]').text
        text = element.find_element(By.XPATH, './/div[@lang]').text
        tweets_data = [x_name, text]
    except:
        tweets_data = ['user', 'text']
    return tweets_data


user_data = []
text_data = []

# Define the number of times you want to scroll (adjust as needed)
scroll_count = 10

for _ in range(scroll_count):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait briefly for new content to load (you can adjust the sleep time)
    time.sleep(2)

# scraper
tweets = WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
if len(tweets) == 0:
    print("No tweets found.")
else:
    for tweet in tweets:
        tweet_list = get_tweet(tweet)
        user_data.append(tweet_list[0])
        text_data.append(" ".join(tweet_list[1].split()))

driver.quit()
print('scrape success......')
df_tweets = pd.DataFrame({'user': user_data, 'tweet': text_data})
df_tweets.to_csv(user + '_tweets.csv', index=False)
print(df_tweets)
