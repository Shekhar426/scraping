import openpyxl
import time
import os
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

def ScrapData(i, url,count,count_1 , sequence, path, requirementList):
    requirementList = requirementList
    path = path
    # Comon data keep here
    allWidth =wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//select[@id='widthWholeDropDown']")))
    allheight = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//select[@id='wholeHeightDropdown']")))
    allWidthText = allWidth.text.split('\n')
    allheightText = allheight.text.split('\n')
    allWidthSelect = Select(allWidth)
    allheightSelect = Select(allheight)
    # requirementList = ["24 x 36", "36 x 54", "36 x 60", "36 x 72", "48 x 48", "78 x 84"]
    for req in requirementList:
        if req[0:2] in allWidthText and req[5:7] in allheightText:
            # Handel stale element reference exception.
            try:
                allWidthSelect.select_by_visible_text(req[0:2])
            except StaleElementReferenceException:
                allWidth = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//select[@id='widthWholeDropDown']")))
                allWidthText = allWidth.text.split('\n')
                allWidthSelect = Select(allWidth)
                allWidthSelect.select_by_visible_text(req[0:2])
            try:
                allheightSelect.select_by_visible_text(req[5:7])
            except StaleElementReferenceException:
                allheight = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//select[@id='wholeHeightDropdown']")))
                allheightText = allheight.text.split('\n')
                allheightSelect = Select(allheight)
                allheightSelect.select_by_visible_text(req[5:7])
            time.sleep(2)
            driver.refresh()
            # If there are //a[text() = 'More Rows of Colors'] elements then click it.
            try:
                while True:
                    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text() = 'More Rows of Colors']"))).click()
            except:
                pass

            # Here below code will identify that how many color and texture realated comobination can be made.
            totalCombination = driver.find_elements(By.XPATH, "//div[@id='gcc-pip-swatches']/ul/li")
            if len(totalCombination) == 1:
                totalColor = driver.find_elements(By.XPATH, "//figure[@class='relative']")
                for clr in totalColor:
                    try:
                        clr.click()
                    except:
                        pass
                    count += 1

                    colorName = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Selected Color')]/following-sibling::div"))).text.strip()
                    html = driver.page_source
                    with open(f'{path}{sequence}_{req[0:2]}_{req[5:7]}_{colorName.replace(" ", "_").replace("/", "").replace('"', '')}.html', 'w', encoding='utf-8') as f:
                        f.write(unidecode(html))
                    print("Dumps Saved for Url : ", url)
            else:
                print("Else Block Executed")
                colorList = driver.find_elements(By.XPATH, "//div[@id='gcc-pip-swatches']/ul/li[1]//ul/li/div//figcaption")
                textutrList = driver.find_elements(By.XPATH, "//div[@id='gcc-pip-swatches']/ul/li[2]//ul/li/div//figcaption")

                for clr in colorList:
                    try:
                        clr.click()
                    except:
                        pass
                    count += 1
                    for txt in textutrList:
                        txt.click()
                        count_1+=1
                        colorName = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Selected Color')]/following-sibling::div"))).text.strip()
                        html = driver.page_source
                        textureName = txt.text.replace(" ", "-").replace("/", "").replace('"', '')
                        with open(f'{path}{sequence}_{req[0:2]}_{req[5:7]}_{colorName.replace(" ", "-").replace("/", "").replace('"', '')}_{textureName.replace("/", "").replace('"', '').replace(" ", "")}.html', 'w', encoding='utf-8') as f:
                            f.write(unidecode(html))
                        print("Dumps Saved for Url : ", url)

# Open Xls File which contains urls.
workbook = openpyxl.load_workbook("urls.xlsx")
sheet = workbook['Sheet']
max_row = sheet.max_row
# Prepare a list of urls and sequence. which we were doing copy paste previously

# Function to create name for the perticular url with the name of row number of url in excel sheet



