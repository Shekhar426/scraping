import logging
from datetime import datetime
import json
import os
import re
from scrapy import Selector
import concurrent.futures

logging.basicConfig(level=logging.DEBUG, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')

product_dumps = []
directory_path = "E:\\dumps_scheels\\Two"


for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        product_dumps.append(os.path.join(directory_path, filename))

def data_parser(html_file, file_count):
    try:
        results_data = []
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        selector = Selector(text=html)
        unprocessed_json = {}

        name = selector.xpath("//h1[@class='product-name-main']/text()").get()
        if name is not None:
            name = name.replace("\n", "")
        brand = selector.xpath("//h1[@class='product-name-main']/../a/text()").get()
        url = selector.xpath("//link[@rel='canonical']/@href").get()
        sku = selector.xpath("//span[@class='productsku']/text()").get()
        description = selector.xpath("//meta[@name='description']/@content").get()

        category = None
        sub_category = None
        Levels = selector.xpath("//nav[@aria-label= 'breadcrumbs']//span")
        for level in range(len(Levels)):
            if level == 0:
                category = Levels[level].xpath("text()").get()
            elif level == 1:
                sub_category = Levels[level].xpath("text()").get()

        regular_price = None
        discounted_price = None
        price1 = selector.xpath("(//span[@class='price-sales'])[1]/span//span[last()]/text()").get()
        price2 = selector.xpath("(//del[@class='price-standard sale'])[1]/text()").get()
        if price1 is not None and price2 is not None:
            regular_price = price2
            discounted_price = price1
        if price1 is not None and price2 is None:
            regular_price = price1
            discounted_price = None
        if regular_price is not None:
            regular_price = regular_price.replace("\n", "").replace("$", "")
        if discounted_price is not None:
            discounted_price = discounted_price.replace("\n", "").replace("$", "")

        variations = selector.xpath("(//ul[@role='presentation'])[1]/li//div[@class='label']")
        for vr in variations:
            key = vr.xpath("./h2/span/text()").get()
            value = vr.xpath("./following-sibling::span[@class='selected-value']/text()").get()
            if value is not None:
                value = value.replace("\n", "")
            unprocessed_json[key] = value
        ratings = selector.xpath("(//div[@class='TTteaser__rating'])[1]/@aria-label").get()
        if ratings is not None:
            ratings = int(ratings.split(" stars out of ")[0])
        currency = selector.xpath("//meta[@itemprop='priceCurrency']/@content").get()
        Availability = selector.xpath("//meta[@itemprop='availability']/@content").get()
        if Availability is not None:
            Availability = Availability.replace("http://schema.org/", "")

        images = []
        image_list = selector.xpath("(//div[contains(@class, 'product-image-container')]//ul)[1]//a")
        for img in image_list:
            imageurl = img.xpath("./@href").get()
            images.append(imageurl)
        images = list(set(images))

        Features = []
        FeatureList = selector.xpath("//h4[text()= 'Features']/following-sibling::div//li")
        for ft in FeatureList:
            singleText = ft.xpath("./text()").get()
            Features.append(singleText)

        parsed_data = {
            'COMP_ITEM_DESCRIPTION': name,

            'COMP_ITEM_LONG_DESCRIPTION': description,
            'COMP_SKU': sku,
            'COMP_UDA_LEVEL1': category,
            'COMP_UDA_LEVEL2': sub_category,
            'COMP_REGULAR_PRICE': regular_price,
            'COMP_PROMO_PRICE': discounted_price,
            "COMP_CURRENCY": currency,
            "COMP_ITEM_URL": url,
            "COMP_ITEM_IMAGE_URL": images,
            "COMP_UDA_ATTRIBUTE1": ratings,
            "COMP_UDA_ATTRIBUTE2": Availability,
            'COMP_UDA_ATTRIBUTE3': brand,
            "COMP_UDA_ATTRIBUTE4": {**unprocessed_json},
            "COMP_UDA_ATTRIBUTE6": Features
        }
        results_data.append(parsed_data)
        return results_data
    except Exception as e:
        with open('error.txt', 'a') as f:
            f.write(str(html_file) + '\n')
        print(e, html_file)

all_results = []
count = 0
total_urls = len(product_dumps)
chunk_size = 400000
file_count = 1

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(data_parser, url, file_count): url for url in product_dumps}
    jb = 1
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        count += 1
        jb = jb + 1
        if result is not None:
            print(f"Processed {count}/{total_urls} urls")
            all_results.extend(result)
            if count % chunk_size == 0 or count == len(product_dumps):
                output_file = f"Scheels2.json"
                with open(output_file, 'w') as file:
                    json.dump(all_results, file, indent=4)
                all_results = []
                file_count += 1