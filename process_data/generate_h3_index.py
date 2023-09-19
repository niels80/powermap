import h3
import pytz
import os
from common import helperfunctions as helper

BATCHSIZE = 5000
RESOLUTION = 7


######################################
def update_h3(tablename):

    TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    sqlConnection2 = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor2 = sqlConnection2.cursor()

    nr = 0;
    nrSQL = 0;

    print("Updating H3 Indizes for table "+str(tablename))
    sqlCursor.execute('''SELECT                                                       
            ID_MASTR_UNIT,                                                           
            COALESCE( 
                `units`.`LATITUDE`, 
                `zip_codes`.`lat` 
            ) AS `LAT`, 
            COALESCE( 
                `units`.`LONGITUDE`, 
                `zip_codes`.`lon` 
            ) AS `LON` 
        FROM ''' + str(tablename) + ''' `units`
        LEFT JOIN `zip_codes` ON `units`.`ZIPCODE` = `zip_codes`.`plz`
        WHERE id_H3 IS NULL 
        ORDER BY
            `units`.`ZIPCODE`   ''')
    nr = 0
    nrSQL = 0
    while True:

        results = sqlCursor.fetchmany(BATCHSIZE)
        if not results:
            break

        data_update = []
        print("Processing row " + str(nr) + "-" + str(nr + BATCHSIZE))
        for row in results:
            id_mastr = row[0]
            lat      = row[1]
            lon      = row[2]

            if (lat is None or lon is None):
                print("No coordinates for "+id_mastr+" ("+str(tablename)+")")
                continue

            nr += 1
            nrSQL += 1

            id_H3 = h3.latlng_to_cell(float(lat), float(lon), RESOLUTION)
            data_update.append([id_H3, id_mastr])

        if nrSQL > 0:
            sqlCursor2.executemany("UPDATE " + str(tablename) + " SET id_H3 = ? WHERE id_mastr_unit = ? ", data_update)
            sqlCursor2.commit()

    print("Final")
######################################

def generate_h3():
    update_h3('gas_units_consumer')
    update_h3('gas_units_generator')
    update_h3('gas_units_storage')
    update_h3('power_units_biomass')
    update_h3('power_units_consumer')
    update_h3('power_units_geo_soltherm_other')
    update_h3('power_units_hydro')
    update_h3('power_units_nuclear')
    update_h3('power_units_solar')
    update_h3('power_units_storage')
    update_h3('power_units_thermal')
    update_h3('power_units_wind')
    exit(0)

if __name__ == "__main__":
    generate_h3()