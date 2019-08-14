#!/usr/bin/python3

import os, sys
from lxml import etree
from selenium import webdriver
import time
import random
import os.path
import urllib.request

target = "https://twitter.com/" + sys.argv[1]

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('window-size=1200x600')
chrome_options.add_argument('--disable-images')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

driver.get(target)

sel = etree.HTML(driver.page_source)

imageList = sel.xpath('//img[starts-with(@src, "https://pbs.twimg.com/media")]/@src')
prevLength = len(imageList)

maxTry, iTry = 3, 0
while iTry < maxTry:
    print('Scrolling down ...', end='')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    print('Wait ...')
    time.sleep(5)
    sel = etree.HTML(driver.page_source)
    imageList = sel.xpath('//img[starts-with(@src, "https://pbs.twimg.com/media")]/@src')
    if len(imageList) > prevLength:
        prevLength = len(imageList)
        print('No of Image = ', prevLength)
        time.sleep(random.randint(8, 17))
        iTry = 0
    else:
        iTry += 1
        print('touch bottom or network error: ', iTry)

folder = target.split('/')[-1]

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
        
