###########################################################################################################
#    import_categories  Import "Katalogkategorien.xml" (catalog categories)
#    import_catalog     Import "Katalogwerte.xml" (catalog values)
#    import_balancing_areas  Import "Bilanzierungsgebiete.xml" (balancing areas)
###########################################################################################################   

import pytz
import os
import datetime
from common import helperfunctions as helper
from lxml import etree
import sys


TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

###########################################################################################################

def import_categories(filename):
    
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])

    sql_string = "TRUNCATE TABLE catalog_categories"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)

    inserts = []
    for event, element in etree.iterparse(filename, tag="Katalogkategorie"):
        id = None
        name = None
        for child in element:
            if (child.tag=="Id"):
                id = child.text
            if (child.tag=="Name"):
                name = child.text
        if (id != None):
            sqlCursor.execute("INSERT INTO catalog_categories(id,name_DE) VALUES (?,?)",id,name)


    sqlCursor.commit()
    sqlCursor.close()
    return("Import of catalog categories successfull!")

###########################################################################################################


def import_catalog(filename):
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])

    sql_string = "TRUNCATE TABLE catalog"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)

    inserts = []
    for event, element in etree.iterparse(filename, tag="Katalogwert"):

        id = None
        category_id = None
        name = None
        for child in element:
            if (child.tag == "Id"):
                id = child.text
            if (child.tag == "KatalogKategorieId"):
                category_id = child.text
            if (child.tag == "Wert"):
                name = child.text
        if (id != None):
            if (name == None):
                name="-"
            sqlCursor.execute("INSERT INTO catalog(id,category_id,name_DE) VALUES (?,?,?)", id, category_id, name)

    sqlCursor.commit()
    sqlCursor.close()
    return ("Import of catalog values successfull!")


###########################################################################################################


def import_balancing_areas(filename):
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])

    sql_string = "TRUNCATE TABLE balancing_areas"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)

    inserts = []
    for event, element in etree.iterparse(filename, tag="Bilanzierungsgebiet"):
        id = None
        category_id = None
        name = None
        yeic = None
        balancing_area_grid_connection_point = None
        control_area_grid_connection_point = None
        for child in element:
            if (child.tag == "Id"):
                id = child.text
            if (child.tag == "Yeic"):
                yeic = child.text
            if (child.tag == "BilanzierungsgebietNetzanschlusspunkt"):
                balancing_area_grid_connection_point = child.text
            if (child.tag == "RegelzoneNetzanschlusspunkt"):
                control_area_grid_connection_point = child.text
        if (id != None):
            sqlCursor.execute("INSERT INTO balancing_areas(id,yeic,balancing_area_grid_connection_point,control_area_id) VALUES (?,?,?,?)", id, yeic, balancing_area_grid_connection_point,control_area_grid_connection_point)

    sqlCursor.commit()
    sqlCursor.close()
    return ("Import of catalog values successfull!")