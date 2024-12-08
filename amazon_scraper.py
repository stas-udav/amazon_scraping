from selenium_driverless import webdriver
from selenium_driverless.types.by import By
# from selenium.common.exceptions import NoSuchElementException
from selenium_driverless.types.webelement import NoSuchElementException
import asyncio
from asynciolimiter import Limiter
import functions as func
import config as config


items_id, urls, zip_codes = func.load_exel_data(config.file_path, config.column_index)
limits = Limiter(1 / 5)

async def main():      
        for item_id, url, zip_code in zip(items_id, urls, zip_codes): 
            
            options = webdriver.ChromeOptions() 
            async with webdriver.Chrome(options=options) as driver: 
               await driver.maximize_window()                                    
               await driver.get(url,wait_load = True)                  
               await asyncio.sleep(5)
               try :
                   capthca = await driver.find_element(By.XPATH, config.captcha_xpath)                    
                   if capthca:
                        print("Captcha found")
                        await func.resolve_captcha(driver, config.captcha_xpath, 
                                                   config.input_captha_field_xpath, config.captcha_continue_bnt_xpath)                
               except NoSuchElementException:
                   print("Captcha not found")
                   pass
               await asyncio.sleep(5)
               
               # zip_code = zip using directly from for loop
               await func.zip_input(config.zip_code_xpath, config.popup_menu_xpath, 
                                   config.input_zip_code_xpath, zip_code, 
                                   config.apply_btn_xpath, config.done_zip_code_btn_xpath, driver)
               # await driver.find.element(By.XPATH, config.zip_code_xpath).click()
               print("Zip code inputed")
               await asyncio.sleep(7)
               drop_down_size_menu = await driver.find_element(By.XPATH, config.size_dropdown_xpath)
               await asyncio.sleep(2)
               # await driver.execute_script("arguments[0].scrollIntoView();", config.size_dropdown_xpath)
               await drop_down_size_menu.click()
               await asyncio.sleep(5)
               print("Size menu opened")
               try:
                    sizes = await driver.find_elements(By.XPATH, config.sizes_xpath)                    
                    for i in range(len(sizes) -1, -1, -1):  
                         try:
                              sizes = await driver.find_elements(By.XPATH, config.sizes_xpath)
                              size = sizes[i] 
                              text_size = await size.text        
                              print(text_size)         
                              await size.click()
                              await asyncio.sleep(1)                    
                              print("Size selected")
                              await asyncio.sleep(1)
                              delivery_date = await driver.find_element(By.XPATH, config.delivery_date_xpath)
                              # print(await delivery_date.text)
                              # delivery_date_text = await delivery_date.text
                              delivery_date_cleaned = func.extract_date_from_text(await delivery_date.text)                              
                              try:
                                   days_to_delivery = (func.extract_date_from_text(await delivery_date.text) - func.today_date()).days
                                   print(f"Delivery in {days_to_delivery} days") 
                              except NoSuchElementException as e:
                                   print(f" {e} date not found or invalid format")
                              func.save_data_to_file(item_id, url, zip_code, text_size, delivery_date_cleaned, 
                                                      days_to_delivery, config.output_file)
                              await asyncio.sleep(1)
                              drop_down_size_menu = await driver.find_element(By.XPATH, config.size_dropdown_xpath)
                              await drop_down_size_menu.click()
                              await asyncio.sleep(2)
                         except IndexError:
                              print("Index out of range")
                              break
                         except Exception  as e:
                              print(f" {e} size not found or invalid format")
                              continue
               except Exception as e:
                    print(f"Eror: {e} with url - {url}")
                    continue
               
            
asyncio.run(main())

