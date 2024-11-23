from email import message
from math import e
from tkinter import simpledialog
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# noqa: F401 (imported in main script)

def extract_urls_excel(file_path, column_name):

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)
    print("Доступные столбцы:", df.columns.tolist())

    # Extract the URLs from the specified column
    urls = df.iloc[:, 0].tolist()

    urls = [url for url in urls if isinstance(url, str) and url.startswith("https://")]

    return urls

def get_window_input():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if file_path:
        while True:
            column_name = simpledialog.askstring(
                "Column Name",
                "Enter the name of the column containing the URLs:"
            )
            if column_name:
                return file_path, column_name
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
