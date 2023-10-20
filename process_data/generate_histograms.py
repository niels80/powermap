import csv

import pytz
import os
import io
import h3
from shapely.geometry import Polygon, Point
import shapely.wkt
import simplejson as json
from common import helperfunctions as helper
import collections

from pathlib import Path

OUTPATH = str(os.environ["OUTPATH"])
TARGET_RESOLUTION = 6

TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

def generate_solar_histogram():

    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    with io.open(OUTPATH + "/histogram_solar.json", 'w', encoding='utf8') as outfile:
        all_data = {}
        print("Create Histogram Solar")
        sqlstr = """SELECT  year(date_commissioning) year, 
                            round(power_netto) AS power, 
                            sum(power_netto)/1000 sum_MW, 
                            count(power_netto) nr 
                    FROM `power_units_solar` 
                    GROUP BY year,power 
                    ORDER BY year,power
        """

        sqlCursor.execute(sqlstr)
        results = sqlCursor.fetchall()
        sqlCursor.commit()

        row_headers = [x[0] for x in sqlCursor.description]  # this will extract row headers
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))
        outfile.write(json.dumps(json_data, use_decimal=True, ensure_ascii=False))

def generate_storage_histogram():

    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    print("Create Histogram Storage")
    sqlstr = """SELECT  year(date_commissioning) year, 
                        round(power_netto) AS power, 
                        sum(power_netto)/1000 sum_MW, 
                        count(power_netto) nr 
                FROM `power_units_storage` 
                GROUP BY year,power 
                ORDER BY year,power
    """
    #
    with io.open(OUTPATH + "/histogram_storage.json", 'w', encoding='utf8') as outfile:

        sqlCursor.execute(sqlstr)
        results = sqlCursor.fetchall()
        sqlCursor.commit()

        row_headers = [x[0] for x in sqlCursor.description]  # this will extract row headers
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))
        outfile.write(json.dumps(json_data, use_decimal=True, ensure_ascii=False))


def generate_histograms():
    generate_solar_histogram()
    generate_storage_histogram()


if __name__ == "__main__":
    generate_histograms()
