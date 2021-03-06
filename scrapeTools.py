from profile import Profile

from selenium import webdriver
from selenium.webdriver.common.by import By
from constant import BASE_URL, USERNAME, PASSWORD
from random import randint
import time


def login(browser: webdriver):
    """
    [login into instagram]

    Args:
        browser (webdriver): Selenium webdriver for rendering JavaScript and loading dynamic content
    """

    browser.get(BASE_URL)
    time.sleep(1)

    username_input = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = browser.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    browser.save_screenshot('screenshots/s1.png')

    print('Credentials Entered.')

    login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    print('Logging In.')
    time.sleep(3)

    browser.save_screenshot('screenshots/s2.png')

    # For headless browsers, This is not needed
    # not_now_btn = browser.find_element(By.XPATH, '//button[text()="Not Now"]')
    # not_now_btn.click()

    print('Login Successful')


def getText(driver: webdriver, PROFILE: str, allMillion: bool = False) -> str:
    """
    Returns the text to send

    Args:
        driver (webdriver): Selenium webdriver for rendering JavaScript and loading dynamic content
        PROFILE (str): username for the profile
        allMillion (bool, optional): to scrape all million views reels or just top 10. Defaults to False.

    Returns:
        str: text to be sent
    """

    login(driver)

    profile = Profile(PROFILE)
    reels = profile.getReels(driver, maxAmt = 50)
    if not allMillion:
        reels = reels[:10]
    else:
        reels = list(filter(lambda x: x.views[-1] == 'm', reels))
    reels = reels[:50]
    if(len(reels) == 0):
        return f"Oops! couldn't find any results for your query"
    returnText = f"Here are the query results for {PROFILE}\n"
    serialNo = 1
    for reel in reels:
        print([reel.URL, reel.views])
        returnText += f"\n{serialNo}. {reel.URL} {reel.views}"
        serialNo += 1
    return returnText