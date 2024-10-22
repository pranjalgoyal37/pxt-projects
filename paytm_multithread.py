from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# driver = webdriver.Chrome()
# url = " https://gateway.rightpays.in/upi/A001707006860"
# driver.get(url )

# print(ele)
# Read URLs from the Excel file
df = pd.read_excel(r"D:\Paytm_url.xlsx",sheet_name="Sheet3")
urls = df['url'].tolist()

# Number of instances or drivers
num_instances = 20

# Divide the URLs into segments for each instance
url_segments = [urls[i::num_instances] for i in range(num_instances)]
common_xpath = "/html/body/div/div/div[1]/div[4]/div/p" 

def scrape_upi_segment(segment):
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--headless')
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.maximize_window()
        for idx, url in enumerate(segment):
            try:
                driver.get(url)
                # time.sleep(3)
                WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.max-w-300px.text-red-500.break-all.mr-8px' )))
                page_source = driver.page_source

# Parse the page source with BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Now you can extract content using BeautifulSoup
                # For example:
                element_class = "max-w-300px text-red-500 break-all mr-8px"
                element = soup.find(class_=element_class)
                if element:
                    upi_value = element.text.strip()
                    df.loc[df['url'] == url, 'upi'] = upi_value
                    print(f'UPI Value for {idx}-- {url}: {upi_value}')
                else:
                    df.loc[df['url'] == url, 'upi'] = "Not Found"
                    print(f'UPI Value for {idx}-- {url}: Not found')
                # upi_element = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, common_xpath)))
                # upi_value = upi_element.text
                # print(f'UPI Value for {idx}-- {url}: {upi_value}')
                # df.loc[df['url'] == url, 'upi'] = upi_value
            except Exception as e:
                print(f"Error {url}: {str(e)}")
                df.loc[df['url'] == url, 'upi'] = "Not Found"

# Use ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor(max_workers=num_instances) as executor:
    executor.map(scrape_upi_segment, url_segments)
df.to_excel(r"D:\result.xlsx", index=False)