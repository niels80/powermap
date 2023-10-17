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

    # Total statistics
    with open(OUTPATH+"/histogram_solar.csv", 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        header = [ 'Year_Comissioning','PowerSolar_kW', 'Sum_MW', 'Number']
        writer.writerow(header)
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

        for r in results:
            writer.writerow(
                    [str(r.year), r.power,  r.sum_MW, r.nr])

if __name__ == "__main__":
    generate_solar_histogram()
