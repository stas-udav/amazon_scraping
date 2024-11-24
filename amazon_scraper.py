import os
from bs4 import BeautifulSoup
from numpy import extract
from playwright.sync_api import sync_playwright
import time
import requests
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio
import os
from asynciolimiter import Limiter
import functions as func

file_path, column_index = func.get_window_input()
urls = func.extract_data_excel(file_path, column_index,
    filter_func=lambda url: isinstance(url, str) and url.startswith("https://"))

file_path_zip, column_index_zip = func.get_window_input()
zip_codes = func.extract_data_excel(file_path_zip, column_index_zip,
    filter_func=lambda zip: isinstance(zip, str))
print(zip_codes)

for url in urls:
    async def main():
        options = webdriver.ChromeOptions()    
        async with webdriver.Chrome(options=options) as driver: 
            await driver.maximize_window()       
            await driver.get(url,
                            wait_load = True)  
            
            await asyncio.sleep(15)
    asyncio.run(main())

