import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver

driver = Driver(uc=True, headed=False, browser='chrome', headless=True)

from TXT.category3 import prodyctUrls

count = 1
varientcount = 1
for i in prodyctUrls[600:]:
        try:
            driver.get(i)
            script_element = driver.find_element(By.XPATH, "(//script[@type='application/ld+json'])[3]")
            script_content = script_element.get_attribute('innerHTML')
            json_data = json.loads(script_content)
            sku_list = json_data[0].get('offers')
            for offer in sku_list:
                sku = offer.get('sku')
                varient_url = i + "?sku=" + sku
                with open('sku4.txt', 'a') as f:
                    f.write(varient_url + '\n')
                varientcount += 1
            print(count, varientcount, i)
            count += 1
        except:
            with open('Error_Sku4.txt', 'a') as f:
                f.write(i + '\n')
            print(count,varientcount, i)
            count += 1
