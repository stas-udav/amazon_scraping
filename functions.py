from email import message
from math import e
from tkinter import simpledialog
from turtle import up
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium_driverless.types.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio


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



async def zip_input(zip_xpath, popup_menu_xpath, input_zip_code_xpath, zip_code, apply_bnt_xpath, done_btn_xpath, driver):
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
        await asyncio.sleep(2)        
        print("Update Location")
        update_location = await driver.find_element(By.XPATH, zip_xpath)
        print("Updated")
        print(await update_location.text)
        await update_location.click()

        # Get the popup menu element
        popup_menu = await driver.find_element(By.XPATH, popup_menu_xpath)
        await popup_menu.click()
        await asyncio.sleep(1)

        # Input the zip code and click the "Apply" button
        input_zip_code = await driver.find_element(By.XPATH, input_zip_code_xpath)
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

