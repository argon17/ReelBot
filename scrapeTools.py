from Profile import Profile
from selenium.webdriver.common.by import By
from Lol import BASE_URL, USERNAME, PASSWORD
from random import randint
import time


def getRandomTime():
    randTime = randint(1, 3)
    return randTime

def login(browser):
    browser.get(BASE_URL)
    browser.implicitly_wait(300)

    username_input = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = browser.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    print('Credentials Entered.')
    time.sleep(getRandomTime())

    login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    print('Logging In.')
    time.sleep(getRandomTime())

    not_now_btn = browser.find_element(By.XPATH, '//button[text()="Not Now"]')
    not_now_btn.click()

    print('Login Successful')
    time.sleep(getRandomTime())


def getText(driver, PROFILE, allMillion = False):

    login(driver)

    profile = Profile(PROFILE)
    reels = profile.getReels(driver, maxAmt = 200)
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