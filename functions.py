from tkinter import simpledialog
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium_driverless.types.by import By
from selenium_driverless.types.webelement import NoSuchElementException
import asyncio
import re
from datetime import date, datetime
from amazoncaptcha import AmazonCaptcha



def get_window_input():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if file_path:
        while True:
            column_index = simpledialog.askinteger(
                "Column Index",
                "Enter the column number (0 for first column):"
            )
            if column_index is not None:
                return file_path, column_index
            else:
                messagebox.showwarning("Error", "Column name not provided.")
                root.destroy()
    else:
        messagebox.showwarning("Error", "File not selected.")
        root.destroy()
        return None, None
    
# extract data from excel file with precondition(urls, zips, ids)
def load_exel_data(file_path, column_indexes):
    df = pd.read_excel(file_path)

    items_id = df.iloc[:, column_indexes[0]].tolist()
    urls = df.iloc[:, column_indexes[1]].tolist()
    zip_codes = df.iloc[:, column_indexes[2]].tolist()

    # print(items_id)
    # print(urls)
    # print(zip_codes)
    return items_id, urls, zip_codes



async def zip_input(zip_xpath, popup_menu_xpath, input_zip_code_xpath, zip_code,
                    apply_bnt_xpath, done_btn_xpath, driver):
    """
    Inputs the zip code into the location popup menu and applies the changes.

    Args:
        zip_xpath (str): The XPath of the "Update Location" button
        popup_menu_xpath (str): The XPath of the popup menu
        input_zip_code_xpath (str): The XPath of the input box for the zip code
        zip_code (str): The zip code to input
        apply_btn_xpath (str): The XPath of the "Apply" button
        driver: The selenium-driverless WebDriver

    Returns:
        bool: True if successful, False if any error occurred
    """
    try:
        # Click the "Update Location" button
        await asyncio.sleep(5)        
        print("Update Location")
        update_location = await driver.find_element(By.XPATH, zip_xpath)
        print("Updated")
        print(await update_location.text)
        await update_location.click()

        # Get the popup menu element
        popup_menu = await driver.find_element(By.XPATH, popup_menu_xpath)
        await popup_menu.click()
        await asyncio.sleep(3)

        # Input the zip code and click the "Apply" button
        try:
            input_zip_code = await driver.find_element(By.XPATH, input_zip_code_xpath)
        except NoSuchElementException:
            print("Input box not found")
            await driver.refresh()
            await asyncio.sleep(5)
            return await zip_input(zip_xpath, popup_menu_xpath, input_zip_code_xpath, zip_code,
                   apply_bnt_xpath, done_btn_xpath, driver)
        await input_zip_code.click()
        zip_code_str = str(int(zip_code))
        await input_zip_code.send_keys(zip_code_str)
    
        # Get the "Apply" button element
        apply_button = await driver.find_element(By.XPATH, apply_bnt_xpath)
        # Click the "Apply" button
        await apply_button.click()
        await asyncio.sleep(2)
        done = await driver.find_element(By.XPATH, done_btn_xpath)
        await done.click()
        return True
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return False

def extract_date_from_text(text):
    match = re.search(r'(\w+ \d+)', text)
    if match:
        try:
            date_str = match.group(1)
            year = date.today().year
            date_obj = datetime.strptime(date_str, '%B %d')
            date_obj = date_obj.date()
            date_obj = date_obj.replace(year=year)
            print(date_obj)
            return date_obj
        except ValueError:
            print(" date not found or invalid format")
            return None

def today_date():
    print (date.today())
    return date.today()       

def save_data_to_file(item_id, url, zip_code, size, delivery_date, days_to_delivery, output_file):
    current_date = today_date()
    try:
        df = pd.read_csv(output_file)
    except FileNotFoundError:
        df = pd.DataFrame()
    if df.empty:
        data = pd.DataFrame([{
            'Item ID': item_id,
            'URL': url,
            'Zip Code': zip_code,
            'Size': size,
            'Delivery Date': delivery_date,
            'Current Data': current_date.strftime('%Y-%m-%d'),
            'Days to Delivery': days_to_delivery
        }])
        df = pd.concat([df, data], ignore_index=True)
    else:
        maching_row = df[(df['Item ID'] == item_id) & 
                         (df['URL'] == url) & 
                         (df['Zip Code'] == zip_code) & 
                         (df['Size'] == size)]
        if not maching_row.empty:
            idx = maching_row.index[0]
            last_column = len(df.columns)      
            df.loc[idx, f'Delivery Date_{last_column}'] = delivery_date
            df.loc[idx, f'Current Data_{last_column}'] = current_date.strftime('%Y-%m-%d')
            df.loc[idx, f'Days to Delivery_{last_column}'] = days_to_delivery
            
        else:
            data = pd.DataFrame([{
                'Item ID': item_id,
                'URL': url,
                'Zip Code': zip_code,
                'Size': size,
                'Delivery Date': delivery_date,
                'Current Data': current_date.strftime('%Y-%m-%d'),
                'Days to Delivery': days_to_delivery
            }])   
            df = pd.concat([df, data], ignore_index=True)
            print('Added new row')
    df.to_csv(output_file, index=False)
    print("Data saved to output.csv")


async def resolve_captcha(driver, captcha_el, captcha_input_field, btn_xpath):
    # Find the captcha element    
    captcha_element = await driver.find_element(By.XPATH, captcha_el)    
    captcha_img = await captcha_element.get_attribute("src")
    print (captcha_img)

    captcha_text = AmazonCaptcha.fromlink(captcha_img)
    captcha_value = captcha_text.solve()    
    print(captcha_value)

    input_field = await driver.find_element(By.XPATH, captcha_input_field)
    await input_field.send_keys(captcha_value)
    click_continue_btn = await driver.find_element(By.XPATH, btn_xpath)
    await click_continue_btn.click()
    print("Captcha resolved")


