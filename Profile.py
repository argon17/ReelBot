from bs4 import BeautifulSoup
import time

class Reel:
    def __init__(self, reelURL, views, viewsInt):
        self.URL = reelURL
        self.views = views
        self.viewsInt = viewsInt


class Profile:
    def __init__(self, username):
        self.username = username
    
    def getReels(self, driver, maxAmt = None, maxFailedScroll = 300):
        JS_SCROLL_SCRIPT = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"
        JS_PAGE_LENGTH_SCRIPT = "var lenOfPage=document.body.scrollHeight; return lenOfPage;"
        driver.get(f"https://www.instagram.com/{self.username}/reels/")
        time.sleep(5)

        # list of Reel objects
        reels = []
        scrollAttempts = 0
        lastPosition = driver.execute_script(JS_PAGE_LENGTH_SCRIPT)
        scrolling = True

        def getViewsInt(views):
            views = views.replace(',', '')
            toMultiply = 1
            if not views.isnumeric():
                multiplier = views[-1]
                toMultiply = 1e3 if multiplier == 'k' else 1e6
                views = views[:-1]
            return int(float(views) * toMultiply)

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
                if reel.URL not in [r.URL for r in reels]:
                    reels.append(reel)
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
        soup = BeautifulSoup(sourceData, 'html.parser')
        anchorTags = soup.find_all("a")
        reelTags = [tag for tag in anchorTags if tag.find("div", {"class": "lVhHa _hpij"})]
        return reelTags