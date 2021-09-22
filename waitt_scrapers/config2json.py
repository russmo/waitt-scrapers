import sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import json

sheet_name = 'WI Project Sites'
sheet_id = '1UP7FFm9LUpDV2YWMHNglGR_wKV2Jo1VkTUT4FUgVa6I'
sheet_name = 'Web Map Config'
# sheet_url_csv = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
sheet_url_xlsx = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vSIi0bUwNN9xDPGxi7qWZMjxHR-rgyIV8olQWqH7Yc8DLXiGtFgFl4WfoqL_5crumCNQGOpgL_N2h3k/pub?output=xlsx'

def config2json(outfile, xlsx_url=sheet_url_xlsx):
    df = pd.read_excel(sheet_url_xlsx, sheet_name=sheet_name, na_filter=False)

    config = {}

    for index,row in df.iterrows():
        config["default_category"] = str(row['Default Category'])
        config["default_headline"] = str(row['Default Headline'])
        config["default_content"] = str(row['Default Content'])
        config["default_img"] = str(row['Default Image'])
        config["default_url"] = str(row['Default Url'])

    print(outfile)

    with open(outfile, 'w') as f:
       json.dump(config, f, indent=2)

if __name__ == '__main__':
    outfile = sys.argv[1]
    config2json(outfile)
