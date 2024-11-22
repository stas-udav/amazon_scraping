import os
from bs4 import BeautifulSoup
from numpy import extract
from playwright.sync_api import sync_playwright
import time
import requests
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio
import os
from asynciolimiter import Limiter
import functions as func

file_path, column_name = func.get_window_input()
urls = func.extract_urls_excel(file_path, column_name)

for url in urls:
    async def main():
        options = webdriver.ChromeOptions()    
        async with webdriver.Chrome(options=options) as driver: 
            await driver.maximize_window()       
            await driver.get(url,
                            wait_load = True)  
                
            await asyncio.sleep(15)
    asyncio.run(main())

# Create a new browser instance 
    # Setup
# driver = webdriver.Chrome()
#     #   Fullscreen browser
# driver.maximize_window()



# scraper = cloudscraper.create_scraper()
# res = scraper.get(url)
# print(res.status_code)
# response = res.text
# print(response)
# time.sleep(5)
# scrape = cfscrape.create_scraper()
# res1 =  scrape.get(url)
# print(res1.status_code)
# response = requests.get(url)
# print(response.status_code)
# soup = BeautifulSoup(response.text, 'lxml')
# print(soup.prettify())

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://www.amazon.com/dp/B07K61RY86?customId=B078RYKX79&customizationToken=MC_Assembly_1%23B078RYKX79&th=1&psc=1")
#     print(page.content())
#     browser.close()

# def get_amazon_delivery_date(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36')
#         page = context.new_page()
#         page.goto(url)
#         # print(page.content())
#         page.wait_for_selector("//div[contains(@class, 'a-box-inner a-accordion-row-container')][.//span[contains(normalize-space(), 'Regular Price')]]")
#         delivery_date = page.locator("//div[contains(@class, 'a-box-inner a-accordion-row-container')][.//span[contains(normalize-space(), 'Regular Price')]]")
#         text = delivery_date.text_content()
#         print(text)
#         browser.close()
#         return text

# get_amazon_delivery_date(url)