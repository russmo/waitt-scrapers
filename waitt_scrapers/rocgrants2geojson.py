import sys, re
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import geojson

sheet_id = '1YZLpy7dqR_JzpYgYf1hebg8AAOakwyQ71BB2ucfKaAM'
sheet_name = 'GIFTSOnlineData22012020123620 change to ROC-duration-portf - final-digits updated 1'
# sheet_url_csv = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
sheet_url_xlsx = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vQPiKyqlfWawurghy4pim31-Bw-lgqk-3xGC21SJwWSB9R53OpynQuy1pgUAaNA10CoPO5Jxa4NrEZG/pub?output=xlsx'


def rocgrants2geojson(outfile, xlsx_url=sheet_url_xlsx):
    # only one sheet name, so don't need to specificy sheet_name in read_excel()
    #df = pd.read_excel(sheet_url_xlsx, sheet_name=sheet_name, na_filter=False)
    df = pd.read_excel(sheet_url_xlsx, na_filter=False)

    # df.fillna('', inplace=True)

    features = []

    pointre = re.compile(r'address="(?P<lat>.*?),\s*(?P<lon>.*?)"\s*zoom="(?P<zoom>\d+)"')

    for index,row in df.iterrows():
        mapcode = str(row['Map shortcode'])
        pmatch = pointre.search(mapcode)
        point = None
        if pmatch:
            point = geojson.Point((float(pmatch.group('lon')), float(pmatch.group('lat'))))
        features.append(geojson.Feature(geometry=point, id=index, properties={
            "title": str(row['Headline']),
            "project_title": str(row['Project Title']),
            # Project Descriptions are too long, take up 500KB in the geojson file
            # "description": str(row['Project Description']),
            "organization": str(row['Organization']),
            "link": row['Link to']
        }))


    feature_collection = geojson.FeatureCollection(features)

    with open(outfile, 'w') as f:
       geojson.dump(feature_collection, f, indent=2)


if __name__ == '__main__':
    outfile = sys.argv[1]
    rocgrants2geojson(outfile)
