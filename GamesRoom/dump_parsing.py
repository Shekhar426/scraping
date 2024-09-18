import json
import os

from scrapy import Selector
from datetime import datetime
path = "C:\dumps_gamesroom"
path_list = []
for file in os.listdir(path):
    if file.endswith(".html"):
        path_list.append(os.path.join(path, file))
count = 1
for i in path_list[:]:
    print(count, end=" ")
    # print(i, end=" ")
    with open(i, 'r', encoding='utf-8') as f:
        html = f.read()
    selector = Selector(text=html)
    url = selector.xpath("//link[@rel='canonical']/@href").get()
    inner_html = selector.xpath("//script[@type='application/ld+json' and contains(.,'sku')]/text()").get().strip()
    if inner_html.startswith('['):
        script_tag = (json.loads(inner_html))[0]
    else:
        inner_html = selector.xpath("//script[@type='application/ld+json' and contains(.,'sku')][2]/text()").get().strip()
        script_tag = (json.loads(inner_html))[0]
    name = script_tag.get('name')
    sku = script_tag.get('sku')
    gtin13 = script_tag.get('gtin13')
    brand = script_tag.get('brand').get('name')
    images = script_tag.get('image')
    description = script_tag.get('description').replace("\n", "").replace("\t", "").replace("\r", "").strip()

    price1 = selector.xpath("//span[@id='old_price_display']/span/text()").get() #Regular Price
    price2 = selector.xpath("//div[@id='our_price_display']/text()").get() # Discounted price
    if price1 is not None and price2 is not None:
        regular_price = price1.replace("€", "").replace(" ", "").replace("EUR", "").replace("\xa0", "").replace("\t", "").replace("\n", "").strip()
        discount_price = price2.replace("€", "").replace(" ", "").replace("EUR", "").replace("\xa0", "").replace("\t", "").replace("\n", "").strip()
    elif price1 is None and price2 is not None:
        regular_price = price2.replace("€", "").replace(" ", "").replace("EUR", "").replace("\xa0", "").replace("\t", "").replace("\n", "").strip()
        discount_price = None
    else:
        regular_price = None
        discount_price = None
    category = selector.xpath("(//ul[@class='breadcrumb clearfix']//a)[2]/@title").get()
    sub_category = selector.xpath("(//ul[@class='breadcrumb clearfix']//a)[3]/@title").get()
    keys = selector.xpath("//table[@class='table-data-sheet']//tr/td[1]")
    values = selector.xpath("//table[@class='table-data-sheet']//tr/td[2]")
    unprocessed_json = {}
    for i in range(len(keys)):
        key = keys[i].xpath("./text()").get().replace('\n', '').replace('\t', '').strip().replace(' ', '')
        if key == "Konsole":
            continue
        value = values[i].xpath("./text()").get().replace('\n', '').replace('\t', '').strip().replace(' ', '')
        unprocessed_json[key] = value
    price_valid_until = script_tag.get('offers').get('priceValidUntil')
    available = script_tag.get('offers').get('availability')
    item_condition = script_tag.get('offers').get('itemCondition')
    product_id = selector.xpath("//span[@class='product-id']/text()").get()
    unprocessed_json['price_valid_until'] = price_valid_until
    unprocessed_json['available'] = available
    unprocessed_json['item_condition'] = item_condition
    unprocessed_json['product_id'] = product_id
    parsed_data = {'time_stamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'tenant_id': "Topo Centras",
                   'competitor_name': "Game Room",
                   'title': name,
                   "gtin": gtin13,
                   "brand": brand,
                   "category": category,
                   'sub_category': sub_category,
                   'regular_price': regular_price,
                   'discounted_price': discount_price,
                   "image_url": images,
                   "priceCurrency": "EUR",
                   "item_url": url,
                   "item_number": sku,
                   'description': description,
                   "unprocessed_json": {**unprocessed_json}}
    json_file_path = 'gameroom.json'
    print(parsed_data)
    # Function to append a dictionary to a list and save it to a JSON file
    def append_dict_to_list_and_save(dictionary, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(dictionary)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    append_dict_to_list_and_save(parsed_data, json_file_path)
    count += 1

