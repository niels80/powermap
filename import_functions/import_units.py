###########################################################################################################
#    import_units -> Import units
###########################################################################################################   

import pytz
import os
import datetime
from common import helperfunctions as helper
from lxml import etree
import sys


TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))
dict_all_units = {

    "EinheitMastrNummer" : "id_mastr_unit",
    "DatumLetzteAktualisierung" : "ts_last_update",
    "LokationMaStRNummer" : "id_mastr_market_location",
    "NetzbetreiberpruefungStatus" : "id_control_status",
    "NetzbetreiberpruefungDatum" : "ts_last_control",
    "AnlagenbetreiberMastrNummer" : "id_mastr_operator",
    "Land" : "id_country",
    "Bundesland" : "id_state",
    "Landkreis" : "region",
    "Gemeinde" : "municipality",
    "Gemeindeschluessel" : "id_municipality",
    "Postleitzahl" : "zipcode",
    "Gemarkung" : "communal_district",
    "FlurFlurstuecknummern" : "id_land_parcel",
    "Strasse" : "street",
    "StrasseNichtGefunden" : "no_street",
    "Hausnummer" : "street_nr",
    "Hausnummer_nv" : "no_street_nr",
    "HausnummerNichtGefunden" : "street_not_found",
    "Adresszusatz" : "address_extra",
    "Ort" : "city",
    "Laengengrad" : "longitude",
    "Breitengrad" : "latitude",
    "Registrierungsdatum" : "date_register",
    "GeplantesInbetriebnahmedatum" : "date_commissioning_planned",
    "Inbetriebnahmedatum" : "date_commissioning",
    "DatumEndgueltigeStilllegung" : "date_final_decommissioning",
    "DatumBeginnVoruebergehendeStilllegung" : "date_temp_decommissioning",
    "DatumWiederaufnahmeBetrieb" : "date_restart_operation",
    "EinheitSystemstatus" : "id_status_system",
    "EinheitBetriebsstatus" : "id_status_operation",
    "BestandsanlageMastrNummer" : "id_mastr_legacy",
    "NichtVorhandenInMigriertenEinheiten" : "not_in_migrated_units",
    "AltAnlagenbetreiberMastrNummer" : "id_mastr_last_operator",
    "DatumDesBetreiberwechsels" : "date_operator_change",
    "DatumRegistrierungDesBetreiberwechsels" : "date_operator_change_register",
    "NameStromerzeugungseinheit" : "name",
    "Weic" : "weic",
    "Weic_nv" : "no_weic",
    "WeicDisplayName" : "weic_display_name",
    "Kraftwerksnummer" : "id_bnetza_nr",
    "Kraftwerksnummer_nv" : "no_bnetza_nr",
    "Energietraeger" : "id_primary_energy",
    "Bruttoleistung" : "power_brutto",
    "Nettonennleistung" : "power_netto",
    "AnschlussAnHoechstOderHochSpannung" : "is_connected_high_voltage",
    "Schwarzstartfaehigkeit" : "is_blackstart_ready",
    "Inselbetriebsfaehigkeit" : "is_island_operation_ready",
    "Einsatzverantwortlicher" : "id_market_partner",
    "FernsteuerbarkeitNb" : "remote_control_grid_operator",
    "FernsteuerbarkeitDv" : "remote_control_direct_marketer",
    "FernsteuerbarkeitDr" : "remote_control_third_party",
    "Einspeisungsart" : "id_infeed_type",
    "PraequalifiziertFuerRegelenergie" : "prequalified_balancing",
    "GenMastrNummer" : "id_mastr_approval",
    "NameKraftwerk" : "name_power_plant",
    "NameKraftwerksblock" : "name_power_unit",
    "Technologie" : "id_technology"
}

dict_solar = {
    "ZugeordneteWirkleistungWechselrichter" : "power_converter"	,
    "GemeinsamerWechselrichterMitSpeicher" : "id_converter_storage",
    "AnzahlModule" : "nr_modules" ,
    "Lage" : "id_location_type",
    "Leistungsbegrenzung" : "id_power_curtailment",
    "EinheitlicheAusrichtungUndNeigungswinkel" : "has_common_angle",
    "Hauptausrichtung" : "id_main_direction",
    "HauptausrichtungNeigungswinkel" : "id_main_angle",
    "Nebenausrichtung" : "id_secondary_direction",
    "NebenausrichtungNeigungswinkel" : "id_secondary_angle",
    "InAnspruchGenommeneFlaeche" : "area_used",
    "ArtDerFlaecheIds" : "id_area_type",
    "InAnspruchGenommeneAckerflaeche" : "area_used_agriculture",
    "Nutzungsbereich" : "id_usage_of_location",
    "EegMaStRNummer" : "id_mastr_eeg"
}

dict_thermal = {
    "DatumBaubeginn" : "date_construction_start",
    "AnzeigeEinerStilllegung" :  "has_reported_operation_end",
    "ArtDerStilllegung" : "id_operation_end",
    "DatumBeginnVorlaeufigenOderEndgueltigenStilllegung" : "date_end_operation",
    "SteigerungNettonennleistungKombibetrieb" : "power_added_combi_operation",
    "AnlageIstImKombibetrieb" : "is_in_combi_operation",
    "MastrNummernKombibetrieb" : "id_mastr_combi_operation",
    "NetzreserveAbDatum" : "date_grid_reserve_start",
    "SicherheitsbereitschaftAbDatum" : "date_emergency_reserve_start",
    "Hauptbrennstoff" : "id_primary_energy",
    "WeitererHauptbrennstoff" : "id_other_primary_energy",
    "WeitereBrennstoffe" : "id_other_fuels",
    "BestandteilGrenzkraftwerk" : "is_border_power_plant",
    "NettonennleistungDeutschland" : "power_netto_max_germany",
    "AnteiligNutzungsberechtigte" : "contracted_consumers",
    "Notstromaggregat" : "is_backup_power",
    "Einsatzort" : "id_location_backup_power",
    "KwkMaStRNummer" : "id_mastr_kwk"
}

dict_wind = {
      "NameWindpark" : "name_windpark" ,
    "Lage" : "id_location_type" ,
    "Seelage" :  "id_location_sea" ,
    "ClusterOstsee" : "id_cluster_sea" ,
    "ClusterNordsee" : "id_cluster_sea" ,
    "Hersteller" :   "id_manufacturer",
    "Technologie" :  "id_technology" ,
    "Typenbezeichnung" :  "name_type" ,
    "Nabenhoehe" :  "hub_height" ,
    "Rotordurchmesser" :  "rotor_diameter" ,
    "Rotorblattenteisungssystem" :  "has_deicing_system" ,
    "AuflageAbschaltungLeistungsbegrenzung" :  "has_restrictions" ,
    "AuflagenAbschaltungSchallimmissionsschutzNachts" :  "has_restrictions_sound_night" ,
    "AuflagenAbschaltungSchallimmissionsschutzTagsueber" :  "has_restrictions_sound_day" ,
    "AuflagenAbschaltungSchattenwurf" :  "has_restrictions_shadow" ,
    "AuflagenAbschaltungTierschutz" :  "has_restrictions_animals" ,
    "AuflagenAbschaltungEiswurf" :  "has_restrictions_falling_ice",
    "AuflagenAbschaltungSonstige" :  "has_restrictions_other",
    "Wassertiefe" :  "water_depth" ,
    "Kuestenentfernung" :  "distance_to_shore" ,
    "EegMaStRNummer" : "id_mastr_eeg"
}


###########################################################################################################
#  Nuclear units
###########################################################################################################
def truncate_units_nuclear():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])

    sql_string = "TRUNCATE TABLE power_units_nuclear"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)

def import_units_nuclear(filename):
    dict_units = dict_all_units
    return import_units(filename, "EinheitKernkraft", "power_units_nuclear", dict_units)


###########################################################################################################
#  Solar units
###########################################################################################################
def truncate_units_solar():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_solar"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_solar(filename):
    dict_units = dict_all_units | dict_solar  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitSolar","power_units_solar",dict_units)


###########################################################################################################
#  Wind units
###########################################################################################################
def truncate_units_wind():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_wind"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_wind(filename):
    dict_units = dict_all_units | dict_wind  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitWind","power_units_wind",dict_units)

###########################################################################################################
#  Thermal units
###########################################################################################################
def truncate_units_thermal():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_thermal"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_thermal(filename):
    dict_units = dict_all_units | dict_thermal  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitVerbrennung","power_units_thermal",dict_units)


###########################################################################################################
#  Generic import
###########################################################################################################


def import_units(filename, tagname,  table, dictionary):
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    inserts = []
    for event, element in etree.iterparse(filename, tag=tagname):

        sqldata = {}
        nr_elements = 0
        for child in element:
            nr_elements = nr_elements + 1
            if child.tag in dictionary.keys():
                # print("Tag: "+child.tag+"\n")
                column = dictionary[child.tag]
                value = child.text
                if (value == 'true'):
                    value = 1
                if (value == 'false'):
                    value = 0
                sqldata[column] = value
            else:
                print("Unknown column: >" + child.tag+"<")
                exit(0)
        # print("Elements: "+str(nr_elements)+"\n")
        if (sqldata['id_mastr_unit'] != None):
            placeholder = ", ".join(["?"] * len(sqldata))
            stmt = "insert into `{table}` ({columns}) values ({values});".format(table=table,
                                                                                 columns=",".join(sqldata.keys()),
                                                                                 values=placeholder)
            sqlCursor.execute(stmt, list(sqldata.values()))

    sqlCursor.commit()
    sqlCursor.close()
    return ("Import of "+table+" successfull!")