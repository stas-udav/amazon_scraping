from email import message
from math import e
from tkinter import simpledialog
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import openpyxl

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