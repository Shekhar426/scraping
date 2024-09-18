import requests
import json
import os
import argparse
from requests.exceptions import RequestException

import time

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('--start', type=int, required=True, help='Starting row number')
# parser.add_argument('--end', type=int, required=True, help='Starting row number')
# args = parser.parse_args()


def dump_download(i):
    # max_retries=3
    products = data[i]
    for product in products:
        max_retries = 3
        while max_retries:
            print(product['url'])
            url = 'https://rh.com/graphql'
            productID = product['url'].split('/')[-1]
            selected_options = [product['Finish']]
            if product['Fabricorleather']:
                selected_options.append(product['Fabricorleather'])

            headers = {'accept': 'application/json', 'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'}

            variables = {"productId": productID, "userType": "ANONYMOUS", "monogrammable": False, "postalCode": "94925", "currencyCode": "USA", "qty": 1, "filter": None, "siteId": "RH", "measureSystem": "imperial", "locale": "en-US", "shouldFetchSku": True, "nextGenDriven": True, "shouldFetchCustomProductOptions": False, "selectedOptionIds": selected_options}

            query = ''' query LineItemSkuQuery( $productId: String!, $selectedOptionIds: [String!], $userType: String, $postalCode: String, $currencyCode: String, $qty: Int, $filter: String, $siteId: String, $measureSystem: String, $locale: String, $nextGenDriven: Boolean, $shouldFetchSku: Boolean, $shouldFetchCustomProductOptions: Boolean ) { lineItemSku( productId: $productId, selectedOptionIds: $selectedOptionIds, userType: $userType, postalCode: $postalCode, currencyCode: $currencyCode, qty: $qty, filter: $filter, siteId: $siteId, measureSystem: $measureSystem, locale: $locale, nextGenDriven: $nextGenDriven, shouldFetchSku: $shouldFetchSku, shouldFetchCustomProductOptions: $shouldFetchCustomProductOptions ) { ...LineItemSkuDetails __typename } } fragment LineItemSkuDetails on ProductSku { ...Sku __typename } fragment Sku on ProductSku { __typename info { name longDescription imageUrl maxOrderQty skuPriceInfo { currencySymbol listPrice salePrice memberPrice tradePrice contractPrice memberOriginalPrice nextgenDriven onSale onClearance showMemberPrice customProductErrorCode customProductErrorMsg sendCwCustomProductCode __typename } canadaShippable dropship shipViaCode hasCasingSkus casingProduct replacementCushionProduct __typename } inventory { lineId fullSkuId atgSkuId postalCode inventoryCode inventoryStatus inventoryRemaining inventoryMessage itemsInStockMessage lineItemMessage needPostalCode postalCodeSpecific preOrder dateString inventoryOnHand __typename } delivery { postalCode needPostalCode deliveryEstimateStatus deliveryEstimate freightExempt shippingSurcharge shippingSurchargeAmount freightExemptMessage deliveryStateMessage lineId shipVia shippingSurcharge unlimitedFurnitureDelivery currency freightExempt __typename } restrictions { spo giftCertificate serviceSku monogram monogramMessage returnPolicyMessage preBillMessage additionalMessages { curbsideMessage assemblyMessage giftCardMessage railroadMessage mattressFeeMessage cancellableMessage finalSaleMessage __typename } countryRestrictions mattressFeeLocation __typename } fulfillmentEta { lineId fullSkuId atgSkuId postalCode inventoryCode inventoryStatus inventoryRemaining inventoryMessage itemsInStockMessage lineItemMessage needPostalCode postalCodeSpecific preOrder dateString startDateRange endDateRange eta lineType __typename } } '''

            payload = {'query': query, 'variables': variables}
            try:
                if product['Finish_name'] != None:
                    finish_name = product['Finish_name'].replace("-", "_").replace(" ", "_").replace('"', '_').replace(
                        "$", "_").replace("@", "_").replace("/", "_")
                else:
                    finish_name = None
            except:
                finish_name = None
            try:
                FabricorleatherName = product['FabricorleatherName'].replace("-", "_").replace(" ", "_").replace('"',
                                                                                                                 '_').replace(
                    "$", "_").replace("@", "_").replace("/", "_")
            except:
                FabricorleatherName = None
                # FabricorleatherName=product['Fabricorleather_name'].replace("-","_").replace(" ","_").replace('"','_').replace("$","_").replace("@","_").replace("/","_")
            response = requests.post(url, headers=headers, json=payload)  # , proxies=proxy)
            if response.status_code == 200:
                print('Success!')
                print(payload, headers)
            else:
                print('Failed to fetch data:', response.status_code)
                print(payload, headers)

            time.sleep(5)
            prod = f"{productID}-{product['Finish']}-{product['Fabricorleather']}"
            try:
                if response.status_code == 200:
                    print('Success!')
                    resp_data = response.json()
                    output_file = f"{productID}-{finish_name}-{FabricorleatherName}.json"
                    with open(output_file, 'a') as file:
                        json.dump(resp_data, file, indent=4)
                    with open(f'rhapiSuccess.txt', 'a') as f:
                        f.write(prod)
                        f.write('\n')
                    break
                else:
                    max_retries -= 1
                    print(f"Attempt {max_retries}: Received status code {response.status_code}. Retrying...")

            except RequestException as e:
                print(f"Attempt {max_retries}: Error occurred: {e}. Retrying...")
                with open(f'rhapiError.txt', 'a') as f:
                    f.write(prod)
                    f.write('\n')
                print('Failed to fetch data:', response.status_code)


file_path = f'rh_all.json'
with open(file_path, 'r') as json_file:
    data = json.load(json_file)
for i in range(1, 2):
    dump_download(i)
