import h3
import pytz
import os
from common import helperfunctions as helper
import multiprocessing as mp
print("Number of processors: ", mp.cpu_count())

BATCHSIZE = 5000;
RESOLUTION = 7;

TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
sqlCursor = sqlConnection.cursor()

sqlConnection2 = helper.getSqlConnection(os.environ["POWERMAP_DB"])
sqlCursor2 = sqlConnection2.cursor()

nr = 0;
nrSQL = 0;

#print("Counting units....")
#sqlCursor.execute("SELECT COUNT(ID_MASTR_UNIT) FROM view_all_units")
#result = sqlCursor.fetchone();
#nrTotal = result[0];
#print("Number of units: ", nrTotal)

sqlCursor.execute('SELECT ID_MASTR_UNIT, TABLENAME, LAT, LON FROM view_all_units_location WHERE id_H3 is null ORDER BY TABLENAME, ID_MASTR_UNIT ')

akt_table = "";
while True:
    results = sqlCursor.fetchmany(BATCHSIZE)
    if not results:
        break

    data_update = []
    print("Processing row " + str(nr) + "-" + str(nr + BATCHSIZE))
    for row in results:
        nr += 1;
        nrSQL += 1;
        id_mastr = row[0]
        table    = row[1]
        lat      = row[2]
        lon      = row[3]

        if (akt_table == ""):
            akt_table = table

        if (lat is None or lon is None):
            print("No coordinates for "+id_mastr+" ("+table+")")
            continue


        id_H3 = h3.geo_to_h3(float(row[2]), float(row[3]), RESOLUTION)
        data_update.append([id_H3, id_mastr])

        if (table != akt_table and nrSQL > 0):
            sql = "UPDATE "+akt_table+" SET id_H3 = ? WHERE id_mastr_unit = ? "
            sqlCursor2.executemany(sql, data_update)
            sqlCursor2.commit()
            data_update = []
            akt_table = table
            nrSQL = 0

    if nrSQL > 0:
        sqlCursor2.executemany("UPDATE " + akt_table + " SET id_H3 = ? WHERE id_mastr_unit = ? ", data_update)
        sqlCursor2.commit()

print("Final")




