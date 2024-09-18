import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
driver = Driver(browser='Chrome')
wait = WebDriverWait(driver, 20)
from category import urlsList

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

count = 1
for i in urlsList:

    try:
        driver.get(i)
        try:
            products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='product-name']")))
        except:
            products = []
        print(len(products), i)
        if len(products) > 0:
            with open('productUrls.txt', 'a') as f:
                for product in products:
                    f.write(i + '\n')
            print("This is a direct url having products inside. URL Appended")
        elif len(products) == 0:
            print("Extra Processing required")
            # try:
            navList = driver.find_elements(By.XPATH, "//ul[@data-test-id='nav-list']/li")
            for navigation in range(len(navList)):
                driver.find_elements(By.XPATH, "//ul[@data-test-id='nav-list']/li")[navigation].click()
                print("Nav List Item Clicked")
                time.sleep(7)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                shopNowList = driver.find_elements(By.XPATH, "//div[@id='descriptionButton']//a")
                print(len(shopNowList))
                for shopthecollection in shopNowList:
                    with open('productUrls.txt', 'a') as f2:
                        f2.write(shopthecollection.get_attribute('href') + '\n')
                print("All shop the collection link are appended to the file.")
                driver.execute_script("window.scrollTo(0, 0);")
    except:
        with open('errorUrls.txt', 'a') as f:
            f.write(i + '\n')
    print("Processed URL: ", count)
    count += 1