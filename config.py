import os

fit_type_xpath = '//p[@class="a-text-left a-size-base"]'
size_xpath = '//li[@class="a-dropdown-item dropdownAvailable"]'
color_xpath = '//span[@class="xoverlay"]'
zip_code_xpath = '//div/span[contains(normalize-space(text()), "Update location")]'
popup_menu_xpath = '//div[@class="a-popover-wrapper"]'
input_zip_code_xpath = '//input[@autocomplete="postal-code"]'
apply_btn_xpath = '//span[text()="Apply"]'
done_zip_code_btn_xpath = '//button[@name="glowDoneButton"]'
file_path = file_path = os.path.join(os.path.dirname(__file__), "URLs for tracking.xlsx")
size_dropdown_xpath = '//span[@class="twister-dropdown-highlight transparentTwisterDropdownBorder"]'
column_index = [0, 1, 2]
sizes_xpath = '//li[@class="a-dropdown-item dropdownAvailable"]'
delivery_date_xpath = '//div[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_MEDIUM"]'
footer_xpath = '//div[@class="navFooterLine navFooterLinkLine navFooterPadItemLine navFooterCopyright"]'
output_file = os.path.join(os.path.dirname(__file__), 'output.csv')
captcha_xpath = '//div[@class="a-row a-text-center"]//img'
input_captha_field_xpath = '//input[@id="captchacharacters"]'
captcha_continue_bnt_xpath = '//span[@class="a-button-inner"]'