import pytz
import os
import io
import simplejson as json
from common import helperfunctions as helper
from pathlib import Path

OUTPATH = str(os.environ["OUTPATH"])
NR_FOLDERS = 50

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



#
#  Statistics per Hexagon
#

dict_global_statistics = {}
for t in data_tables:
    dict_table_statistics = {}
    print("Processing "+str(t))
    sqlstr = "SELECT id_H3, COUNT(id_H3) nr, "
    n = 0
    for col in data_tables[t]:
        if (n > 0):
            sqlstr += ","
        else:
            n += 1
        sqlstr += str("SUM("+col+") "+col)
    sqlstr += " FROM "+t+" GROUP BY id_H3 ORDER BY id_H3 "
    sqlCursor.execute(sqlstr)
    results = sqlCursor.fetchall()
    sqlCursor.commit()
    colnames = [column[0] for column in sqlCursor.description]
    for r in results:
        if r.id_H3 not in dict_global_statistics:
            dict_global_statistics[r.id_H3] = {}
        dict_global_statistics[r.id_H3][t] = dict(zip(colnames,r))
        dict_table_statistics[r.id_H3] = dict(zip(colnames, r))
    dat2 = []
    # Write table statistics
    for d in dict_table_statistics:
        dat2.append({"id_H3": d} | dict_table_statistics[d])
    with io.open(OUTPATH + "/statistics_t_"+t+".json", 'w',encoding='utf8') as outfile:
        outfile.write(json.dumps(dat2, use_decimal=True, ensure_ascii=False))

#Write total statistics
# Hash : {idH3 : {Data}, idH3 : {Data}, .... }
with io.open(OUTPATH+"/statistics.json", 'w',encoding='utf8') as outfile:
    outfile.write(json.dumps(dict_global_statistics, use_decimal=True, ensure_ascii=False))

# Array: [ {idH3 : xxxx, .... }, { }, ....  ]
dat2 = []
for d in dict_global_statistics:
    dat2.append({ "id_H3" : d } | dict_global_statistics[d])
with io.open(OUTPATH+"/statistics2.json", 'w',encoding='utf8') as outfile:
    outfile.write(json.dumps(dat2, use_decimal=True, ensure_ascii=False))


#
#  All data per H3 hexagon
#
sql_all_id3 = ""
n = 0
for t in data_tables:
    if (n>0):
        sql_all_id3 += " UNION "
    n += 1
    sql_all_id3 += " (SELECT DISTINCT id_H3 FROM "+t+")"


# Count all H3 indizes
sqlstr = "SELECT COUNT(DISTINCT id_H3) nr_total FROM ("+sql_all_id3+") AS all_H3s "
sqlCursor.execute(sqlstr)
results = sqlCursor.fetchall()
for r in results:
    n_total = r.nr_total

# Get all H3 indizes
sqlstr = "SELECT id_H3 FROM ("+sql_all_id3+") AS all_H3s GROUP BY id_H3 ORDER BY id_H3"
sqlCursor.execute(sqlstr)
results = sqlCursor.fetchall()



# Write all data per H3 hexagon
n2 = 0
for r in results:
    n2 += 1
    if (r.id_H3 is None):
        continue
    idH3 = r.id_H3
    print("H3: "+str(idH3)+" "+str(round(n2/n_total*100,2))+"%  "+str(n2)+"/"+str(n_total)+" ")
    h3data = { "id_H3" : idH3,
               "units" : {}
    }
    for t in data_tables:
        h3data["units"][t] = {}
        sqlstr2 = "SELECT * FROM "+t+" WHERE id_H3='"+idH3+"'"
        sqlCursor2.execute(sqlstr2)
        results2 = sqlCursor2.fetchall()
        colnames = [column[0] for column in sqlCursor2.description]
        for row in results2:
            dat = dict(zip(colnames,row))
            h3data["units"][t][dat["id_mastr_unit"]] = dat

    folder = OUTPATH + "/" + str(int(idH3, 16) % NR_FOLDERS)
    Path(folder).mkdir(parents=True, exist_ok=True)
    with io.open(folder+"/h3_"+idH3+".json", 'w',encoding='utf8') as outfile:
        outfile.write(json.dumps(h3data, use_decimal=True, default=str, ensure_ascii=False))
    outfile.close()