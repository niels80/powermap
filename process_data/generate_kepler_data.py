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

clear_names = {
    "gas_units_consumer" : "Gas units consumer",
    "gas_units_generator" : "Gas units generation",
    "gas_units_storage" : "Gas units storage",
    "power_units_biomass" : "Biomass",
    "power_units_consumer" : "Power consumers",
    "power_units_geo_soltherm_other" : "Geothermal and others",
    "power_units_hydro" : "Hydro power",
    "power_units_nuclear" : "Nuclear",
    "power_units_solar" : "Photovoltaics",
    "power_units_storage" : "Power storage",
    "power_units_thermal" : "Thermal power unit",
    "power_units_wind"   : "Wind turbines"
}

def generate_kepler_data():

    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    sqlConnection2 = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor2 = sqlConnection2.cursor()

    # Total statistics
    with open(OUTPATH+"/statistics_total_yearly.csv", 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        header = [ 'Year Commissioning', 'Unit Type', 'Number of Installations', 'Sum [MW]', 'Minimum [kW]', '10% Percentile [kW]', 'Median [kW]', 'Average [kW]', '90% Percentile [kW]', 'Maximum [kW]']
        writer.writerow(header)
        all_data = {}
        for dt in data_tables:

            print("Processing Statistics for " + dt)
            colname = data_tables[dt][0]
            sqlstr = "SELECT t1.year year,number,sum,minimum,p10,median,average,p90,maximum FROM  \
                        (SELECT DISTINCT year(date_commissioning) year, \
                           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "+colname+") OVER (PARTITION BY year(date_commissioning)) AS median, \
                           PERCENTILE_CONT(0.1) WITHIN GROUP (ORDER BY "+colname+") OVER (PARTITION BY year(date_commissioning)) AS p10, \
                           PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY "+colname+") OVER (PARTITION BY year(date_commissioning)) AS p90 \
                           FROM "+dt+" ) t1 \
                        LEFT JOIN \
                          ( \
                              SELECT year(date_commissioning) year,  \
                                     MIN("+colname+") minimum,  \
                                     MAX("+colname+") maximum,  \
                                     AVG("+colname+") average,  \
                                     COUNT("+colname+") number, \
                                     SUM("+colname+")/1000 sum FROM "+dt+" GROUP BY year \
                              ) t2 \
                          ON (t1.year=t2.year) \
                          WHERE t1.year>=1990 \
                          ORDER BY t1.year "

            sqlCursor.execute(sqlstr)
            results = sqlCursor.fetchall()
            sqlCursor.commit()

            for r in results:
                if (r.year not in all_data):
                    all_data[r.year] = {}
                if (dt not in all_data[r.year]):
                    all_data[r.year][dt] = {}

                if (r.sum is not None):
                    all_data[r.year][dt]["P"]  = r.sum
                    all_data[r.year][dt]["nr"] = r.number
                    all_data[r.year][dt]["median"] = r.median
                    all_data[r.year][dt]["average"]  = r.average
                    all_data[r.year][dt]["minimum"]  = r.minimum
                    all_data[r.year][dt]["maximum"] = r.maximum
                    all_data[r.year][dt]["p10"] = r.p10
                    all_data[r.year][dt]["p90"] = r.p90

                    writer.writerow(
                        [str(r.year), clear_names[dt],  r.number, r.sum, r.minimum, r.p10, r.median, r.average, r.p90, r.maximum])

    with open(OUTPATH + "/statistics_total_yearly.json", 'w', newline='', encoding='UTF8') as outfile:
        outfile.write(json.dumps(all_data, use_decimal=True, default=str, ensure_ascii=False))
        outfile.close()





    # Statistics per Hexagon

    all_data = {}
    for dt in data_tables:
        print("Processing H3 localized statistics "+dt)
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

    with open(OUTPATH + "/statistics_h3_yearly.json", 'w', newline='', encoding='UTF8') as outfile:
            outfile.write(json.dumps(all_data, use_decimal=True, default=str, ensure_ascii=False))
            outfile.close()

if __name__ == "__main__":
    generate_kepler_data()
