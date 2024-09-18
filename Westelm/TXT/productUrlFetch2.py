import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
driver = Driver(browser='Chrome')
wait = WebDriverWait(driver, 20)
from category2 import subCategory

def popUpClosed():
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='dismiss-modal']/span"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='no-thanks']/a"))).click()
    except:
        pass
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='no-thanks']/a"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='dismiss-modal']/span"))).click()
    except:
        pass

driver.get('https://www.westelm.com/')
popUpClosed()
print("Pop ups are closed if there were any")

count = 1
for i in subCategory:
        driver.get(i)
        time.sleep(8)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        try:
            MainproductUrls = driver.find_elements(By.XPATH, "//div[@class='product-name']/a")
            totalProductCount = len(MainproductUrls)
            for url in MainproductUrls:
                correctUrl = url.get_attribute('href').split('?')[0]
                with open('Main_product_Url.txt', 'a') as f:
                    f.write(correctUrl + '\n')
        except:
            with open('Error_Main_Product.txt', 'a') as f:
                f.write(i + '\n')
            totalProductCount = "Error appended in logs file."
        print(count, i)
        count += 1