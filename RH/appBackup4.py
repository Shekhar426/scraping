import requests
import json
import os
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--start', type=int, required=True, help='Starting row number')
parser.add_argument('--end', type=int, required=True, help='Starting row number')
args = parser.parse_args()

file_path = f'/usr/src/app/Inputs/rh_all.json'

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created at: {folder_path}", end=" | ")
    else:
        print(f"Folder already exists at: {folder_path}")


with open(file_path, 'r') as json_file:
    data = json.load(json_file)

for i in range(int(args.start), int(args.end)):
    products = data[i]
    create_folder(f"/usr/src/app/json_rh/output/{args.start}")
    for product in products:
        # import pdb; pdb.set_trace()
        url = 'https://rh.com/graphql'
        productID = product['url'].split('/')[-1]
        selected_options = [product['Finish']]
        # import pdb; pdb.set_trace()
        try:
            Fabricorleather = product['Fabricorleather']
            selected_options.append(product['Fabricorleather'])
        except:
            Fabricorleather = product['Fabricorleathercode']
            selected_options.append(product['Fabricorleathercode'])

        # finish_name=product['Finish_name'].replace("-","_").replace(" ","_").replace('"','_').replace("$","_").replace("@","_").replace("/","_")
        # FabricorleatherName=product['FabricorleatherName'].replace("-","_").replace(" ","_").replace('"','_').replace("$","_").replace("@","_").replace("/","_")
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
        }

        variables = {
            "productId": productID,
            "userType": "ANONYMOUS",
            "monogrammable": False,
            "postalCode": "94925",
            "currencyCode": "USA",
            "qty": 1,
            "filter": None,
            "siteId": "RH",
            "measureSystem": "imperial",
            "locale": "en-US",
            "shouldFetchSku": True,
            "nextGenDriven": True,
            "shouldFetchCustomProductOptions": False,
            "selectedOptionIds": selected_options
        }

        query = '''
        query LineItemSkuQuery(
            $productId: String!,
            $selectedOptionIds: [String!],
            $userType: String,
            $postalCode: String,
            $currencyCode: String,
            $qty: Int,
            $filter: String,
            $siteId: String,
            $measureSystem: String,
            $locale: String,
            $nextGenDriven: Boolean,
            $shouldFetchSku: Boolean,
            $shouldFetchCustomProductOptions: Boolean
        ) {
            lineItemSku(
                productId: $productId,
                selectedOptionIds: $selectedOptionIds,
                userType: $userType,
                postalCode: $postalCode,
                currencyCode: $currencyCode,
                qty: $qty,
                filter: $filter,
                siteId: $siteId,
                measureSystem: $measureSystem,
                locale: $locale,
                nextGenDriven: $nextGenDriven,
                shouldFetchSku: $shouldFetchSku,
                shouldFetchCustomProductOptions: $shouldFetchCustomProductOptions
            ) {
                ...LineItemSkuDetails
                __typename
            }
        }

        fragment LineItemSkuDetails on ProductSku {
            ...Sku
            __typename
        }

        fragment Sku on ProductSku {
            __typename
            info {
                name
                longDescription
                imageUrl
                maxOrderQty
                skuPriceInfo {
                    currencySymbol
                    listPrice
                    salePrice
                    memberPrice
                    tradePrice
                    contractPrice
                    memberOriginalPrice
                    nextgenDriven
                    onSale
                    onClearance
                    showMemberPrice
                    customProductErrorCode
                    customProductErrorMsg
                    sendCwCustomProductCode
                    __typename
                }
                canadaShippable
                dropship
                shipViaCode
                hasCasingSkus
                casingProduct
                replacementCushionProduct
                __typename
            }
            inventory {
                lineId
                fullSkuId
                atgSkuId
                postalCode
                inventoryCode
                inventoryStatus
                inventoryRemaining
                inventoryMessage
                itemsInStockMessage
                lineItemMessage
                needPostalCode
                postalCodeSpecific
                preOrder
                dateString
                inventoryOnHand
                __typename
            }
            delivery {
                postalCode
                needPostalCode
                deliveryEstimateStatus
                deliveryEstimate
                freightExempt
                shippingSurcharge
                shippingSurchargeAmount
                freightExemptMessage
                deliveryStateMessage
                lineId
                shipVia
                shippingSurcharge
                unlimitedFurnitureDelivery
                currency
                freightExempt
                __typename
            }
            restrictions {
                spo
                giftCertificate
                serviceSku
                monogram
                monogramMessage
                returnPolicyMessage
                preBillMessage
                additionalMessages {
                    curbsideMessage
                    assemblyMessage
                    giftCardMessage
                    railroadMessage
                    mattressFeeMessage
                    cancellableMessage
                    finalSaleMessage
                    __typename
                }
                countryRestrictions
                mattressFeeLocation
                __typename
            }
            fulfillmentEta {
                lineId
                fullSkuId
                atgSkuId
                postalCode
                inventoryCode
                inventoryStatus
                inventoryRemaining
                inventoryMessage
                itemsInStockMessage
                lineItemMessage
                needPostalCode
                postalCodeSpecific
                preOrder
                dateString
                startDateRange
                endDateRange
                eta
                lineType
                __typename
            }
        }
        '''

        payload = {
            'query': query,
            'variables': variables
        }
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

        prod = f"{productID}-{product['Finish']}"
        if response.status_code == 200:
            print('Success!')
            data = response.json()

            output_file = f"/usr/src/app/json_rh/output/{args.start}/{productID}-{finish_name}-{FabricorleatherName}.json"
            with open(output_file, 'a') as file:
                json.dump(data, file, indent=4)
            with open(f'rhapiSuccess.txt', 'a') as f:
                f.write(prod)
                f.write('\n')
        else:
            with open(f'rhapiError.txt', 'a') as f:
                f.write(prod)
                f.write('\n')
            print('Failed to fetch data:', response.status_code)
