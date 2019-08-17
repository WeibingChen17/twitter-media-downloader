#!/usr/bin/python3
import os, sys, time
import random
import os.path
import urllib.request
from distutils.spawn import find_executable
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TWITTER = "https://twitter.com/" 

class UrlNotExistException(Exception):
    def __init__(self):
        super("Url not accessible")

class ChromedriverNotExistException(Exception):
    def __init__(self):
        super('Chromedriver could not be found')

class TwitterDownloader:
    def __init__(self, targetURL):
        self.targetURL = targetURL
        response = urllib.request.urlopen(targetURL)
        if response.getcode() != 200:
            raise UrlNotExistException("Twitter account could not be reached")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('window-size=1200x600')
        chrome_options.add_argument('--disable-images')
        ChromedriverPath = find_executable('chromedriver')
        if len(ChromedriverPath) == 0:
            raise ChromedriverNotExistException();
        self.driver = webdriver.Chrome(ChromedriverPath, options=chrome_options)

    def run(self):
        self.driver.get(self.targetURL)
        sel = etree.HTML(self.driver.page_source)

        imageList = sel.xpath('//img[starts-with(@src, "https://pbs.twimg.com/media")]/@src')
        prevLength = len(imageList)

        maxTry, iTry = 3, 0
        while iTry < maxTry:
            print('Scrolling down ...', end='')
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            print('Wait ...')
            time.sleep(5)
            sel = etree.HTML(self.driver.page_source)
            imageList = sel.xpath('//img[starts-with(@src, "https://pbs.twimg.com/media")]/@src')
            if len(imageList) > prevLength:
                prevLength = len(imageList)
                print('No of Image = ', prevLength)
                time.sleep(random.randint(8, 17))
                iTry = 0
            else:
                iTry += 1
                print('touch bottom or network error: ', iTry)

        folder = self.targetURL.split('/')[-1]

        if not os.path.exists(folder):
            print('creating ', folder)
            os.mkdir(folder)

        for image in  imageList:
            image.strip()
            image.rstrip(':thumb')
            local = folder + '/' + image.split('/')[-1]
            if not os.path.exists(local):
                print('downloading ', image, ' to ', local)
                while True:
                    try:
                        urllib.request.urlretrieve(image, local)
                        break
                    except:
                        time.sleep(random.randint(5, 13))
                        print("try again to download. Crawling God bless you")
                        continue
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        sys.exit(1)
    targetURL = TWITTER + sys.argv[1]
    try:
        td = TwitterDownloader(targetURL)
        td.run()
    except UrlNotExistException as e:
        print(e)
    except Exception as e:
        print(e)
