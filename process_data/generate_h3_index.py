import h3
import pytz
import os
from common import helperfunctions as helper
import multiprocessing as mp
print("Number of processors: ", mp.cpu_count())

BATCHSIZE = 100;
RESOLUTION = 9;

TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
sqlCursor = sqlConnection.cursor()

sqlConnection2 = helper.getSqlConnection(os.environ["POWERMAP_DB"])
sqlCursor2 = sqlConnection2.cursor()

nr = 0;

#print("Counting units....")
#sqlCursor.execute("SELECT COUNT(ID_MASTR_UNIT) FROM view_all_units")
#result = sqlCursor.fetchone();
#nrTotal = result[0];
#print("Number of units: ", nrTotal)

sqlCursor.execute('SELECT ID_MASTR_UNIT, TABLENAME, LAT, LON FROM view_all_units_location WHERE id_H3 IS NULL ')
while True:
    results = sqlCursor.fetchmany(BATCHSIZE)
    if not results:
        break

    data_update = []
    print("Processing row " + str(nr) + "-" + str(nr + BATCHSIZE))
    for row in results:
        nr += 1;

        id_mastr = row[0]
        table    = row[1]
        #print(str(row[2]) + "/" + str(row[3]) )
        id_H3    = h3.geo_to_h3(float(row[2]), float(row[3]), RESOLUTION )
        data_update.append([table,id_H3,id_mastr])

    sqlCursor2.executemany("UPDATE ? SET id_H3 = ? WHERE id_mastr_unit = ? ",data_update)
    sqlCursor2.commit()





