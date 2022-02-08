import pyodbc
import logging
import os
import time
import datetime



###########################################################################################################
#  Helper functions
###########################################################################################################   

def getSqlConnection(sqlConnectionString):
    i = 1
    while i < 4:
        logging.info('contacting DB, try Nr. '+str(i))
        try:
            sqlConnection = pyodbc.connect(sqlConnectionString)
        except pyodbc.Error as err:
            logging.warning(err)
            time.sleep(10) # wait 10s before retry
            i+=1
        else:
            return sqlConnection


# ToDo: Correct error handling
def error(message):
    logging.info("Error! "+str(message))
    raise Exception('Error', message)

