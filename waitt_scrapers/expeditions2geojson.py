import sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import re

import geojson

sheet_name = 'WI Project Sites'
sheet_id = '10j1tAtZxIa4b_L-UsKJ_IM_sLMxhAcdY'
sheet_name = 'Webmap'
# sheet_url_csv = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
sheet_url_xlsx = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vSSynaci-pqj5Z0loo0YRLGw0vN5m_bZKtq4k18kn2vTFqdyMaZdljn54eyOLcsCQ/pub?output=xlsx'

def expeditions2geojson(outfile_point, outfile_line, xlsx_url=sheet_url_xlsx):
    df = pd.read_excel(sheet_url_xlsx, sheet_name=sheet_name, na_filter=False)

    features_point = []
    features_line = []

    def dms2dec(dms_str):
        """Return decimal representation of DMS
        
        >>> dms2dec(utf8(48°53'10.18"N))
        48.8866111111F
        
        >>> dms2dec(utf8(2°20'35.09"E))
        2.34330555556F
        
        >>> dms2dec(utf8(48°53'10.18"S))
        -48.8866111111F
        
        >>> dms2dec(utf8(2°20'35.09"W))
        -2.34330555556F
        
        """
        
        dms_str = re.sub(r'\s', '', dms_str)
        
        sign = -1 if re.search('[swSW]', dms_str) else 1
        
        numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

        degree = numbers[0]
        minute = numbers[1] if len(numbers) >= 2 else '0'
        second = numbers[2] if len(numbers) >= 3 else '0'
        frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
        
        second += "." + frac_seconds
        return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)

    point_fields = [(f'Lon{i}', f'Lat{i}') for i in range(0,20)]

    for index,row in df.iterrows():
        point = None
        track = None
        coords = []
        for (lon, lat) in point_fields:
            try:
                coords.append( (dms2dec(str(row[lon])), dms2dec(str(row[lat]))) )
            except:
                pass
        print('index:', index, '->', len(coords), 'points in track')
        if coords:
            point = geojson.Point(coords[0])
        if len(coords) > 1:
            track = geojson.LineString(coords)
        properties = {
            "visible": str(row['Visible']),
            "location": str(row['Expedition Location']),
            "description": str(row['Description']),
            "dates": str(row['Dates']),
            "link": str(row['Link']),
            "image_url": str(row['Image URL']),
            "type": str(row['Type']),
            "partners": str(row['Key Partners/Contact']),
            "equipment": str(row['Equipment']),
            "track": coords
        }
        features_point.append(geojson.Feature(geometry=point, id=index, properties=properties))
        features_line.append(geojson.Feature(geometry=track, id=index, properties=properties))
        

    feature_collection_point = geojson.FeatureCollection(features_point)
    feature_collection_line = geojson.FeatureCollection(features_line)

    print(outfile_point)
    with open(outfile_point, 'w') as f:
       geojson.dump(feature_collection_point, f, indent=2)

    print(outfile_line)
    with open(outfile_line, 'w') as f:
       geojson.dump(feature_collection_line, f, indent=2)


if __name__ == '__main__':
   outfile_point = sys.argv[1]
   outfile_line = sys.argv[2]
   expeditions2geojson(outfile_point, outfile_line)

