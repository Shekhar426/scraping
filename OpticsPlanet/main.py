import json
import os
import re
from scrapy import Selector
from datetime import datetime

path = "dumps_opticsplanet"
path_list = []
for file in os.listdir(path):
    if file.endswith(".html"):
        path_list.append(os.path.join(path, file))
count = 1
variant_count = 0
for i in path_list[:]:
    dump_number = i.replace(".html", "").replace("C:\\dumps_opticsplanet\\", "")
    # print(f"Dumps Completed : {count} | Total Variant Found : {variant_count} |Dump Number : {dump_number}")
    print(f"Dumps Completed : {count} | Total Variant Found : {variant_count} | Dump Number : {dump_number}")

    with open('json_matching.json', 'r') as f:
        data = json.load(f)
    searched_upc = ''
    for key, item in data.items():
        if key == dump_number:
            gd_url = item['url']
            searched_upc = re.findall(r'\d+$', gd_url)[-1]
            break
    try:
        with open(i, 'r', encoding='utf-8') as f:
            html = f.read()
        selector = Selector(text=html)
        no_product_ele = selector.xpath("//div[@class='product-promotion-block']//h2[contains(.,'Product No Longer Available')] | //div[@class='product-promotion-block']//h2[contains(.,'Product Discontinued by Manufacturer')] | //div[@class='product-promotion-block']//h2[contains(.,'Product Not Available for Order Yet')] | //span[@class='dHwEVK' and contains(.,'Product No Longer Available')] | //div[@class='product-promotion-block']//h2[contains(.,'Promotional Item Not Available for Purchase')] | //div[@class='product-promotion-block']//h2[contains(.,'Product Temporarily Unavailable')] | //h3[@class='YB0JPr' and contains(.,'This page is for information purpose only')]").get()
        if not no_product_ele:
            stock_status = 'In Stock'
            script_tag = selector.xpath("//script[@type='application/ld+json' and contains(.,'sku')]/text()").get(default='')
            product_data = json.loads(script_tag, strict=False)
            item = product_data.get('name', '')
            sku = product_data.get('sku', '')
            brand = product_data.get('brand', {}).get('name', '')
            description = product_data.get('description', '')
            url = product_data.get('url', '')
            # print(url)
            image_urls = []
            image_url_ele = selector.xpath("//div[@class='gallery-main-image-scrollable']//div//picture//img[@src]")
            for image_url in image_url_ele:
                image_src_url = image_url.xpath("./@src").get(default='')
                image_urls.append(image_src_url)
            if len(description) > 10000:
                description = description[:9000]
            else:
                description = description
            rating = product_data.get('aggregateRating', {}).get('ratingValue', None)
            cat_script_tag = selector.xpath("//script[@type='application/ld+json' and contains(.,'BreadcrumbList')]/text()").get(default='')
            cat_data = json.loads(cat_script_tag, strict=False)
            if len(cat_data['itemListElement']) > 1:
                category = cat_data['itemListElement'][1]['item'].get('name', '')
                sub_category = cat_data['itemListElement'][2]['item'].get('name', '')
            else:
                category = cat_data['itemListElement'][0]['item'].get('name', '')
                sub_category = ''
            Specification_list = selector.xpath("(//table)[1]/tbody/tr")
            specification = {}
            for j, spec_row in enumerate(Specification_list):
                key = spec_row.xpath(f"td[1]/text()").get(default='').replace(':', '')
                value = spec_row.xpath(f"td[2]/text()").get(default='').replace(':', '')
                specification[key.replace('\n', ' ').replace('\xa0', '')] = value.replace('\n', ' ').replace('\xa0', '')
            weight = ''
            for key in specification.keys():
                if "Weight" in key or "weight" in key:
                    weight = specification.get(key)
                    break
            size = ''
            for key in specification.keys():
                if "Size" in key or "size" in key:
                    size = specification.get(key)
                    break
            variants = selector.xpath("//div[@id='variantSelectorDefault']//div[@role='presentation']")
            if variants:
                variant_list = []
                for variant in variants:
                    variant_info = {}
                    common_info_elements = variant.xpath(".//div[@class='UTi2HC']//div[@data-for='variantSelector']//div[@class='umvEY9']//div//span[@class='IpNPnb']")
                    for info_element in common_info_elements:
                        key = info_element.xpath("strong/text()").get(default='').rstrip(':')
                        value = info_element.xpath("text()").get(default='')
                        variant_info[key] = value
                    additional_info_elements = variant.xpath(".//div[@class='UTi2HC']//div[@data-for='variantSelector']//div[@class='umvEY9']//p[@class='nBUOJt']")
                    for info_element in additional_info_elements:
                        key = info_element.xpath("span/text()").get(default='').rstrip(':').replace(': ', '')
                        value = info_element.xpath("text()").get(default='').strip()
                        variant_info[key] = value
                    regular_price_ele = variant.xpath(".//div[@class='UTi2HC']//div[@class='xaIMsU']//div//div[@class='XpXf4h']//div[@class='CTolU1']")
                    for reg_price in regular_price_ele:
                        key = 'Regular Price'
                        value = reg_price.xpath(".//div//s[@class='k4ELxW']/text()").get(default='')
                        variant_info[key] = value
                    discounted_price_ele = variant.xpath(".//div[@class='UTi2HC']//div[@class='xaIMsU']//div//div[@class='XpXf4h']")
                    for dis_price in discounted_price_ele:
                        key = 'Discounted Price'
                        value = dis_price.xpath(".//div//span[@class='PvloAJ']/text()").get(default='')
                        variant_info[key] = value
                    variant_list.append(variant_info)
                keys_to_exclude = ['Regular Price', 'Discounted Price', 'UPC']
                for output_1 in variant_list:
                    filtered_output = {key: value for key, value in output_1.items() if
                                       key not in keys_to_exclude}
                    regular_price = output_1.get('Regular Price')
                    discounted_price = output_1.get('Discounted Price')
                    if regular_price is not None and discounted_price is not None:
                        regular_price = regular_price.replace('$', '')
                        discounted_price = discounted_price.replace('$', '')
                    elif regular_price is not None and discounted_price is None:
                        regular_price = regular_price.replace('$', '')
                        discounted_price = ""
                    elif regular_price is None and discounted_price is not None:
                        regular_price = discounted_price
                        discounted_price = ""
                    else:
                        regular_price = ""
                        discounted_price = ""
                    parsed_data = {
                        'time_stamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'tenant_id': "Brownells",
                        'competitor_name': "www.opticsplanet.com",
                        'upc': output_1.get('UPC', ''),
                        "brownells_upc" : searched_upc,
                        'sku': sku,
                        'title': item,
                        'competitor_url': url,
                        'brand': brand,
                        'category': category,
                        'image_url': image_urls,
                        'description': description,
                        'sub_category': sub_category,
                        'stock_status': stock_status,
                        'rating': rating,
                        'size': size,
                        'weight': weight,
                        'regular_price': regular_price or None,
                        'effective_price': discounted_price or None,
                        'unprocessed_json': {
                            **specification,
                            **filtered_output
                        }}
                    # print(parsed_data)
                    variant_count = variant_count + 1

                    json_file_path = 'opticsplanet.json'
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
                    variant_count = variant_count + 1
                count += 1
            else:
                no_variant = selector.xpath("//div[@id='variantSelectorDefault']//div[@data-qa-variant-id]")
                variant_list = []
                for variant in no_variant:
                    variant_info = {}
                    common_info_elements = variant.xpath(
                        ".//div[@class='UTi2HC TohfKR']//div//div[@class='umvEY9']//div//span[@class='IpNPnb']")
                    for info_element in common_info_elements:
                        key = info_element.xpath("strong/text()").get(default='').rstrip(':')
                        value = info_element.xpath("text()").get(default='')
                        variant_info[key] = value
                    additional_info_elements = variant.xpath(
                        ".//div[@class='UTi2HC TohfKR']//div//div[@class='umvEY9']//p[@class='nBUOJt']")
                    for info_element in additional_info_elements:
                        key = info_element.xpath("span/text()").get(default='').rstrip(':').replace(': ', '')
                        value = info_element.xpath("text()").get(default='').strip()
                        variant_info[key] = value
                    regular_price_ele = variant.xpath(
                        ".//div[@class='UTi2HC TohfKR']//div[@class='xaIMsU']//div//div[@class='CTolU1']")
                    for reg_price in regular_price_ele:
                        key = 'Regular Price'
                        value = reg_price.xpath(".//div//s[@class='k4ELxW']/text()").get(default='')
                        variant_info[key] = value
                    discounted_price_ele = variant.xpath(".//div[@class='UTi2HC TohfKR']//div[@class='xaIMsU']")
                    for dis_price in discounted_price_ele:
                        key = 'Discounted Price'
                        value = dis_price.xpath(".//div//div//span[@class='PvloAJ']/text()").get(default='')
                        variant_info[key] = value
                    variant_list.append(variant_info)
                keys_to_exclude = ['Regular Price', 'Discounted Price', 'UPC']
                for output_2 in variant_list:
                    filtered_output = {key: value for key, value in output_2.items() if
                                       key not in keys_to_exclude}
                    regular_price = output_2.get('Regular Price')
                    discounted_price = output_2.get('Discounted Price')
                    if regular_price is not None and discounted_price is not None:
                        regular_price = regular_price.replace('$', '')
                        discounted_price = discounted_price.replace('$', '')
                    elif regular_price is not None and discounted_price is None:
                        regular_price = regular_price.replace('$', '')
                        discounted_price = ""
                    elif regular_price is None and discounted_price is not None:
                        regular_price = discounted_price
                        discounted_price = ""
                    else:
                        regular_price = ""
                        discounted_price = ""
                    parsed_data = {
                        'time_stamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'tenant_id': "Brownells",
                        'competitor_name': "www.opticsplanet.com",
                        'upc': output_2.get('UPC', ''),
                        "brownells_upc" : searched_upc,
                        'sku': sku,
                        'title': item,
                        'competitor_url': url,
                        'brand': brand,
                        'category': category,
                        'image_url': image_urls,
                        'description': description,
                        'sub_category': sub_category,
                        'stock_status': stock_status,
                        'rating': rating,
                        'size': size,
                        'weight': weight,
                        'regular_price': regular_price or None,
                        'effective_price': discounted_price or None,
                        'unprocessed_json': {
                            **specification,
                            **filtered_output
                        }}
                    # print(parsed_data)
                    json_file_path = 'opticsplanet.json'
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
                    variant_count = variant_count + 1
                count += 1
        else:
            # print(f"no product found for {i}")
            with open('error1.txt', 'a') as f:
                f.write(str(dump_number) + '\n')
            variant_count = variant_count + 1
            count += 1
    except Exception as e:
        # print(dump_number, "Error Occoured")
        with open('error1.txt', 'a') as f:
            f.write(str(dump_number) + '\n')
        variant_count = variant_count + 1
        count += 1