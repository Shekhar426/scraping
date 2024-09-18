import json
import os
import pandas as pd
import snowflake.connector as sf_account
from snowflake.connector.pandas_tools import write_pandas


def get_connection_obj():
    try:
        conn = sf_account.connect(
            account="oma07528",
            user="dev_etl_user_ecom",
            password="pmhjpxfnkwqzrcqz",
            database="COMP_DATA",
            schema="ML",
            warehouse="DEV",
            role="DEV_ETL_ROLE",
        )
        print("DB Connection established successfully.")
    except Exception as e:
        raise Exception("Connection issue a DB end", e)
    return conn


conn_obj = get_connection_obj()

initial_data_table = 'GLOBAL_COMPETITOR_MASTER_INITIAL_SCRAPING_DATA'
json_files = []
directory_path = "C:/Users/NamitaJain/Downloads/Namita/blinds_shades_dumps/data/"
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        if filename.endswith('.json'):
            json_files.append(os.path.join(root, filename))
try:
    data_list = []
    for i, json_file in enumerate(json_files):
        print(i, json_file)
        with open(json_file) as f:
            scraped_data = json.load(f)
            if scraped_data:
                for data in scraped_data:
                    # data['COMP_UDA_ATTRIBUTE1'] = str(data['COMP_UDA_ATTRIBUTE1'])
                    data['COMP_UDA_ATTRIBUTE2'] = str(data['COMP_UDA_ATTRIBUTE2'])
                    data['COMP_UDA_ATTRIBUTE3'] = str(data['COMP_UDA_ATTRIBUTE3'])
                    data['COMP_UDA_ATTRIBUTE4'] = str(data['COMP_UDA_ATTRIBUTE4'])
                    data['COMP_ITEM_DESCRIPTION'] = str(data['COMP_ITEM_DESCRIPTION'])
                    data['COMP_REGULAR_PRICE'] = data['COMP_REGULAR_PRICE'].replace('$', '').replace(',', '') if data['COMP_REGULAR_PRICE'] is not None else None
                    data['COMP_PROMO_PRICE'] = data['COMP_PROMO_PRICE'].replace('$', '').replace(',', '') if data['COMP_PROMO_PRICE'] is not None else None
                    # data['COMP_UDA_ATTRIBUTE15'] = 'blossom_orcas_data'
                    # data['GLOBAL_COMPETITOR_ID'] = 123,
                    # data['JOB_ID']='BLINDSGALORE_BLINDS_BLINDS_19062024',
                    data['BATCH_ID'] ='BLINDS_SHADES'
                    data_list.append(data)
                print(len(data_list))
                df = pd.DataFrame(data_list)
                try:
                    success, nchunks, nrows, _ = write_pandas(conn_obj, df, initial_data_table)
                    print(f"Success: {success}, Number of chunks: {nchunks}, Number of rows: {nrows}")
                except Exception as g:
                    print(f"Error: {g}")
            data_list = []
except Exception as d:
    print(f"Error: {d}")