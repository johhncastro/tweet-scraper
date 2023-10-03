
# Twitter Scraper Documentation

## Introduction
This Python script is designed to scrape tweets from a specific Twitter user's profile. It utilizes the Selenium library for web automation and scraping, and it requires a web driver for Google Chrome. This documentation provides instructions on how to set up and use the script.

## Prerequisites
Before using this script, you need to have the following software and libraries installed:

1. Python 3.x
2. Selenium (Python library)
3. Pandas (Python library)
4. Chrome web browser
5. ChromeDriver

Make sure to install the required Python libraries using `pip` if you haven't already:

```bash
pip install selenium pandas webdriver-manager
```

Additionally, ensure that you have ChromeDriver installed and available in your system's PATH. You can download it from [here](https://sites.google.com/chromium.org/driver/).

## Usage

1. Clone or download the script to your local machine.

2. Create a file named `passwords.py` in the same directory as the script. Inside `passwords.py`, define your Twitter username and password as follows:

```python
username = "your_twitter_username"
password = "your_twitter_password"
```

**Note:** Storing your password in a script is not recommended for security reasons. Consider using alternative authentication methods when building a production-ready application.

3. Open a terminal or command prompt and navigate to the directory where the script is located.

4. Run the script 

5. Follow the on-screen prompts in the terminal:
   - Enter the Twitter username (without the "@" symbol) for the profile you want to scrape.
   - Choose whether you want to export the scraped data to CSV or JSON format by typing `csv` or `json` when prompted.

6. The script will start scraping tweets from the specified user's profile. It will display progress information in the terminal, and when the scraping is complete, it will save the data in the chosen format (CSV or JSON) with the filename based on the Twitter username.

## Output

The script will generate an output file in either CSV or JSON format, depending on your choice. The filename will be based on the Twitter username you provided during the execution.

- CSV Output: A CSV file containing two columns: `user` and `text`. Each row represents a scraped tweet, where `user` is the Twitter username of the author, and `text` is the content of the tweet.

- JSON Output: A JSON file containing an array of objects, where each object has two properties: `user` (the Twitter username) and `text` (the content of the tweet).

## Note
- The script may take some time to scrape tweets, depending on the number of tweets on the user's profile.
- Twitter's website structure and elements may change over time, which could impact the script's functionality. Be prepared to update the script accordingly if needed.




