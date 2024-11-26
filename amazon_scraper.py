import time
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio
import os
from asynciolimiter import Limiter
import functions as func
import config as config

# file_path, column_index = func.get_window_input()
# urls = func.extract_data_excel(file_path, column_index,
#     filter_func=lambda url: isinstance(url, str) and url.startswith("https://"))
# time.sleep(0.5)

# file_path_zip, column_index_zip = func.get_window_input()
# zip_codes = func.extract_data_excel(file_path_zip, column_index_zip,
#     filter_func=lambda zip: isinstance(zip, (str, int, float)))
# print(zip_codes)

items_id, urls, zip_codes= func.load_exel_data(config.file_path, config.column_index)

async def main():          
    # for zip in zip_codes:
    #     options = webdriver.ChromeOptions()    
    #     async with webdriver.Chrome(options=options) as driver: 
    #         try:
    #             await driver.maximize_window() 
    #             await driver.get("https://www.amazon.com/",wait_load = True)

    #             # zip_code = zip using directly from for loop
    #             await func.zip_input(config.zip_code_xpath, config.popup_menu_xpath, 
    #                                     config.input_zip_code_xpath, zip, config.apply_btn_xpath, driver)
    #         # await driver.find.element(By.XPATH, config.zip_code_xpath).click()
    #         except NoSuchElementException: 
    #             print("Page not loaded, try again")
        for url, zip_code in zip(urls, zip_codes): 
            
            options = webdriver.ChromeOptions() 
            async with webdriver.Chrome(options=options) as driver: 
                await driver.maximize_window()                                    
                await driver.get(url,wait_load = True)  
                await asyncio.sleep(1)
                # zip_code = zip using directly from for loop
                await func.zip_input(config.zip_code_xpath, config.popup_menu_xpath, 
                                    config.input_zip_code_xpath, zip_code, 
                                    config.apply_btn_xpath, config.done_zip_code_btn_xpath, driver)
                # await driver.find.element(By.XPATH, config.zip_code_xpath).click()
                print("Zip code inputed")
                await asyncio.sleep(5)
                drop_down_size_menu = await driver.find_element(By.XPATH, config.size_dropdown_xpath)
                await asyncio.sleep(1)
                print("Size menu opening")
                # await driver.execute_script("arguments[0].scrollIntoView();", config.size_dropdown_xpath)
                await drop_down_size_menu.click()
                await asyncio.sleep(5)
                print("Size menu opened")
                sizes = await driver.find_elements(By.XPATH, config.sizes_xpath)
                for size in sizes:   
                    text_size = await size.text        
                    print(text_size)         
                    await size.click()
                    await asyncio.sleep(0.5)                    
                    print("Size selected")
                    await asyncio.sleep(1)
                    delivery_date = await driver.find_element(By.XPATH, config.delivery_date_xpath)
                    print(await delivery_date.text)
                    drop_selected_size = await driver.find_element(By.XPATH, f'//span[@class="a-dropdown-container"]//span[contains(normalize-space(text()), "{text_size}")]')
                    await drop_selected_size.click()
                    # await asyncio.sleep(0.5)
                    # next_size = sizes[sizes.index(size)+1]
                    # print(next_size.text)
                    # await next_size.click()
                    # print("Next size selected")
                    # await asyncio.sleep(5)
asyncio.run(main())

