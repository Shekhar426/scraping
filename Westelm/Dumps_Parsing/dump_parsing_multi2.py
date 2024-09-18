import logging
from datetime import datetime
import json
import os
from scrapy import Selector
import concurrent.futures

logging.basicConfig(level=logging.DEBUG, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')

tenant_id = 'Living Furniture'
competitor_name = 'WestElm'
product_dumps = []
directory_path = "E:\\dumps_westelm2"

for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        product_dumps.append(os.path.join(directory_path, filename))
def data_parser(html_file):
    try:
        results_data = []
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        selector = Selector(text=html)

        name = selector.xpath("//div[@data-style='product-title-wrapper']/h1/text()").get()
        if name is None:
            name = selector.xpath("//div[@data-test-id='nla-title-container']/h1/text()").get()
        url = selector.xpath("//link[@rel='canonical']/@href").get()
        sku = selector.xpath("//p[@data-test-id='sku-display']/text()").get()
        if sku is not None:
            sku = sku.replace(" ", "").replace("SKU:", "").replace("\n", "")
            varientUrl = url + "?sku=" + sku
        else:
            varientUrl = ""
        description = selector.xpath("//meta[@name='description']/@content").get()
        if description is not None:
            description = description.replace("<h6>", " ").replace("</h6>", " ").replace("<li>", " ").replace("</li>",
                                                                                                              " ").replace(
                "\n", " ").replace("<ul>", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
        category = selector.xpath("(//ul[@id='breadcrumbs']//span)[1]/text()").get()
        sub_category = selector.xpath("(//ul[@id='breadcrumbs']//span)[2]/text()").get()
        regular_price = None
        discounted_price = None
        price1 = selector.xpath("//span[@data-style='product-pricing-amount']/text()").get()
        if price1 is not None:
            regular_price = price1
            discounted_price = None
        if price1 is None:
            regular_price = selector.xpath("//span[@data-test-id='suggested-price-amount']/text()").get()
            discounted_price = selector.xpath("//span[@data-test-id='sale-or-our-price-amount']/text()").get()
        if regular_price is not None:
            regular_price = float(regular_price.replace(",", ""))
        if discounted_price is not None:
            discounted_price = float(discounted_price.replace(",", ""))
        unprocessed_json = {}
        images = []
        image_list = selector.xpath(
            "//div[@class='sliding-images-outer horizontal-indicators']//li[contains(@class, 'hooper-slide')]//img")
        for i in image_list:
            imageurl = i.xpath("./@data-src").get()
            images.append(imageurl.replace("f.jpg", "o.jpg"))
        elements = selector.xpath(
            "//div[@data-test-id='guided-accordion']//div[contains(@data-test-id, 'guided-accordion-item')]")
        for i in elements:
            key = i.xpath(".//div[@data-test-id='guided-accordion-header-title']/text()").get().strip().replace("\\n",
                                                                                                                "")
            value = i.xpath(".//div[@data-test-id='guided-accordion-header-attribute-value']/text()").get()
            unprocessed_json[key] = value
        dimensions = selector.xpath(
            "//div[@data-test-id='productDimensions-desktop-accordion-component']//div[@data-test-id='product-dimensions-data']//li")
        for index, element in enumerate(dimensions):
            if index % 2 == 0:  # Even index elements are keys
                key = element.xpath("text()").get().strip().replace("\n", "")
            else:  # Odd index elements are values
                value = element.xpath("text()").get().strip().replace("\n", "")
                unprocessed_json[key] = value
        li_elements = selector.xpath("//div[@data-test-id='product-details-description']//li")
        li_texts = [li.xpath('string(.)').get().strip() for li in li_elements]
        unprocessed_json["Product Details"] = li_texts
        parsed_data = {
            'COMP_ITEM_DESCRIPTION': name,
            'COMP_ITEM_LONG_DESCRIPTION': description,
            'COMP_SKU': sku,
            'COMP_UDA_LEVEL1': category,
            'COMP_UDA_LEVEL2': sub_category,
            'COMP_REGULAR_PRICE': regular_price,
            'COMP_PROMO_PRICE': discounted_price,
            "COMP_CURRENCY": "USD",
            "COMP_ITEM_URL": url,
            "COMP_UDA_ATTRIBUTE5": varientUrl,
            "COMP_ITEM_IMAGE_URL": images,
            "COMP_UDA_ATTRIBUTE4": {**unprocessed_json}}
        results_data.append(parsed_data)
        return results_data

    except Exception as e:
        with open('error.txt', 'a') as f:
            f.write(str(html_file) + '\n')
        print(e, html_file)

all_results = []
count = 0
total_urls = len(product_dumps)
chunk_size = 10000000
file_count = 1

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(data_parser, url): url for url in product_dumps}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        count += 1
        if result is not None:
            print(f"Processed {count}/{total_urls} urls")
            all_results.extend(result)
            if count % chunk_size == 0 or count == len(product_dumps):
                output_file = f"Westelm2_{file_count}.json"
                with open(output_file, 'w') as file:
                    json.dump(all_results, file, indent=4)
                all_results = []
                file_count += 1