from __future__ import annotations 
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Reel:
    def __init__(self, reelURL: str, views: str, viewsInt:  int):
        """
        Initializes an instance of Reel class

        Args:
            reelURL (str): URL for the reel
            views (str): views in type str
            viewsInt (int): views in type int
        """

        self.URL = reelURL
        self.views = views
        self.viewsInt = viewsInt


class Profile:
    def __init__(self, username: str):
        """
        Initializes an instance of Profile class

        Args:
            username (str): instagram username for the profile
        """

        self.username = username
    
    def getReels(self, driver: webdriver, maxAmt: int = 0, maxFailedScroll: int = 100) -> List[Reel]:
        """
        Returns Reel objects from profile scraped using a webdriver

        Args:
            driver (webdriver): Selenium webdriver for rendering JavaScript and loading dynamic
            content
            maxAmt (int, optional): Maximum amount of reels to return. Defaults to 0.
            maxFailedScroll (int, optional): Maximum amount of scroll attempts before stopping if scroll is stuck. Defaults to 100.

        Returns:
            List[Reel]: reel objects sorted according to views
        """

        JS_SCROLL_SCRIPT = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"
        JS_PAGE_LENGTH_SCRIPT = "var lenOfPage=document.body.scrollHeight; return lenOfPage;"
        driver.get(f"https://www.instagram.com/{self.username}/reels/")
        time.sleep(5)

        # list of Reel objects
        reels = []
        scrollAttempts = 0
        lastPosition = driver.execute_script(JS_PAGE_LENGTH_SCRIPT)
        scrolling = True

        def getViewsInt(views: str) -> int:
            """
            Returns views converted to type int

            Args:
                views (str): views in type str

            Returns:
                [int]: views in type int
            """

            views = views.replace(',', '')
            toMultiply = 1
            if not views.isnumeric():
                multiplier = views[-1]
                toMultiply = 1e3 if multiplier == 'k' else 1e6
                views = views[:-1]
            return int(float(views) * toMultiply)

        alreadyPresent = set()

        while scrolling:
            # print('scrolling')
            currentPosition = driver.execute_script(JS_SCROLL_SCRIPT)
            sourceData = driver.page_source
            reelTags = self.getReelTags(sourceData)

            for reelTag in reversed(reelTags):
                reelURL = f"https://www.instagram.com{reelTag['href']}"
                views = reelTag.find_all('span')[-1].text
                viewsInt = getViewsInt(views)
                reel = Reel(reelURL, views, viewsInt)
                if reel.URL not in alreadyPresent:
                    reels.append(reel)
                    alreadyPresent.add(reel.URL)
                else:
                    break
            # print(f"currentPosition: {currentPosition}, lastPosition: {lastPosition}")
            if currentPosition == lastPosition:
                scrollAttempts += 1
                if scrollAttempts > maxFailedScroll:
                    print('Failed Scroll Limit Exceeded.')
                    scrolling = False
            else:
                scrollAttempts = 0
                lastPosition = currentPosition
 
            if len(reels) >= maxAmt:
                break


        print(f'Total Reels Found: {len(reels)}')
        reels = reels[:maxAmt]
        return sorted(reels, key = lambda x: x.viewsInt, reverse = True)


    def getReelTags(self, sourceData):
        """
        Separates the HTML and parse the BeautifulSoup for every reel
        """
        
        soup = BeautifulSoup(sourceData, 'html.parser')
        anchorTags = soup.find_all("a")
        reelTags = [tag for tag in anchorTags if tag.find("div", {"class": "lVhHa _hpij"})]
        return reelTags