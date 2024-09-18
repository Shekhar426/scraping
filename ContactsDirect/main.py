import time
from datetime import datetime
from selenium import webdriver
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options= chrome_options)
wait = WebDriverWait(driver, 3)

def extract_values(input_string):
    lines = input_string.strip().split('\n')
    result = {}
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            keyword = lines[i].strip()
            value = lines[i + 1].strip()
            result[keyword] = value
    return result
urls =["https://www.contactsdirect.com/contacts/1-day-acuvue-oasys-hydraluxe-90pk", "https://www.contactsdirect.com/contacts/1-day-acuvue-moist-90pk", "https://www.contactsdirect.com/contacts/dailies-total-1-90pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-24pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-for-astigmatism-6pk", "https://www.contactsdirect.com/contacts/pc1", "https://www.contactsdirect.com/contacts/biofinity-toric-6pk", "https://www.contactsdirect.com/contacts/dailies-aquacomfort-plus-90pk", "https://www.contactsdirect.com/contacts/1-day-acuvue-moist-for-astigmatism-90pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-12pk", "https://www.contactsdirect.com/contacts/dailies-total-1-multifocal-90pk", "https://www.contactsdirect.com/contacts/ao1a9", "https://www.contactsdirect.com/contacts/air-optix-hydraglyde-6pk", "https://www.contactsdirect.com/contacts/biofinity-ew-6pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-max-1-day-multifocal-90pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-max-1-day-30pk", "https://www.contactsdirect.com/contacts/pc1a90", "https://www.contactsdirect.com/contacts/acuvue-oasys-max-1-day-90pk", "https://www.contactsdirect.com/contacts/air-optix-night-day-aqua-6pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-1-day-for-astigmatism-30pk", "https://www.contactsdirect.com/contacts/clariti-1-day-90pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-max-1-day-multifocal-30pk", "https://www.contactsdirect.com/contacts/biotrue-1-day-90pk", "https://www.contactsdirect.com/contacts/1-day-acuvue-moist-multifocal-90pk", "https://www.contactsdirect.com/contacts/aohas", "https://www.contactsdirect.com/contacts/av12", "https://www.contactsdirect.com/contacts/air-optix-plus-hydraglyde-multifocal", "https://www.contactsdirect.com/contacts/dailies-aquacomfort-toric-90pk", "https://www.contactsdirect.com/contacts/ultra-with-moistureseal-6pk", "https://www.contactsdirect.com/contacts/biofinity-xr-toric-6-pack", "https://www.contactsdirect.com/contacts/air-optix-colors-6pk", "https://www.contactsdirect.com/contacts/ultra-for-astigmatism-6pk", "https://www.contactsdirect.com/contacts/biofinity-energys-6pk", "https://www.contactsdirect.com/contacts/inf90", "https://www.contactsdirect.com/contacts/ava6", "https://www.contactsdirect.com/contacts/aom6", "https://www.contactsdirect.com/contacts/myday-daily-disposable-90pk", "https://www.contactsdirect.com/contacts/dailies-aquacomfort-plus-multifocal-90pk", "https://www.contactsdirect.com/contacts/biofinity-multifocal-distance-6pk", "https://www.contactsdirect.com/contacts/clariti-1-day-toric-90pk", "https://www.contactsdirect.com/contacts/biotrue-oneday-for-astigmatism-90pk", "https://www.contactsdirect.com/contacts/rb90", "https://www.contactsdirect.com/contacts/infuse-multifocal-90pk", "https://www.contactsdirect.com/contacts/1-day-acuvue-moist-30pk", "https://www.contactsdirect.com/contacts/ultra-for-presbyopia-6pk", "https://www.contactsdirect.com/contacts/acuvue-2-6pk", "https://www.contactsdirect.com/contacts/myday-toric-90pk", "https://www.contactsdirect.com/contacts/proclear-1-day-90pk", "https://www.contactsdirect.com/contacts/dailies-total-1-for-astigmatism-90pk", "https://www.contactsdirect.com/contacts/acuvue-vita-6pk", "https://www.contactsdirect.com/contacts/total-30-12-pack", "https://www.contactsdirect.com/contacts/myday-multifocal-90-pack", "https://www.contactsdirect.com/contacts/1-day-acuvue-moist-for-astigmatism-30pk", "https://www.contactsdirect.com/contacts/avaira-vitality-6pk", "https://www.contactsdirect.com/contacts/t30", "https://www.contactsdirect.com/contacts/clariti-1-day-multifocal-90pk", "https://www.contactsdirect.com/contacts/biotrue-oneday-presbyopia-30pk", "https://www.contactsdirect.com/contacts/avaira-vitality-toric-6pk", "https://www.contactsdirect.com/contacts/pc130", "https://www.contactsdirect.com/contacts/biofinity-multifocal-near-6pk", "https://www.contactsdirect.com/contacts/aoh12", "https://www.contactsdirect.com/contacts/1-day-acuvue-moist-multifocal-30pk", "https://www.contactsdirect.com/contacts/pc1a30", "https://www.contactsdirect.com/contacts/air-optix-colors-2pk", "https://www.contactsdirect.com/contacts/dailies-total-1-30pk", "https://www.contactsdirect.com/contacts/total-30-toric-6-pack", "https://www.contactsdirect.com/contacts/proclear-sphere-6pk", "https://www.contactsdirect.com/contacts/dailies-total-1-multifocal-30pk", "https://www.contactsdirect.com/contacts/rbt90", "https://www.contactsdirect.com/contacts/dac90", "https://www.contactsdirect.com/contacts/biomedics-55-premier-6pk", "https://www.contactsdirect.com/contacts/proclear-1-day-multifocal-90pk", "https://www.contactsdirect.com/contacts/dailies-aquacomfort-toric-30pk", "https://www.contactsdirect.com/contacts/biotrue-oneday-for-astigmatism-30pk", "https://www.contactsdirect.com/contacts/proclear-toric-6pk", "https://www.contactsdirect.com/contacts/biotrue-1-day-30pk", "https://www.contactsdirect.com/contacts/biofinity-xr-6pk", "https://www.contactsdirect.com/contacts/dailies-aquacomfort-plus-30pk", "https://www.contactsdirect.com/contacts/dailies-total-1-for-astigmatism-30pk", "https://www.contactsdirect.com/contacts/proclear-toric-xr-6pk", "https://www.contactsdirect.com/contacts/rbm90", "https://www.contactsdirect.com/contacts/dac30", "https://www.contactsdirect.com/contacts/dailies-aquacomfort-plus-multifocal-30pk", "https://www.contactsdirect.com/contacts/myday-energys-90pk", "https://www.contactsdirect.com/contacts/acuvue-oasys-with-transitions", "https://www.contactsdirect.com/contacts/clariti-1-day-multifocal-30pk", "https://www.contactsdirect.com/contacts/proclear-multifocal-dominant-6pk", "https://www.contactsdirect.com/contacts/proclear-multifocal-xr-dominant-6pk", "https://www.contactsdirect.com/contacts/clariti-1-day-toric-30pk", "https://www.contactsdirect.com/contacts/proclear-multifocal-xr-non-dom-6pk", "https://www.contactsdirect.com/contacts/proclear-multifocal-non-dom-6pk", "https://www.contactsdirect.com/solutions/scom", "https://www.contactsdirect.com/solutions/sze", "https://www.contactsdirect.com/solutions/optifree-pure-moist-solution-2-pack", "https://www.contactsdirect.com/solutions/optifree-pure-moist-drops", "https://www.contactsdirect.com/solutions/systane-balance", "https://www.contactsdirect.com/solutions/systane-ultra"]
number = 1
for i in urls:
    driver.get(i)
    print(number, end=" ")
    number = number + 1
    time.sleep(1)
    try:
        name = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@id ='PDPTelaniumDataproductName']"))).text
    except:
        driver.find_element(By.XPATH, "//img[@alt='close']").click()
        name  = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@id ='PDPTelaniumDataproductName']"))).text
    try:
        manufacturer = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@id ='maker']"))).text
    except:
        driver.find_element(By.XPATH, "//img[@alt='close']").click()
        manufacturer = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[@id ='maker']"))).text
    try:
        full_price = wait.until(EC.visibility_of_element_located((By.XPATH, "//del[@class='pdp_full_price']"))).text
    except TimeoutException:
        try:
            driver.find_element(By.XPATH, "//img[@alt='close']").click()
            full_price = wait.until(EC.visibility_of_element_located((By.XPATH, "//del[@class='pdp_full_price']"))).text
        except (NoSuchElementException,ElementNotInteractableException,TimeoutException):
            full_price =''
    try:
        price = driver.find_element(By.XPATH, "//span[@class='pdp_real_price']").text
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, "//img[@alt='close']").click()
            price = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='pdp_real_price']"))).text
        except (NoSuchElementException,ElementNotInteractableException,TimeoutException):
            price = ''
    try:
        details = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@aria-label='Product additional informations'])[1]"))).text
        input_text = details.replace("Additional Information", "")
        product_details= extract_values(input_text)
    except:
        driver.find_element(By.XPATH, "//img[@alt='close']").click()
        details = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@aria-label='Product additional informations'])[1]"))).text
        input_text = details.replace("Additional Information", "")
        product_details= extract_values(input_text)
    parsed_data={
        'time_stamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name":name,
        "manufacturer":manufacturer,
        "full_price":full_price,
        "price":price,
        "product_details": product_details
    }
    print(parsed_data)
    json_file_path = 'contactsdirect.json'
    # Function to append a dict to a list and save it to a JSON file
    def append_dict_to_list_and_save(dictionary, file_path):
        try:
            # Read the existing data from the JSON file (if it exists)
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, create an empty list
            data = []
        data.append(dictionary)
        # Save the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    # Dictionary to append to the list
    append_dict_to_list_and_save(parsed_data, json_file_path)