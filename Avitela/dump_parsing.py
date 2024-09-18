import csv
import json
import os

from scrapy import Selector
from datetime import datetime

path = "C:\dumps_avitela"
path_list = []

for file in os.listdir(path):
    if file.endswith(".html"):
        path_list.append(os.path.join(path, file))

count = 1
for i in path_list[:]:
    print(count, end=" ")
    print(i, end=" ")
    with open(i, 'r', encoding='utf-8') as f:
        html = f.read()
    selector = Selector(text=html)
    title = selector.xpath("//title/text()").get()
    if title != "Avitela.lt":
        name = selector.xpath("//div[@id='quickview_product']/div/h1/text()").get()
        url = selector.xpath("//link[@rel='canonical']/@href").get()
        sku = selector.xpath("//script[@data-flix-language='lt']/@data-flix-sku").get()
        mpn = selector.xpath("//script[@data-flix-language='lt']/@data-flix-mpn").get()
        brand = selector.xpath("//script[@data-flix-language='lt']/@data-flix-brand").get()
        ean = selector.xpath("//script[@data-flix-language='lt']/@data-flix-ean").get()
        distributor = selector.xpath("//script[@data-flix-language='lt']/@data-flix-distributor").get()
        category = selector.xpath("//div[@class='clearfix']/ul/li[2]/a/text()").get()
        sub_category = selector.xpath("//div[@class='clearfix']/ul/li[3]/a/text()").get()

        regular_price = selector.xpath("//span[@id='price-old']/text()").get()
        if regular_price:
            regular_price = regular_price.replace("€", "").replace(" ", "").replace("EUR", "")
        unprocessed_json = {}
        unprocessed_json["distributor"] = distributor

        images = []

        image_list = selector.xpath("//div[@class='owl-carousel product_image_slider owl-loaded owl-drag']//img")
        for i in image_list:
            imageurl = i.xpath("./@data-src").get()
            images.append(imageurl)
        item_number = selector.xpath("//span[@id='pmodel']/text()").get()
        elements = selector.xpath("//div[@id='tab-specification']//div//table//tbody//tr")

        for i in elements:
            key = i.xpath("./td[1]/text()").get()
            value = i.xpath("./td[2]/text()").get()
            unprocessed_json[key] = value
        parsed_data = {'time_stamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'tenant_id': "Topo Centras", 'competitor_name': "Avitela", 'title': name, 'mpn': mpn, 'ean': ean, 'brand': brand, 'category': category, 'sub_category': sub_category, 'regular_price': regular_price, 'discounted_price': "", "image_url": images, "priceCurrency": "EUR", "item_url": url, "item_number": item_number, "unprocessed_json": {**unprocessed_json}}
        json_file_path = 'avitela.json'
        print(parsed_data)

        # Function to append a dictionary to a list and save it to a JSON file
        def append_dict_to_list_and_save(dictionary, file_path):
            try:
                # Read the existing data from the JSON file (if it exists)
                with open(file_path, 'r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # If the file doesn't exist or is empty, create an empty list
                data = []
            # Append the new dictionary to the list
            data.append(dictionary)
            # Save the updated data back to the JSON file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        # Dictionary to append to the list
        append_dict_to_list_and_save(parsed_data, json_file_path)
        count += 1
    else:
        print(i, "Product is redirecting to home Page")
        with open("Error_logs.txt", 'a') as file:
            file.write(f"{i}, Product is redirecting to home Page\n")
