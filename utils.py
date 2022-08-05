from selenium import webdriver  # for opening chrome
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By  # for locating elements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import \
    expected_conditions as EC  # condition that wait for element
from selenium.webdriver.support.ui import \
    WebDriverWait  # for wait if condition is not fulfilled
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time


import undetected_chromedriver as uc
from sys import platform
import os




def checkBSC(token):
    if platform != 'win32':
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox") 
        options.add_argument('--disable-gpu')
        driver = uc.Chrome(options=options, use_subprocess=True)
    else:
        driver = uc.Chrome(use_subprocess=True)
    # creating waiting element
    wait = WebDriverWait(driver, 10)
    driver.get(f'https://bscscan.com/dextracker?q={token}')
    
    myElem = wait.until(EC.presence_of_element_located((By.XPATH, '//table//td')))

    if driver.find_element(By.XPATH, '//table//td').text == 'No txn matching your filter.':
        driver.quit()        
        return False
    else:
        driver.quit()
        return True

def checkETH(token):
    if platform != 'win32':
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox") 
        options.add_argument('--disable-gpu')
        driver = uc.Chrome(options=options, use_subprocess=True)
    else:
        driver = uc.Chrome(use_subprocess=True)
    # creating waiting element
    wait = WebDriverWait(driver, 10)
    url = f'https://etherscan.io/token/{token}#tokenTrade'
    driver.get(url)
    if driver.current_url == url:
        driver.quit()
        return True 
    else: 
        driver.quit()
        return False
     