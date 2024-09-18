import time
from bs4 import BeautifulSoup
import csv
from seleniumbase import Driver

urls = ["https://www.technorama.lt/2_lt_1_sitemap.xml","https://www.technorama.lt/2_lt_2_sitemap.xml"]

# Set up a headless browser using Selenium
driver = Driver(uc=True)

# Use Selenium to get the page content
count=0
def get_urls(url):
    driver.uc_open(url)
    time.sleep(10)
    page_source = driver.page_source
    # Parse XML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "xml")
    # Find all URLs inside the <loc> tag
    loc_tags = soup.find_all("loc")
    urls = [loc.text for loc in loc_tags]
    return urls

# Create or open a CSV file to write URLs
csv_file_path = 'urls.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['URL'])  # Write header
    # Get and write URLs to CSV

    for url in urls:
        extracted_urls = get_urls(url)
        time.sleep(5)
        for extracted_url in extracted_urls:
            if ".jpg" not in extracted_url and ".png" not in extracted_url:
                csv_writer.writerow([extracted_url])
                count=count+1
                print(count)
# Close the browser
driver.quit()
