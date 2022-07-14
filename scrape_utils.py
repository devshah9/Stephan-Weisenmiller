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




import os 


# for heroku

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")



chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

def scrape_function_bsc(token):
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # creating waiting element
    wait = WebDriverWait(driver, 10)
    page_no = 1
    running = True
    min_filter = 0 
    total_rows = 100
    BIG_BUY = 0
    while running:

        url = f'https://bscscan.com/dextracker?q={token}&ps={total_rows}&p={page_no}'
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']//tbody//tr")))
        full_text_table = driver.find_elements(By.XPATH, "//div[@class='card-body']//tbody//tr")

        for i in full_text_table:
            each_row = i.text.replace('\n', ' ')
            each_row = each_row.split(' ')
            if (each_row[2] == 'secs') or (int(each_row[1]) <= 10 and (each_row[2] == 'min' or each_row[2] == 'mins')): 
                min_filter += 1
                if BIG_BUY < float(each_row[4].replace(',', '')) and (each_row[5] == 'WBNB'):
                    BIG_BUY = float(each_row[4].replace(',', ''))
                    GOT = f'{each_row[-4]} {each_row[-3]}'
                    TRX_HASH = each_row[0]
                    TRX_HASH_LINK =f'https://bscscan.com/tx/{TRX_HASH}'

                    # print(51, BIG_BUY, GOT)
                    # print(f"""SPENT : {BIG_BUY} BNB
# GOT : {each_row[-4]} {each_row[-3]} 
# BUYER POSITION: {each_row[1]} {each_row[2]} ago""")
        if (total_rows*page_no) != min_filter:
            running = False
        page_no +=1
    # print(57, BIG_BUY)

    if BIG_BUY:
        BIG_BUY = round(BIG_BUY, 2)
        driver.get('https://coinmarketcap.com/currencies/bnb/')
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="priceValue "]')))
        dollar_val = float(driver.find_element(By.XPATH, '//div[@class="priceValue "]').text[1:])
        in_dollar = round(dollar_val*BIG_BUY)
        return BIG_BUY, TRX_HASH, TRX_HASH_LINK, in_dollar
    else:
        return None
                
# print(scrape_function_bsc('0x2170ed0880ac9a755fd29b2688956bd959f933f8'))
# print(scrape_function_eth('0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE'))

def scrape_function_eth(token):
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # creating waiting element
    wait = WebDriverWait(driver, 10)
    url = f'https://etherscan.io/dex?q={token}#transactions'
    driver.get(url)
    driver.switch_to.default_content()
    wait.until(EC.presence_of_element_located((By.XPATH, '//iframe')))
    a = driver.find_element(By.XPATH, "//iframe")
    driver.switch_to.frame(a)

    wait.until(EC.presence_of_element_located((By.XPATH, '//select[@id="ddlRecordsPerPage"]')))
    select = Select(driver.find_element(By.XPATH, '//select[@id="ddlRecordsPerPage"]'))

    select.select_by_value('100')
    driver.switch_to.default_content()
    wait.until(EC.presence_of_element_located((By.XPATH, '//iframe')))
    a = driver.find_element(By.XPATH, "//iframe")
    driver.switch_to.frame(a)
    wait.until(EC.presence_of_element_located((By.XPATH, '//tbody//tr')))
    b = driver.find_elements(By.XPATH, '//tbody//tr')
    BIG_ROW, BIG_VAL = None, 0
    for i in b:
        if ("Buy" in i.text) and ('hr' not in i.text) and ('day' not in i.text):
            if int(i.text.split(' ')[1]) <= 30:
                    if BIG_VAL < float(i.text.replace(',','').split('$')[-1]):
                        BIG_ROW, BIG_VAL = i, float(i.text.replace(',','').split('$')[-1])



    BIG_BUY = BIG_ROW.find_element(By.XPATH, '//td[7]').text
    TRX_HASH =  BIG_ROW.find_element(By.XPATH, '//td[2]').text
    TRX_HASH_LINK = BIG_ROW.find_element(By.XPATH, '//td[2]//a').get_attribute('href')
    in_dollar = BIG_VAL
    return BIG_BUY, TRX_HASH, TRX_HASH_LINK, in_dollar
