from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
import time
executable_path = Service("../chromedriver.exe")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service = executable_path, options= chrome_options)
wait = WebDriverWait(driver, 20)
driver.get("https://www.targetoptical.com/ContactLensCategoriesDisplay?page=1&storeId=12001&urlRequestType=Base&categoryId=82862&langId=-1&catalogId=12751")
page_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class='nextPageNumerical total-pages']")))

for i in range(int(page_element.text)):
    driver.get("https://www.targetoptical.com/ContactLensCategoriesDisplay?page="+str(i+1)+"&storeId=12001&urlRequestType=Base&categoryId=82862&langId=-1&catalogId=12751")
    items_per_page = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[starts-with(@id,'WC_CatalogSearchResultDisplay_td_')]")))
    
    for j in range(len(items_per_page)):
        time.sleep(1)
        items_per_page = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[starts-with(@id,'WC_CatalogSearchResultDisplay_td_')])["+str(j+1)+"]")))
        items_per_page.click()
        time.sleep(1)
        category = wait.until(EC.visibility_of_element_located((By.XPATH, "(//span[@property='name'])[1]")))
        print("Page : ",(i+1) , j+1,end=" | ")
        print(category.text, end= "|")

        brand = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@property='name' and @itemprop='brand']")))
        print(brand.text, end= "|")
        name  = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='contacts-name']")))
        print(name.text,end=" | ")
        manufacturer = wait.until(EC.visibility_of_element_located((By.XPATH, "(//span[@class='brand'])[2]")))
        print(manufacturer.text,end=" | ")
        try:
            box_discount = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='p-0 col-md-4 col-sm-4 col-xs-4 price right boxDiscount']")))
            print(box_discount.text,end=" | ")
        except TimeoutException:
            pass
        try:
            list_price = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='p-0 col-md-2 col-sm-2 col-xs-2 price right listPrice']")))
            print(list_price.text,end=" | ")
        except TimeoutException:
            pass
        try:
            lens_type = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@class='lens-type description']")))
            print(lens_type.text,end=" | ")
        except:
            pass
        try:
            package_details = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@class='lens-package description']")))
            print(package_details.text,end=" | ")
        except TimeoutException:
            pass
        try:
            material = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@class='material description']")))
            print(material.text,end=" | ")
        except TimeoutException:
            pass
        try:
            water_content = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@class='lens-water description']")))
            print(water_content.text,end=" | ")
        except TimeoutException:
            pass
        print(driver.current_url)
        driver.back()
