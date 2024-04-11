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
    "Technologie" : "id_technology",
    "EegMaStRNummer": "id_mastr_eeg",
    "KwkMaStRNummer": "id_mastr_kwk",
    "Buergerenergie": "is_buergerenergie",
    "ReserveartNachDemEnWG": "id_reserve_enwg",
    "DatumDerUeberfuerungInReserve": "date_reserve_enwg"
}

dict_power_solar = {
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
    "Nutzungsbereich" : "id_usage_of_location"
}

dict_power_thermal = {
    "DatumBaubeginn" : "date_construction_start",
    "AnzeigeEinerStilllegung" :  "has_reported_operation_end",
    "ArtDerStilllegung" : "id_operation_end",
    "DatumBeginnVorlaeufigenOderEndgueltigenStilllegung" : "date_end_operation",
    "SteigerungNettonennleistungKombibetrieb" : "power_added_combi_operation",
    "AnlageIstImKombibetrieb" : "is_in_combi_operation",
    "AusschliesslicheVerwendungImKombibetrieb" : "is_only_in_combi_operation",
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
}

dict_power_wind = {
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
    "Nachtkennzeichnung" : "has_night_marking"

}

dict_power_biomass = {
    "KwkMaStRNummer" : "id_mastr_kwk",
    "Hauptbrennstoff" : "id_primary_fuel",
    "Biomasseart"     : "id_biomass_type"
}


dict_power_hydro = {
    "ArtDerWasserkraftanlage" : "id_hydro_type",
    "ArtDesZuflusses" : "id_hydro_source",
    "MinderungStromerzeugung" : "has_restrictions",
    "BestandteilGrenzkraftwerk": "is_border_power_plant",
    "NettonennleistungDeutschland": "power_netto_max_germany",
    "AnzeigeEinerStilllegung": "has_reported_operation_end",
    "ArtDerStilllegung": "id_operation_end",
    "DatumBeginnVorlaeufigenOderEndgueltigenStilllegung": "date_end_operation",
}

dict_power_geothermal_other = {


}

dict_power_storage = {
    "Einsatzort" : "id_location_type",
    "AcDcKoppelung" : "id_ac_dc_connection",
    "Batterietechnologie" : "id_battery_technology",
    "PumpbetriebLeistungsaufnahme" : "power_netto_pumping",
    "PumpbetriebKontinuierlichRegelbar" : "is_linear_controllable",
    "Pumpspeichertechnologie"  : "id_pump_storage_technology",
    "Notstromaggregat" : "is_backup_power",
    "BestandteilGrenzkraftwerk"  : "is_border_power_plant",
    "NettonennleistungDeutschland" :  "power_netto_max_germany",
    "ZugeordnenteWirkleistungWechselrichter" : "power_converter",
    "SpeMastrNummer" : "id_mastr_storage",
    "EegAnlagentyp"  :  "id_eeg_type"
}

dict_power_consumer = {
    "NameStromverbrauchseinheit" : "name",
    "AnzahlStromverbrauchseinheitenGroesser50Mw" : "nr_units_above_50mw",
    "PraequalifiziertGemaessAblav" : "prequalified_ablav",
    "AnteilBeinflussbareLast" : "controllable_load",
    "ArtAbschaltbareLast" : "id_type_controllable"

}

dict_gas_generator = {
    "Erzeugungsleistung" : "max_inject_power",
    "NameGaserzeugungseinheit" : "name",
    "SpeicherMaStRNummer" : "id_mastr_storage"
}

dict_gas_storage = {
    "NameGasspeicher" : "name",
    "Speicherart" : "id_storage_type",
    "MaximalNutzbaresArbeitsgasvolumen" : "working_gas_max",
    "MaximaleEinspeicherleistung" : "max_withdrawal_power" ,  # Withdrawal from the grid - always grid view
    "MaximaleAusspeicherleistung" : "max_inject_power",       # Inject into the grid
    "DurchschnittlicherBrennwert" : "caloric_value_avg",
    "SpeicherMaStRNummer" : "id_mastr_storage",
    "Weic_Na" : "no_weic"
}

dict_gas_consumer = {
    "NameGasverbrauchsseinheit" : "name",
    "MaximaleGasbezugsleistung" : "max_withdrawal_power",
    "EinheitDientDerStromerzeugung" : "is_power_generator",
    "VerknuepfteEinheitenMaStRNummern" : "id_mastr_connected"
}

###########################################################################################################
#  Power Nuclear units
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
#  Power Solar units
###########################################################################################################
def truncate_units_solar():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_solar"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_solar(filename):
    dict_units = dict_all_units | dict_power_solar  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitSolar","power_units_solar",dict_units)


###########################################################################################################
#  Power Wind units
###########################################################################################################
def truncate_units_wind():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_wind"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_wind(filename):
    dict_units = dict_all_units | dict_power_wind  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitWind","power_units_wind",dict_units)

###########################################################################################################
#  Power Thermal units
###########################################################################################################
def truncate_units_thermal():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_thermal"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_thermal(filename):
    dict_units = dict_all_units | dict_power_thermal  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitVerbrennung","power_units_thermal",dict_units)

###########################################################################################################
#  Power Biomass units
###########################################################################################################
def truncate_units_biomass():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_biomass"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_biomass(filename):
    dict_units = dict_all_units | dict_power_biomass  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitBiomasse","power_units_biomass",dict_units)

###########################################################################################################
#  Power Hydro units
###########################################################################################################
def truncate_units_hydro():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_hydro"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_hydro(filename):
    dict_units = dict_all_units | dict_power_hydro  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitWasser","power_units_hydro",dict_units)


###########################################################################################################
#  Power Geothermal and other units
###########################################################################################################
def truncate_units_geothermal_other():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_geo_soltherm_other"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_geothermal_other(filename):
    dict_units = dict_all_units | dict_power_geothermal_other  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitGeothermieGrubengasDruckentspannung","power_units_geo_soltherm_other",dict_units)

###########################################################################################################
#  Power Storage units
###########################################################################################################
def truncate_units_storage():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_storage"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_storage(filename):
    dict_units = dict_all_units | dict_power_storage  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitStromSpeicher","power_units_storage",dict_units)

###########################################################################################################
#  Power consumer units
###########################################################################################################
def truncate_units_consumer():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE power_units_consumer"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_consumer(filename):
    dict_units = dict_all_units | dict_power_consumer  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitStromVerbraucher","power_units_consumer",dict_units)

###########################################################################################################
#  Gas generator units
###########################################################################################################
def truncate_units_gas_generator():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE gas_units_generator"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_gas_generator(filename):
    dict_units = dict_all_units | dict_gas_generator # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitGasErzeuger","gas_units_generator",dict_units)

###########################################################################################################
#  Gas Storage units
###########################################################################################################
def truncate_units_gas_storage():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE gas_units_storage"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_gas_storage(filename):
    dict_units = dict_all_units | dict_gas_storage  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitGasSpeicher","gas_units_storage",dict_units)

###########################################################################################################
#  Gas consumer units
###########################################################################################################
def truncate_units_gas_consumer():
    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sql_string = "TRUNCATE TABLE gas_units_consumer"
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute(sql_string)


def import_units_gas_consumer(filename):
    dict_units = dict_all_units | dict_gas_consumer  # Needs Python 3.9.x   but it's so elegant :-)
    return import_units(filename,"EinheitGasverbraucher","gas_units_consumer",dict_units)


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
            stmt = "insert ignore into `{table}` ({columns}) values ({values});".format(table=table,
                                                                                 columns=",".join(sqldata.keys()),
                                                                                 values=placeholder)
            sqlCursor.execute(stmt, list(sqldata.values()))

    sqlCursor.commit()
    sqlCursor.close()
    return ("Import of "+table+" successfull!")
