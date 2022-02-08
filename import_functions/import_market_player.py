###########################################################################################################
#    import_market_player (Marktakteure.xml)
###########################################################################################################

import pytz
import os
import datetime
from common import helperfunctions as helper
from lxml import etree
import sys


TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))

###########################################################################################################

dict_market_player = {

    "Id" : "id",
    "MastrNummer" : "id_mastr",
    "DatumLetzeAktualisierung" : "ts_last_update",    # Jep, the typo is in the official document ... letze vs. letzte
    "Personenart" : "id_persona",
    "MarktakteurAnrede" : "id_salutation",
    "MarktakteurTitel" : "id_title",
    "MarktakteurVorname" : "first_name",
    "MarktakteurNachname" : "last_name",
    "Firmenname" : "company_name",
    "Marktfunktion" : "id_role",
    "Rechtsform" : "id_legal_form",
    "SonstigeRechtsform" : "id_other_form",
    "Marktrollen" : "id_market_roles",
    "Marktakteursvertreter" : "representative",
    "Land" : "id_country",
    "Region" : "region",
    "Strasse" : "street",
    "Hausnummer" : "street_nr",
    "Hausnummer_nv" : "no_street",
    "Adresszusatz" : "address_extra",
    "Postleitzahl" : "zipcode",
    "Ort" : "city",
    "Bundesland" : "id_state",
    "Netz" : "id_grid_operator",
    "Nuts2" : "nuts2",
    "Email" : "email",
    "Telefon" : "phone",
    "Fax" : "fax",
    "Fax_nv" : "no_fax",
    "Webseite" : "website",
    "Webseite_nv" : "no_website",
    "Registergericht" : "id_court",
    "Registergericht_nv" : "no_court",
    "RegistergerichtAusland" : "foreign_court",
    "RegistergerichtAusland_nv" : "no_foreign_court",
    "Registernummer" : "registration_nr",
    "Registernummer_nv" : "no_registration_nr",
    "RegisternummerAusland" : "foreign_registration_nr",
    "RegisternummerAusland_nv" : "no_foreign_registration_nr",
    "Taetigkeitsbeginn" : "date_start_operation",
    "AcerCode" : "acer_code",
    "AcerCode_nv" : "no_acer_code",
    "Umsatzsteueridentifikationsnummer" : "sales_tax_id",
    "Umsatzsteueridentifikationsnummer_nv" : "no_sales_tax_id",
    "Taetigkeitsende" : "date_end_operation",
    "Taetigkeitsende_nv" : "no_date_end_operation",
    "BundesnetzagenturBetriebsnummer" : "bundesnetzagentur_id",
    "BundesnetzagenturBetriebsnummer_nv" : "no_bundesnetzagentur_id",
    "LandAnZustelladresse" : "id_postal_country",
    "PostleitzahlAnZustelladresse" : "postal_zip",
    "OrtAnZustelladresse" : "postal_city",
    "StrasseAnZustelladresse" : "postal_street",
    "HausnummerAnZustelladresse" : "postal_nr",
    "HausnummerAnZustelladresse_nv" : "postal_no_nr",
    "AdresszusatzAnZustelladresse" : "postal_extra_info",
    "Kmu" : "small_company_kmu",
    "TelefonnummerVMav" : "phone_vmav",
    "EmailVMav" : "email_vmav",
    "RegistrierungsdatumMarktakteur" : "date_registration",
    "HauptwirtdschaftszweigAbteilung" : "id_industry_dept",
    "HauptwirtdschaftszweigGruppe" : "id_industry_group",
    "HauptwirtdschaftszweigAbschnitt" : "id_industry_section",
    "Direktvermarktungsunternehmen" : "is_direct_marketer",
    "BelieferungVonLetztverbrauchernStrom" : "is_electricity_supplier_customer",
    "BelieferungHaushaltskundenStrom" : "is_electricity_supplier_households",
    "Gasgrosshaendler" : "is_gas_trader",
    "Stromgrosshaendler" : "is_electricity_trader",
    "BelieferungVonLetztverbrauchernGas" : "is_gas_supplier",
    "BelieferungHaushaltskundenGas" : "is_gas_supplier_households"

}


def truncate_market_player():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])

    sql_string = "TRUNCATE TABLE market_player"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)

def import_market_player(filename):
    
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    inserts = []
    for event, element in etree.iterparse(filename, tag="Marktakteur"):

        sqldata = {}
        nr_elements = 0
        for child in element:
            nr_elements = nr_elements+1
            if child.tag in dict_market_player.keys():
                #print("Tag: "+child.tag+"\n")
                column = dict_market_player[child.tag]
                value  = child.text
                if (value == 'true'):
                    value = 1
                if (value == 'false'):
                    value = 0
                sqldata[column] = value
            else:
                  print("Unknown column: "+child.tag)
                  exit(0)
        #print("Elements: "+str(nr_elements)+"\n")
        if (sqldata['id_mastr'] != None):
            placeholder = ", ".join(["?"] * len(sqldata))
            stmt = "insert into `{table}` ({columns}) values ({values});".format(table="market_player",
                                                                                 columns=",".join(sqldata.keys()),
                                                                                 values=placeholder)
            sqlCursor.execute(stmt, list(sqldata.values()))

    sqlCursor.commit()
    sqlCursor.close()
    return("Import of market actors successfull!")

###########################################################################################################

