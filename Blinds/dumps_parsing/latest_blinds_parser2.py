import logging
from datetime import datetime
import json
import os
from scrapy import Selector
import concurrent.futures
logging.basicConfig(level=logging.DEBUG, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')


tenant_id = 'Blinds'
competitor_name = 'https://blinds.com/'
product_dumps = []
url = 67
directory_path = f"D:\\Google Drive\\{url}"

for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        product_dumps.append(os.path.join(directory_path, filename))

def data_parser(html_file):
    try:
        results_data = []
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        selector = Selector(text=html)

        regular_price = selector.xpath("//section[@id='gcc-pip-summary']//meta[@itemprop='price']/@content").get()
        if regular_price:
            COMP_REGULAR_PRICE = regular_price
        else:
            COMP_REGULAR_PRICE = None
        comp_item_description = selector.xpath("//h1[@data-testid='productName']/text()").get()
        if comp_item_description:
            comp_item_description = comp_item_description
        else:
            comp_item_description = None

        comp_item_long_description = selector.xpath("//div[@id='gcc-pip-description']//text()").get()
        if comp_item_long_description:
            comp_item_long_description = comp_item_long_description
        else:
            comp_item_long_description = None

        images_urls = selector.xpath('//img[@alt= "Product Preview"]/@src').get()
        if images_urls:
            images_urls = images_urls
        else:
            images_urls = None

        COMP_PROMO_PRICE = selector.xpath('//div/@data-react-discountprice').get()
        if COMP_PROMO_PRICE:
            COMP_PROMO_PRICE = COMP_PROMO_PRICE
        else:
            COMP_PROMO_PRICE = None

        url = selector.xpath("//link[@rel='canonical']/@href").get()
        if url:
            comp_url = url
        else:
            comp_url = None
        level1 = selector.xpath("//nav[@data-testid = 'breadcrumb']/ol/li[1]/a//text()").get()
        if level1:
            COMP_UDA_LEVEL1 = level1
        else:
            COMP_UDA_LEVEL1 = None

        level2 = selector.xpath("//nav[@data-testid = 'breadcrumb']/ol/li[2]/a//text()").get()
        if level2:
            COMP_UDA_LEVEL2 = level2
        else:
            COMP_UDA_LEVEL2 = None

        level3 = selector.xpath("//nav[@data-testid = 'breadcrumb']/ol/li[3]/a//text()").get()
        if level3:
            COMP_UDA_LEVEL3 = level3
        else:
            COMP_UDA_LEVEL3 = None

        rating = selector.xpath("//meta[@itemprop = 'ratingValue']/@content").get()
        if rating:
            COMP_UDA_ATTRIBUTE2 = rating
        else:
            COMP_UDA_ATTRIBUTE2 = None

        review = selector.xpath("//span[@itemprop='ratingCount']/text()").get()
        if review:
            COMP_UDA_ATTRIBUTE3 = review
        else:
            COMP_UDA_ATTRIBUTE3 = None

        color = selector.xpath("//div[text() ='Selected Color']/following-sibling::div/text()").get()
        if color:
            COMP_UDA_ATTRIBUTE4 = color
        else:
            COMP_UDA_ATTRIBUTE4 = None
        second_color = selector.xpath("(//div[@class='gcc-swatch relative lh-title br3 ba overflow-hidden gcc-swatch-selected bw2 b--blue']//figure/figcaption)[2]/text()").get()

        if second_color:
            COMP_UDA_ATTRIBUTE9 = second_color
        else:
            COMP_UDA_ATTRIBUTE9 = None

        brand = selector.xpath("//span[@data-testid='productBrand']/text()").get()
        if brand:
            COMP_UDA_ATTRIBUTE6 = brand
        else:
            COMP_UDA_ATTRIBUTE6 = None

        width = selector.xpath("//div[text()='Width']/following-sibling::div//select[@id='widthWholeDropDown']/option[@selected]/text()").get()
        if width:
            COMP_UDA_ATTRIBUTE7 = width
        else:
            COMP_UDA_ATTRIBUTE7 = None

        height = selector.xpath("//select[@id='wholeHeightDropdown']/option[@selected]/text()").get()
        if height:
            COMP_UDA_ATTRIBUTE8 = height
        else:
            COMP_UDA_ATTRIBUTE8 = None

        strong_tags = selector.xpath("//div[@id='gcc-pip-specs-content']/div/div/p/strong/text()").getall()
        unprocessed_data = {}
        for i in range(len(strong_tags)):
            key = strong_tags[i].strip()
            values = selector.xpath(f"(//div[@id='gcc-pip-specs-content']/div/div/p)[{i + 1}]/following-sibling::ul/li/text()").getall()
            valuesList = []
            for j in values:
                valuesList.append(j.strip())
            unprocessed_data[key] = valuesList
        parsed_data = {
            'COMP_UDA_ATTRIBUTE10': html_file,
            'COMP_ITEM_URL': comp_url,
            'COMP_ITEM_DESCRIPTION': comp_item_description,
            'COMP_ITEM_LONG_DESCRIPTION': comp_item_long_description,
            'COMP_PROMO_PRICE': COMP_PROMO_PRICE,
            'COMP_REGULAR_PRICE': COMP_REGULAR_PRICE,
            # 'COMP_UDA_ATTRIBUTE1': COMP_UDA_ATTRIBUTE1,
            'COMP_UDA_ATTRIBUTE2': COMP_UDA_ATTRIBUTE2,
            'COMP_UDA_ATTRIBUTE3': COMP_UDA_ATTRIBUTE3,
            'COMP_UDA_ATTRIBUTE4': COMP_UDA_ATTRIBUTE4,
            'COMP_UDA_ATTRIBUTE6': COMP_UDA_ATTRIBUTE6,
            'COMP_UDA_ATTRIBUTE7': COMP_UDA_ATTRIBUTE7,
            'COMP_UDA_ATTRIBUTE8': COMP_UDA_ATTRIBUTE8,
            'COMP_UDA_ATTRIBUTE9':COMP_UDA_ATTRIBUTE9,
            'COMP_UDA_LEVEL1': COMP_UDA_LEVEL1,
            'COMP_UDA_LEVEL2': COMP_UDA_LEVEL2,
            'COMP_UDA_LEVEL3': COMP_UDA_LEVEL3,
            'COMP_ITEM_IMAGE_URL': str(images_urls),
            'COMP_UDA_ATTRIBUTE5': unprocessed_data
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
chunk_size = 10000000000000000
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
                output_file = f"blinds_{url}.json"
                with open(output_file, 'w') as file:
                    json.dump(all_results, file, indent=4)
                all_results = []
                file_count += 1