from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options= chrome_options)
wait = WebDriverWait(driver, 3)
urls = ["https://www.samsclubcontacts.com/lens/310", "https://www.samsclubcontacts.com/lens/323", "https://www.samsclubcontacts.com/lens/330", "https://www.samsclubcontacts.com/lens/572", "https://www.samsclubcontacts.com/lens/305", "https://www.samsclubcontacts.com/lens/704", "https://www.samsclubcontacts.com/lens/929", "https://www.samsclubcontacts.com/lens/681", "https://www.samsclubcontacts.com/lens/308", "https://www.samsclubcontacts.com/lens/938", "https://www.samsclubcontacts.com/lens/571", "https://www.samsclubcontacts.com/lens/514", "https://www.samsclubcontacts.com/lens/914", "https://www.samsclubcontacts.com/lens/952", "https://www.samsclubcontacts.com/lens/715", "https://www.samsclubcontacts.com/lens/148", "https://www.samsclubcontacts.com/lens/718", "https://www.samsclubcontacts.com/lens/611", "https://www.samsclubcontacts.com/lens/960", "https://www.samsclubcontacts.com/lens/317", "https://www.samsclubcontacts.com/lens/378", "https://www.samsclubcontacts.com/lens/528", "https://www.samsclubcontacts.com/lens/687", "https://www.samsclubcontacts.com/lens/552", "https://www.samsclubcontacts.com/lens/686", "https://www.samsclubcontacts.com/lens/614", "https://www.samsclubcontacts.com/lens/610", "https://www.samsclubcontacts.com/lens/685", "https://www.samsclubcontacts.com/lens/951", "https://www.samsclubcontacts.com/lens/714", "https://www.samsclubcontacts.com/lens/479", "https://www.samsclubcontacts.com/lens/977", "https://www.samsclubcontacts.com/lens/950", "https://www.samsclubcontacts.com/lens/700", "https://www.samsclubcontacts.com/lens/710", "https://www.samsclubcontacts.com/lens/295", "https://www.samsclubcontacts.com/lens/626", "https://www.samsclubcontacts.com/lens/554", "https://www.samsclubcontacts.com/lens/698", "https://www.samsclubcontacts.com/lens/702", "https://www.samsclubcontacts.com/lens/622", "https://www.samsclubcontacts.com/lens/896", "https://www.samsclubcontacts.com/lens/713", "https://www.samsclubcontacts.com/lens/719", "https://www.samsclubcontacts.com/lens/127", "https://www.samsclubcontacts.com/lens/299", "https://www.samsclubcontacts.com/lens/629", "https://www.samsclubcontacts.com/lens/936", "https://www.samsclubcontacts.com/lens/558", "https://www.samsclubcontacts.com/lens/945", "https://www.samsclubcontacts.com/lens/711", "https://www.samsclubcontacts.com/lens/553", "https://www.samsclubcontacts.com/lens/939", "https://www.samsclubcontacts.com/lens/948", "https://www.samsclubcontacts.com/lens/306", "https://www.samsclubcontacts.com/lens/942", "https://www.samsclubcontacts.com/lens/312", "https://www.samsclubcontacts.com/lens/178", "https://www.samsclubcontacts.com/lens/895", "https://www.samsclubcontacts.com/lens/927", "https://www.samsclubcontacts.com/lens/540", "https://www.samsclubcontacts.com/lens/966", "https://www.samsclubcontacts.com/lens/984", "https://www.samsclubcontacts.com/lens/226", "https://www.samsclubcontacts.com/lens/684", "https://www.samsclubcontacts.com/lens/556", "https://www.samsclubcontacts.com/lens/47", "https://www.samsclubcontacts.com/lens/983", "https://www.samsclubcontacts.com/lens/699", "https://www.samsclubcontacts.com/lens/314", "https://www.samsclubcontacts.com/lens/621", "https://www.samsclubcontacts.com/lens/107", "https://www.samsclubcontacts.com/lens/103", "https://www.samsclubcontacts.com/lens/551", "https://www.samsclubcontacts.com/lens/712", "https://www.samsclubcontacts.com/lens/296", "https://www.samsclubcontacts.com/lens/962", "https://www.samsclubcontacts.com/lens/617", "https://www.samsclubcontacts.com/lens/931", "https://www.samsclubcontacts.com/lens/117", "https://www.samsclubcontacts.com/lens/297", "https://www.samsclubcontacts.com/lens/981", "https://www.samsclubcontacts.com/lens/615", "https://www.samsclubcontacts.com/lens/930", "https://www.samsclubcontacts.com/lens/557", "https://www.samsclubcontacts.com/lens/967", "https://www.samsclubcontacts.com/lens/539", "https://www.samsclubcontacts.com/lens/609", "https://www.samsclubcontacts.com/lens/375", "https://www.samsclubcontacts.com/lens/315", "https://www.samsclubcontacts.com/lens/603", "https://www.samsclubcontacts.com/lens/290", "https://www.samsclubcontacts.com/lens/982", "https://www.samsclubcontacts.com/lens/988", "https://www.samsclubcontacts.com/lens/535", "https://www.samsclubcontacts.com/lens/616", "https://www.samsclubcontacts.com/lens/478", "https://www.samsclubcontacts.com/lens/344", "https://www.samsclubcontacts.com/lens/163", "https://www.samsclubcontacts.com/lens/979", "https://www.samsclubcontacts.com/lens/106", "https://www.samsclubcontacts.com/lens/339", "https://www.samsclubcontacts.com/lens/677", "https://www.samsclubcontacts.com/lens/672", "https://www.samsclubcontacts.com/lens/705", "https://www.samsclubcontacts.com/lens/676", "https://www.samsclubcontacts.com/lens/321"]
number = 1
for i in urls:
    driver.get(i)
    print(number, i, end=" | ")
    number = number + 1
    try:
        discontinue_warning  = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='lens-detail__discontinued-warning']")))
        if len(discontinue_warning) == 1:
            print("Discontinued Lens")
    except:
        name  = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='lens-info']/h1")))
        print(name.text, end= "|")
        manufacturer = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='subtext']/span")))
        print(manufacturer.text,end=" | ")
        Free_shipping_over = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='js-popover-btn link']/span")))
        print(Free_shipping_over.text,end=" | ")
        try:
            avaliblity  = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='in-stock col-xs-12']/span/b")))
            print(avaliblity.text,end=" | ")
        except:
                try:
                    avaliblity  = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='in-stock col-xs-12']/span")))
                    print(avaliblity.text,end=" | ")
                except (TimeoutException, StaleElementReferenceException):
                    pass
        try:
            price = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class = 'best-value-price']/span")))
            print(price.text.strip().replace("\n","").replace(" ","").replace("/Box",""),end=" | ")
        except TimeoutException:
                    price = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='lens-detail__price-box']/div[1]")))
                    print(price.text.strip().replace("\n","").replace(" ","").replace("/Box",""),end=" | ")
        except StaleElementReferenceException:
                    pass
        lens_descs = {}
        lens_desc_ele = driver.find_elements(By.XPATH, "(//div[@class='lens-description'])[2]/ul/li")
        try:
            for lens_desc in lens_desc_ele[1:]:
                key, value = lens_desc.text.split(":")
                lens_descs[key.strip()] = value.strip()
            if len(lens_descs.keys()) > 0:
                print(lens_descs)
            else:
                lens_desc_ele = driver.find_elements(By.XPATH, "(//div[@class='lens-description'])[1]/ul/li")
                for lens_desc in lens_desc_ele[1:]:
                    key, value = lens_desc.text.split(":")
                    lens_descs[key.strip()] = value.strip()
                print(lens_descs)
        except ValueError:
            print(lens_descs)