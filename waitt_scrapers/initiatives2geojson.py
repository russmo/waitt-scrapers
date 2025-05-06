import sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import geojson

sheet_name = "WI Project Sites"
sheet_id = "1UP7FFm9LUpDV2YWMHNglGR_wKV2Jo1VkTUT4FUgVa6I"
sheet_name = "WI Project Sites"
# sheet_url_csv = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
sheet_url_xlsx = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vSIi0bUwNN9xDPGxi7qWZMjxHR-rgyIV8olQWqH7Yc8DLXiGtFgFl4WfoqL_5crumCNQGOpgL_N2h3k/pub?output=xlsx"


def toFloat(f):
    output = None
    try:
        output = float(f)
    except ValueError:
        pass
    return output


def makeOffset(x, y):
    output = None
    try:
        output = [float(x), float(y)]
    except ValueError:
        pass
    return output


def initiatives2geojson(outfile, xlsx_url=sheet_url_xlsx):
    df = pd.read_excel(sheet_url_xlsx, sheet_name=sheet_name, na_filter=False)

    features = []

    for index, row in df.iterrows():
        point = None
        try:
            point = geojson.Point((row["Longitude"], row["Latitude"]))
        except:
            pass
        features.append(
            geojson.Feature(
                geometry=point,
                id=index,
                properties={
                    "title": str(row["Title"]),
                    "description": str(row["Project Description"]),
                    "iso3": str(row["EEZ_ISO3"]),
                    "link": str(row["Link"]),
                    "image_url": str(row["Hero Image URL"]),
                    "legacy": (
                        str(row["Legacy"])
                        if "Legacy" in row.index  # alternative df.columns
                        else str(row["Pilot"])
                    ),
                    "label_anchor": str(row["Label Anchor"]),
                    "label_x_offset": toFloat(row["Label X Offset"]),
                    "label_y_offset": toFloat(row["Label Y Offset"]),
                    "label_offset": makeOffset(
                        row["Label X Offset"], row["Label Y Offset"]
                    ),
                },
            )
        )

    feature_collection = geojson.FeatureCollection(features)

    print(outfile)

    with open(outfile, "w") as f:
        geojson.dump(feature_collection, f, indent=2)


if __name__ == "__main__":
    outfile = sys.argv[1]
    initiatives2geojson(outfile)
