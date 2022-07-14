from fake_useragent import UserAgent
# for automating chrome importing selenium
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
options = Options()
ua = UserAgent()
userAgent = ua.random
# print(userAgent)
options.add_argument(f'user-agent={userAgent}')
options.add_argument("--start-maximized")
options.add_argument('--headless')

def checkBSC(token):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # creating waiting element
    wait = WebDriverWait(driver, 10)
    driver.get(f'https://bscscan.com/dextracker?q={token}')
    
    myElem = wait.until(EC.presence_of_element_located((By.XPATH, '//table//td')))

    if driver.find_element(By.XPATH, '//table//td').text == 'No txn matching your filter.':
        return False
    else:
        return True

def checkETH(token):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # creating waiting element
    wait = WebDriverWait(driver, 10)
    url = f'https://etherscan.io/token/{token}#tokenTrade'
    driver.get(url)
    if driver.current_url == url:
        return True 
    else: return False
    
