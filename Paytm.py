from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Read URLs from the Excel file
df = pd.read_excel(r"D:\Automation_all_files\Excel_files\Paytm_url.xlsx")
urls = df.url.tolist()

# Number of instances or drivers
num_instances = 8

# Divide the URLs into segments for each instance
url_segments = [urls[i::num_instances] for i in range(num_instances)]
common_xpath = "/html/body/div/div/div[1]/div[4]/div/p" 

def scrape_upi_segment(segment):
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')


    with webdriver.Chrome(options=chrome_options) as driver:
        driver.maximize_window()
        for idx, url in enumerate(segment):
            try:
                driver.get(url)
             
                # upi_element = WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, common_xpath)))
                upi_value = upi_element.text
                print(f'UPI Value for {idx}-- {url}: {upi_value}')
                df.loc[df['url'] == url, 'upi'] = upi_value
            except Exception as e:
                print(f"Error {url}: {str(e)}")
                df.loc[df['url'] == url, 'upi'] = "Not Found"

# Use ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor(max_workers=num_instances) as executor:
    executor.map(scrape_upi_segment, url_segments)
df.to_excel(r"D:\Automation_all_files\Excel_files\result.xlsx", index=False)