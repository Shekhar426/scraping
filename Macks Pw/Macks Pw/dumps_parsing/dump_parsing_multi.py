import logging
from datetime import datetime
import json
import os
import re
from scrapy import Selector
import concurrent.futures

logging.basicConfig(level=logging.DEBUG, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')

product_dumps = []
directory_path = "E:\\dumps_mackspw"

for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        product_dumps.append(os.path.join(directory_path, filename))

def data_parser(html_file, file_count):
    try:
        results_data = []
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        selector = Selector(text=html)
        scrip_tag = selector.xpath("//script[@type='application/ld+json' and contains(., 'sku')]/text()").get()
        modified_data = re.sub(r'"description":".*?[^\\]",', '', scrip_tag, flags=re.DOTALL)
        product_data = json.loads(modified_data)

        # ITEM = int(html_file.replace("E:\\dumps_mackspw\\", "").replace(".html", "").split("_")[1])
        name = product_data.get('name')
        main_sku = product_data.get('sku')
        sku = selector.xpath("//span[@class='product-line-sku-value']/text()").get()
        uom = selector.xpath("//div[@class='price-per-round-amount']/text()").get(default=None)

        if uom is not None:
            uomPrice = uom.replace("($","").replace("per round)","").strip()
            pattern = r'[a-zA-Z\s]+'
            matches = re.findall(pattern, uom)
            comp_uom = ''.join(matches).strip()
        else:
            comp_uom = None
            uomPrice = None

        rating = selector.xpath("//div[@class='global-views-star-rating-area ']/@data-value").get()
        text_values = selector.xpath('//div[@id="product-details-information-tab-content-container-0"]/text() | //div[@id="product-details-information-tab-content-container-0"]/br/following-sibling::text()').getall()
        text_values = [text.strip() for text in text_values if text.strip()]
        if sku is None:
            sku = product_data.get('sku')
        url = product_data.get('url')
        InstanceType = product_data.get('offers')
        varintUrl = None

        if isinstance(InstanceType, dict):
            varintUrl = url
        elif isinstance(InstanceType, list):
            for of in InstanceType:
                if of.get('sku').strip() == sku.strip():
                    varintUrl = of.get('url')
                    break

        description = selector.xpath("//meta[@property='og:description']/@content").get()
        brand = product_data.get('brand')

        price1 = selector.xpath("//small[@aria-label='Old Price']/text()").get()
        price2 = selector.xpath("//span[@class='product-views-price-lead ']/text()").get()

        if price1 is not None and price2 is not None:
            regular_price = price1.replace("$","").strip()
            discout_price = price2.replace("$","").strip()
        elif price1 is not None and price2 is None:
            regular_price = price1.replace("$","").strip()
            discout_price = None
        elif price1 is None and price2 is not None:
            regular_price = price2.replace("$","").strip()
            discout_price = None
        else:
            regular_price = None
            discout_price = None

        department = selector.xpath("//ul[@class='global-views-breadcrumb']/li[3]/text()").get()
        if department is None:
            department = selector.xpath("//ul[@class='global-views-breadcrumb']/li[3]/a/text()").get()
        category = selector.xpath("//ul[@class='global-views-breadcrumb']/li[5]/text()").get()
        if category is None:
            category = selector.xpath("//ul[@class='global-views-breadcrumb']/li[5]/a/text()").get()
        sub_category = selector.xpath("//ul[@class='global-views-breadcrumb']/li[7]/text()").get()
        if sub_category is None:
            sub_category = selector.xpath("//ul[@class='global-views-breadcrumb']/li[7]/a/text()").get()
        availablity = selector.xpath("//span[@class='product-line-stock-msg-out-text']/text()").get()
        if availablity is None:
            availablity = selector.xpath("//span[@class='inventory-display-message-in-stock']/text()").get()
        if availablity is not None:
            availablity = availablity.strip()

        imageList = []
        image_list = selector.xpath("//div[@class='bx-pager-item']/a/img")
        for i in image_list:
            imageurl = i.xpath("./@src").get().split(".jpg?")[0] + ".jpg"
            imageList.append(imageurl)
        if len(imageList) == 0:
            singleImage = selector.xpath("//div[@class='product-details-image-gallery-detailed-image']/img/@src").get().split(".jpg?")[0] + ".jpg"
            if singleImage is not None:
                imageList.append(singleImage)
        unprocessed_json = {}
        ColorLike_Key1 = selector.xpath("(//div[@class='product-views-option-color-label-header'])[1]/label/text()").get()
        ColorLike_Value1 = selector.xpath("(//div[@class='product-views-option-color-label-header'])[1]/span/text()").get()
        if ColorLike_Value1 is not None and ColorLike_Key1 is not None:
            unprocessed_json[ColorLike_Key1.replace(":","").replace(" ","")] = ColorLike_Value1.replace(":","").replace(" ","")

        SizeLike_Key1 = selector.xpath("(//div[@class='custcol_macks_all_sizes-controls-group'])[1]/label/text()").get()
        SizeLike_Value1 = selector.xpath("(//div[@class='custcol_macks_all_sizes-controls-group'])[1]/label/span/text()").get()

        if SizeLike_Value1 is not None and SizeLike_Key1 is not None:
            unprocessed_json[SizeLike_Key1.replace(":","").replace(" ","")] = SizeLike_Value1.replace(":","").replace(" ","")

        # For different case of size >>>>>> if size is not found by above xpath then use below xpath
        if SizeLike_Value1 is None or SizeLike_Key1 is None:
            SizeLike_Key1 = selector.xpath("(//label[@class='product-views-option-tile-label'])[1]/text()").get()
            SizeLike_Value1 = selector.xpath("(//label[@class='product-views-option-tile-label'])[1]/span/text()").get()

            if SizeLike_Value1 is not None and SizeLike_Key1 is not None:
                unprocessed_json[SizeLike_Key1.replace(":", "").replace(" ", "")] = SizeLike_Value1.replace(":", "").replace(" ", "")


            if SizeLike_Value1 is None or SizeLike_Key1 is None:
                SizeLike_Key1 = selector.xpath("(//label[@class='product-views-option-tile-label'])[2]/text()").get()
                SizeLike_Value1 = selector.xpath("(//label[@class='product-views-option-tile-label'])[2]/span/text()").get()
                if SizeLike_Value1 is not None and SizeLike_Key1 is not None:
                    unprocessed_json[SizeLike_Key1.replace(":", "").replace(" ", "")] = SizeLike_Value1.replace(":",
                                                                                                                "").replace(" ", "")
        jb = int(html_file.replace("E:\\dumps_mackspw\\", "").replace(".html", "").split("_")[0])
        if jb < 2501:
            batchId = "MACKSPW_01072024_1"
        elif jb < 5001:
            batchId = "MACKSPW_01072024_2"
        elif jb < 7501:
            batchId = "MACKSPW_01072024_3"
        elif jb < 10001:
            batchId = "MACKSPW_01072024_4"
        elif jb < 12501:
            batchId = "MACKSPW_01072024_5"
        elif jb < 15001:
            batchId = "MACKSPW_01072024_6"
        elif jb < 17501:
            batchId = "MACKSPW_01072024_7"
        elif jb < 20001:
            batchId = "MACKSPW_01072024_8"
        elif jb < 22501:
            batchId = "MACKSPW_01072024_9"
        elif jb < 25001:
            batchId = "MACKSPW_01072024_10"
        else:
            batchId = "MACKSPW_01072024_11"
        parsed_data = {

                       'COMP_UDA_ATTRIBUTE10' : html_file,
                        # 'ITEM' : ITEM,
                       'COMP_ITEM_DESCRIPTION': name.strip(),
                       'COMP_ITEM_URL': url.strip(),
                       'COMP_UDA_ATTRIBUTE1' : varintUrl,
                       "COMP_ITEM_LONG_DESCRIPTION": description,
                       "JOB_ID" : "MACKSPW_01072024",
                        "BATCH_ID" : batchId,
                       'COMP_UDA_LEVEL1': department.strip(),
                       "COMP_UDA_LEVEL2": category.strip(),
                       'COMP_UDA_LEVEL3': sub_category.strip(),
                       'COMP_REGULAR_PRICE': regular_price,
                       'COMP_PROMO_PRICE': discout_price,
                       'COMP_UDA_ATTRIBUTE2': availablity,
                       'COMP_SKU': main_sku.strip(),
                       'COMP_UDA_ATTRIBUTE3': sku.strip(),
                       'COMP_UDA_ATTRIBUTE4': brand.strip(),
                       'COMP_ITEM_IMAGE_URL': imageList,
                       'COMP_UOM' : comp_uom,
                       'COMP_UOM_PRICE' : uomPrice,
                       'COMP_UDA_ATTRIBUTE5' : text_values,
                       'COMP_UDA_ATTRIBUTE6' : rating,
                        'COMP_UDA_ATTRIBUTE7': unprocessed_json,
                        'COMP_UDA_ATTRIBUTE19': "ScrapedON_08082024"

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
chunk_size = 100000
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
                output_file = f"Data_{file_count}.json"
                with open(output_file, 'w') as file:
                    json.dump(all_results, file, indent=4)
                all_results = []
                file_count += 1