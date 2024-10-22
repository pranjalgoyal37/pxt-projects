from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver= webdriver.Firefox()
import io
import pandas as pd

amazon_des='//*[@id="productTitle"]'
url='https://www.amazon.in/dp/B00EH9A0RI/ref=syn_sd_onsite_desktop_0?ie=UTF8&psc=1&pd_rd_plhdr=t'

def read_data():
     df = pd.read_excel()

driver.get(url)
# banner_xpath='//*[@id="ad"]/div/div/div[2]/div[2]/div/div'
# banner_xpath_02=ss='//*[@id="ad"]/div/div/div[2]/div[2]/div/div'
# banner_03_path='//*[@id="cr-ADPlaceholder"]'
# banner_04_XPath='//*[@id="ape_Detail_hero-quick-promo_Desktop_placement"]'

time.sleep(3)

driver.find_element(By.XPATH,amazon_des).click()

# to close the address change bar

try:
    driver.find_element(By.XPATH,'//*[@id="nav-main"]/div[1]/div/div/div[3]/span[1]').click()

except:

     pass

# find the 1st banner

# banner_01=driver.find_element(By.ID,'percolate-ui-ilm_div')

# css selector

banner_01=driver.find_element(By.CSS_SELECTOR,'#percolate-ui-ilm_div')

banner_02=driver.find_element(By.XPATH,'//*[@id="ape_Detail_ams-detail-right-v2_desktop_placement"]')

banner_03=driver.find_element(By.XPATH,'//*[@id="cr-ADPlaceholder"]')
banner_04=driver.find_element(By.XPATH,'//*[@id="ape_Detail_hero-quick-promo_Desktop_placement"]')

banner_01.screenshot('banner_01.png')
banner_02.screenshot('banner_02.png')
banner_03.screenshot('banner_03.png')
banner_04.screenshot('banner_04.png')


# banner_02=driver.find_element(By.CSS_SELECTOR,'#aplus > div > div:nth-child(4) > div > img')

# print(banner_01.text)

print(banner_01.is_displayed())

print(banner_01.get_property('href'))

print(banner_01.location)

# if banner_02.get_property('complete'):

#     banner_02.screenshot('banner_02.png')

#     print('Image is loaded!')

# else:

#     print('Image failed to load.')

# print(banner_02)