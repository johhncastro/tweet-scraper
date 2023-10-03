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
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

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

print('initializing scrape...')
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
tweet_ids = set()
scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(
        ec.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
    print(len(tweets))
    for tweet in tweets[-15:]:
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(tweet_list[0])
            text_data.append(" ".join(tweet_list[1].split()))

    # get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scrolling = False
            break
        else:
            last_height = new_height
            break

driver.quit()
print('scrape complete')
data_type = input('Export data to CSV or JSON? (csv/json): ')

if data_type.lower() == 'csv':
    # export to CSV
    df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
    df_tweets.to_csv(user + '.csv', index=False)
    print('Data exported to CSV:', user + '.csv')
elif data_type.lower() == 'json':
    # export to JSON
    df_json = pd.DataFrame({'user':user_data, 'text': text_data})
    df_json.to_json(user + '.json', index=False)
    print('Data exported to JSON:', user + '.json')
else:
    print('Invalid export format. Please enter "csv" or "json".')
