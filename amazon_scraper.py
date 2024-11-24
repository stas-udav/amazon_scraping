import time
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio
import os
from asynciolimiter import Limiter
import functions as func
import config as config

file_path, column_index = func.get_window_input()
urls = func.extract_data_excel(file_path, column_index,
    filter_func=lambda url: isinstance(url, str) and url.startswith("https://"))
time.sleep(0.5)

file_path_zip, column_index_zip = func.get_window_input()
zip_codes = func.extract_data_excel(file_path_zip, column_index_zip,
    filter_func=lambda zip: isinstance(zip, str))
print(zip_codes)

async def main():          
    for zip in zip_codes:
        options = webdriver.ChromeOptions()    
        async with webdriver.Chrome(options=options) as driver: 
            await driver.maximize_window() 
            await driver.get("https://www.amazon.com/",wait_load = True)

            # zip_code = zip using directly from for loop
            await func.zip_input(config.zip_xpath, config.popup_menu_xpath, 
                                    config.input_zip_code_xpath, zip, config.apply_bnt_xpath, driver)
        for url in urls: 
            async with webdriver.Chrome(options=options) as driver: 
                await driver.maximize_window()                                    
                await driver.get(url,wait_load = True)                      
                await asyncio.sleep(15)
asyncio.run(main())

