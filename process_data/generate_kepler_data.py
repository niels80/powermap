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

sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
sqlCursor = sqlConnection.cursor()

sqlConnection2 = helper.getSqlConnection(os.environ["POWERMAP_DB"])
sqlCursor2 = sqlConnection2.cursor()

data_tables = {
    "gas_units_consumer" : ["max_withdrawal_power","is_power_generator"],
    "gas_units_generator" : ["max_inject_power"],
    "gas_units_storage" : ["max_inject_power", "max_withdrawal_power", "working_gas_max"],
    "power_units_biomass" : ["power_netto"],
    "power_units_consumer" : ["controllable_load "],
    "power_units_geo_soltherm_other" : ["power_netto"],
    "power_units_hydro" : ["power_netto"],
    "power_units_nuclear" : ["power_netto"],
    "power_units_solar" : ["power_netto"],
    "power_units_storage" : ["power_netto"],
    "power_units_thermal" : ["power_netto"],
    "power_units_wind"   : ["power_netto"]
}

all_data = {}
for dt in data_tables:
    print("Processing "+dt)
    colname = data_tables[dt][0]
    sqlstr  = "SELECT id_H3, YEAR(date_commissioning) year, COUNT(id_H3) nr, SUM("+colname+") power_netto FROM "+dt+" WHERE id_H3 IS NOT NULL GROUP BY year, id_H3"
    sqlCursor.execute(sqlstr)
    results = sqlCursor.fetchall()
    sqlCursor.commit()

    header = ['hex_id', 'year_commisssioning', 'unit_type', 'nr_installations', 'P_installed']

    for r in results:
       id_H3 = h3.cell_to_parent(r.id_H3, TARGET_RESOLUTION)
       if (id_H3 not in all_data):
            all_data[id_H3] = {}
       if (r.year not in all_data[id_H3]):
            all_data[id_H3][r.year]={}
       if (dt not in all_data[id_H3][r.year]):
                all_data[id_H3][r.year][dt] = {}
                all_data[id_H3][r.year][dt]["nr"] = 0
                all_data[id_H3][r.year][dt]["P"] = 0

       if (r.power_netto is not None):
           all_data[id_H3][r.year][dt]["P"] += r.power_netto
           all_data[id_H3][r.year][dt]["nr"] += r.nr

with open(OUTPATH+"/kepler_data.csv", 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for id_H3 in all_data:
        for year_c in all_data[id_H3]:
            for unit_type in all_data[id_H3][year_c]:
                if(year_c != None):
                    writer.writerow([id_H3,str(year_c)+"-06-01 00:00",unit_type,all_data[id_H3][year_c][unit_type]['nr'],all_data[id_H3][year_c][unit_type]['P']])

with open(OUTPATH + "/statistics_yearly.json", 'w', newline='', encoding='UTF8') as outfile:
        outfile.write(json.dumps(all_data, use_decimal=True, default=str, ensure_ascii=False))
        outfile.close()


