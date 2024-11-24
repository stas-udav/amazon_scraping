from email import message
from math import e
from tkinter import simpledialog
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium_driverless.types.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio

# noqa: F401 (imported in main script)

def extract_data_excel(file_path, column_index, filter_func=None):
    """ Extracts data from an Excel file.
    Arguments: file_path (str) ( resiving from get_window_input): 
    The path to the Excel file to extract data from. column_name (str or numbers): 
    The name of the column to retrieve data from. 
    filter_func (callable, optional): An optional function to filter the extracted data.
    Returns: The extracted data from the specified column.
    Notes: This function provides a universal interface for extracting data from Excel files.
    Example for urls: urls = extract_data_excel(file_path, column_name, 
    filter_func=lambda x: isinstance(x, str) and x.startswith('https://'))    """

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)
    print("Available columns:", df.columns.tolist())

    # Extract the data from the specified column
    data = df.iloc[:, column_index].tolist()

    # function to filter the extracted data
    if filter_func:
        data = [item for item in data if filter_func(item)]    
    return data

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
    

async def zip_input(zip_xpath, popup_menu_xpath, input_zip_code_xpath, zip_code, apply_bnt_xpath, driver):
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
        update_location = await driver.find_element(By.XPATH, zip_xpath)
        await update_location.click()

        # Get the popup menu element
        popup_menu = await driver.find_element(By.XPATH, popup_menu_xpath)
   
        # Input the zip code and click the "Apply" button
        input_zip_code = await driver.find_element(By.XPATH, input_zip_code_xpath)
        await input_zip_code.click()
        await input_zip_code.send_keys(zip_code)
    
        # Get the "Apply" button element
        apply_button = await driver.find_element(By.XPATH, apply_bnt_xpath)
        # Click the "Apply" button
        await apply_button.click()

        return True
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return False
