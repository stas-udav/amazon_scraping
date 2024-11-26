import os

fit_type_xpath = '//p[@class="a-text-left a-size-base"]'
size_xpath = '//li[@class="a-dropdown-item dropdownAvailable"]'
color_xpath = '//span[@class="xoverlay"]'
zip_code_xpath = '//div/span[contains(normalize-space(text()), "Update location")]'
popup_menu_xpath = '//div[@class="a-popover-wrapper"]'
input_zip_code_xpath = '//input[@autocomplete="postal-code"]'
apply_btn_xpath = '//span[text()="Apply"]'
file_path = file_path = os.path.join(os.path.dirname(__file__), "test.xlsx")
column_index = [0, 1, 2]