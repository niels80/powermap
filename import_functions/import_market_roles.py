###########################################################################################################
#    import_market_roles (Marktrollen.xml)
###########################################################################################################   

import pytz
import os
import datetime
from common import helperfunctions as helper
from lxml import etree
import sys


TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

###########################################################################################################

dict_market_roles = {

"MastrNummer" : "id_mastr_role",
"Marktrolle" : "market_role",
"DatumLetzteAktualisierung" : "ts_last_update",
"MarktakteurMastrNummer" : "id_mastr_party",
"BundesnetzagenturBetriebsnummer" : "bnetza_nr",
"BundesnetzagenturBetriebsnummer_nv" : "no_bnetza_nr",
"Marktpartneridentifikationsnummer" : "id_market_partner",
"Marktpartneridentifikationsnummer_nv" : "no_id_market_partner",
"KontaktdatenMarktrolle" : "contact_role"
}


def truncate_market_roles():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])

    sql_string = "TRUNCATE TABLE market_roles"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)

def import_market_roles(filename):
    
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    inserts = []
    for event, element in etree.iterparse(filename, tag="Marktrolle"):
        #print(etree.tostring(element))
        sqldata = {}
        nr_elements = 0
        for child in element:
            nr_elements = nr_elements+1
            if child.tag in dict_market_roles.keys():
                #print("Tag: "+child.tag)
                column = dict_market_roles[child.tag]
                value  = child.text
                if (value == 'true'):
                    value = 1
                if (value == 'false'):
                    value = 0
                sqldata[column] = value
            else:
                  print("Unknown column: "+child.tag)
                  exit(0)
        #("Elements: "+str(nr_elements)+"\n")
        if (nr_elements > 0):
            if (sqldata['id_mastr_role'] != None):
                #print("ID Mastr Role: "+sqldata['id_mastr_role'])
                placeholder = ", ".join(["?"] * len(sqldata))
                stmt = "insert into `{table}` ({columns}) values ({values});".format(table="market_roles",
                                                                                     columns=",".join(sqldata.keys()),
                                                                                     values=placeholder)
                sqlCursor.execute(stmt, list(sqldata.values()))

    sqlCursor.commit()
    sqlCursor.close()
    return("Import of market roles successfull!")

###########################################################################################################

