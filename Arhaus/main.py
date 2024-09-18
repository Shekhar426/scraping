import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

urls = ["https://www.arhaus.com/products/remington-two-over-two-sofa?variant=43102153375915", "https://www.arhaus.com/products/kipton-sofa?variant=43147359944875", "https://www.arhaus.com/products/beale-sofa?variant=42374722453675", "https://www.arhaus.com/products/ashby-sofa?variant=42880461209771", "https://www.arhaus.com/products/landsbury-sofa?variant=43110946930859", "https://www.arhaus.com/products/kaplan-sofa?variant=42864636657835", "https://www.arhaus.com/products/beale-four-piece-sectional?variant=43140891967659", "https://www.arhaus.com/products/parsons-dining-table-in-abanos?variant=42754370797739", "https://www.arhaus.com/products/kensington-dining-table?variant=43140855038123", "https://www.arhaus.com/products/mila-dining-chairs?variant=41426781798571", "https://www.arhaus.com/products/rodin-dining-side-chair-in-vesuvio-black?variant=42847688327339", "https://www.arhaus.com/products/pelle-dining-side-chair?variant=40869964939435", "https://www.arhaus.com/products/aimee-arm-chair-in-black-drifted?variant=41770182705323", "https://www.arhaus.com/products/canterbury-dining-chair?variant=43074258600107", "https://www.arhaus.com/products/finnley-dining-table?variant=42862901166251", "https://www.arhaus.com/products/noa-dining-chair-in-cinder?variant=43141319983275", "https://www.arhaus.com/products/bottoni-dining-chair?variant=40869737562283", "https://www.arhaus.com/products/samantha-dining-arm-chair?variant=42834718982315", "https://www.arhaus.com/products/geoffrey-dining-side-chair?variant=42401805303979", "https://www.arhaus.com/products/panta-dining-table?variant=43140903731371", "https://www.arhaus.com/products/kira-swivel-dining-chair-in-nomad-snow?variant=42754364702891", "https://www.arhaus.com/products/mihaela-dining-table?variant=42397730865323", "https://www.arhaus.com/products/margot-cane-back-dining-chair-in-stone-vintage?variant=42150535856299", "https://www.arhaus.com/products/whitby-extension-dining-table-in-honey?variant=43141449416875", "https://www.arhaus.com/products/lunden-dining-side-chair?variant=42016046383275", "https://www.arhaus.com/products/park-dining-table?variant=42163121389739", "https://www.arhaus.com/products/henry-dining-side-chair?variant=41724476883115", "https://www.arhaus.com/products/jacob-round-dining-table-with-tulip-base?variant=42070618177707", "https://www.arhaus.com/products/malone-nightstand?variant=41487143600299", "https://www.arhaus.com/products/malone-wide-dresser?variant=42423735189675", "https://www.arhaus.com/products/henley-wide-dresser?variant=40869316001963", "https://www.arhaus.com/products/henley-nightstand?variant=42360383996075", "https://www.arhaus.com/products/st-martin-bed?variant=42103389520043", "https://www.arhaus.com/products/finnley-bed?variant=42837806481579", "https://www.arhaus.com/products/polanco-bed?variant=42845867016363", "https://www.arhaus.com/products/finnley-closed-nightstand?variant=42251407261867", "https://www.arhaus.com/products/finnley-wide-dresser?variant=42051147595947", "https://www.arhaus.com/products/polanco-closed-nightstand?variant=42834605834411", "https://www.arhaus.com/products/polanco-six-drawer-dresser?variant=42730211770539", "https://www.arhaus.com/products/adalynn-bed?variant=42871800135851", "https://www.arhaus.com/products/bodhi-tall-nightstand?variant=41785796952235", "https://www.arhaus.com/products/bodhi-six-drawer-dresser?variant=40869106909355", "https://www.arhaus.com/products/corey-closed-nightstand?variant=42946921300139", "https://www.arhaus.com/products/corey-six-drawer-dresser?variant=42847303205035", "https://www.arhaus.com/products/lago-bed?variant=42154412474539", "https://www.arhaus.com/products/malone-bed?variant=42373659885739", "https://www.arhaus.com/products/st-martin-closed-nightstand?variant=42070816325803", "https://www.arhaus.com/products/st-martin-six-drawer-dresser?variant=42065085661355", "https://www.arhaus.com/products/malone-media-console?variant=41232712990891", "https://www.arhaus.com/products/palmer-glass-coffee-table?variant=42062244544683", "https://www.arhaus.com/products/kensington-glass-buffet?variant=42029656244395", "https://www.arhaus.com/products/malone-plinth-coffee-table?variant=42373614469291", "https://www.arhaus.com/products/aviana-coffee-table?variant=41289416999083", "https://www.arhaus.com/products/sullivan-four-door-media-console?variant=43146223059115", "https://www.arhaus.com/products/finnley-media-console?variant=40869946425515", "https://www.arhaus.com/products/leandro-coffee-table?variant=42397751804075", "https://www.arhaus.com/products/corey-sideboard?variant=42062256832683", "https://www.arhaus.com/products/owen-three-piece-sectional?variant=40869835800747", "https://www.arhaus.com/products/remington-three-piece-sectional?variant=42814583636139", "https://www.arhaus.com/products/kaplan-two-piece-chaise-sectional?variant=42849481162923", "https://www.arhaus.com/products/finnley-coffee-table?variant=42363447640235"]

for url in urls[:]:
    data = {}
    driver.get(url)
    script_tag  = driver.find_element(By.XPATH, "//script[@type='application/ld+json' and contains(.,'sku')]")
    json_object = script_tag.get_attribute('innerHTML')
    product_data = json.loads(json_object, strict=False)
    item_name = product_data.get('name')
    brand = product_data.get('brand').get("name")
    total_prod = product_data.get('offers')
    main_sku = product_data.get('sku')
    category = product_data.get('category').get('name')

    for i in range(len(total_prod)):
        variant_url = product_data.get('offers')[i].get('url')
        sku = product_data.get('offers')[i].get('sku')
        price = product_data.get('offers')[i].get('price')
        price_currency = product_data.get('offers')[i].get('priceCurrency')
        availablity = product_data.get('offers')[i].get('availability').replace("https://schema.org/", "")
        price_valid_until = product_data.get('offers')[i].get('priceValidUntil')
        data['title'] = item_name
        data['sku'] = main_sku
        data['variant_sku'] = sku
        data['url'] = variant_url
        data['brand'] = brand
        data['regular_price'] = price
        data['category'] = category
        data['unprocessed_json'] = {"price_currency":price_currency, "price_valid_until":price_valid_until, "availablity":availablity}
