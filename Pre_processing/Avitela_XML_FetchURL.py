from selenium import webdriver
from bs4 import BeautifulSoup
import csv
# URL to be scraped
import csv
import openpyxl
import json
from datetime import datetime
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
urls = ["https://avitela.lt/sitemap-product-1.xml", "https://avitela.lt/sitemap-product-2.xml", "https://avitela.lt/sitemap-product-3.xml", "https://avitela.lt/sitemap-product-4.xml", "https://avitela.lt/sitemap-product-5.xml", "https://avitela.lt/sitemap-product-6.xml", "https://avitela.lt/sitemap-product-7.xml", "https://avitela.lt/sitemap-product-8.xml", "https://avitela.lt/sitemap-product-9.xml", "https://avitela.lt/sitemap-product-10.xml", "https://avitela.lt/sitemap-product-11.xml", "https://avitela.lt/sitemap-product-12.xml", "https://avitela.lt/sitemap-product-13.xml", "https://avitela.lt/sitemap-product-14.xml", "https://avitela.lt/sitemap-product-15.xml", "https://avitela.lt/sitemap-product-16.xml", "https://avitela.lt/sitemap-product-17.xml", "https://avitela.lt/sitemap-product-18.xml", "https://avitela.lt/sitemap-product-19.xml", "https://avitela.lt/sitemap-product-20.xml", "https://avitela.lt/sitemap-product-21.xml", "https://avitela.lt/sitemap-product-22.xml", "https://avitela.lt/sitemap-product-23.xml", "https://avitela.lt/sitemap-product-24.xml", "https://avitela.lt/sitemap-product-25.xml", "https://avitela.lt/sitemap-product-26.xml", "https://avitela.lt/sitemap-product-27.xml", "https://avitela.lt/sitemap-product-28.xml", "https://avitela.lt/sitemap-product-29.xml", "https://avitela.lt/sitemap-product-30.xml", "https://avitela.lt/sitemap-product-31.xml", "https://avitela.lt/sitemap-product-32.xml", "https://avitela.lt/sitemap-product-33.xml", "https://avitela.lt/sitemap-product-34.xml", "https://avitela.lt/sitemap-product-35.xml", "https://avitela.lt/sitemap-product-36.xml", "https://avitela.lt/sitemap-product-37.xml", "https://avitela.lt/sitemap-product-38.xml", "https://avitela.lt/sitemap-product-39.xml", "https://avitela.lt/sitemap-product-40.xml", "https://avitela.lt/sitemap-product-41.xml", "https://avitela.lt/sitemap-product-42.xml", "https://avitela.lt/sitemap-product-43.xml", "https://avitela.lt/sitemap-product-44.xml", "https://avitela.lt/sitemap-product-45.xml", "https://avitela.lt/sitemap-product-46.xml", "https://avitela.lt/sitemap-product-47.xml", "https://avitela.lt/sitemap-product-48.xml", "https://avitela.lt/sitemap-product-49.xml", "https://avitela.lt/sitemap-product-50.xml", "https://avitela.lt/sitemap-product-51.xml", "https://avitela.lt/sitemap-product-52.xml", "https://avitela.lt/sitemap-product-53.xml", "https://avitela.lt/sitemap-product-54.xml", "https://avitela.lt/sitemap-product-55.xml", "https://avitela.lt/sitemap-product-56.xml", "https://avitela.lt/sitemap-product-57.xml", "https://avitela.lt/sitemap-product-58.xml", "https://avitela.lt/sitemap-product-59.xml", "https://avitela.lt/sitemap-product-60.xml", "https://avitela.lt/sitemap-product-61.xml", "https://avitela.lt/sitemap-product-62.xml", "https://avitela.lt/sitemap-product-63.xml", "https://avitela.lt/sitemap-product-64.xml", "https://avitela.lt/sitemap-product-65.xml", "https://avitela.lt/sitemap-product-66.xml", "https://avitela.lt/sitemap-product-67.xml", "https://avitela.lt/sitemap-product-68.xml", "https://avitela.lt/sitemap-product-69.xml", "https://avitela.lt/sitemap-product-70.xml"]
driver = Driver(uc=True)
for i in urls:
    driver.uc_open(i)
    urls = driver.find_elements(By.XPATH, '//tr/td/a')
    for i in urls:
        url = i.get_attribute('href')
        print(url)
        with open("url.txt", 'a') as file:
            file.write(url + '\n')