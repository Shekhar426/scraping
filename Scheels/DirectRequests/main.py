import requests
from scrapy import Selector

# Send a GET request to the URL
url = "https://www.scheels.com/p/vortex-defender-flip-cap/E-10.html"
response = requests.get(url)
selector = Selector(text=response.text)
name_value_xpath = selector.xpath('//input[@name="name"]/@value').get()
name_value_css = selector.css('input[name="name"]::attr(value)').get()
