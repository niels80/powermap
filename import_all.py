import os.path

from import_functions import import_catalog as catalog
from import_functions import import_market_player
from import_functions import import_market_roles
from import_functions import import_units

BASE_DIR = os.environ.get('PATH_MARKTSTAMMDATENREGISTER')

catalog.import_categories(BASE_DIR+'\Katalogkategorien.xml')
catalog.import_catalog(BASE_DIR+'\Katalogwerte.xml')
catalog.import_balancing_areas(BASE_DIR+'\Bilanzierungsgebiete.xml')
#
# #Market roles
import_market_roles.truncate_market_roles()
import_market_roles.import_market_roles(BASE_DIR+'\Marktrollen.xml')
#
# #Market players
import_market_player.truncate_market_player()
for i in range(100):
    file = BASE_DIR+'\Marktakteure_'+str(i)+'.xml'
    if (os.path.isfile(file)):
        print ('Importing '+file)
        import_market_player.import_market_player(file)



#########################################################
# GAS
#########################################################

# Units Consumer
import_units.truncate_units_gas_consumer()
import_units.import_units_gas_consumer(BASE_DIR+'\EinheitenGasverbraucher.xml')


# Units Storage
import_units.truncate_units_gas_storage()
import_units.import_units_gas_storage(BASE_DIR+'\EinheitenGasSpeicher.xml')


# Units Generator
import_units.truncate_units_gas_generator()
import_units.import_units_gas_generator(BASE_DIR+'\EinheitenGasErzeuger.xml')

#########################################################
# Power
#########################################################

# Units Consumer
import_units.truncate_units_consumer()
import_units.import_units_consumer(BASE_DIR+'\EinheitenStromVerbraucher.xml')


# Units Storage
import_units.truncate_units_storage()
for i in range(100):
     file = BASE_DIR+'\EinheitenStromSpeicher_'+str(i)+'.xml'
     if (os.path.isfile(file)):
         print ('Importing '+file)
         import_units.import_units_storage(file)


# Units Geothermal and others
import_units.truncate_units_geothermal_other()
import_units.import_units_geothermal_other(BASE_DIR+'\EinheitenGeoSolarthermieGrubenKlaerschlammDruckentspannung.xml')


# Units Hydro
import_units.truncate_units_hydro()
import_units.import_units_hydro(BASE_DIR+'\EinheitenWasser.xml')

# Units Biomass
import_units.truncate_units_biomass()
import_units.import_units_biomass(BASE_DIR+'\EinheitenBiomasse.xml')

# Units Thermal
import_units.truncate_units_thermal()
import_units.import_units_thermal(BASE_DIR+'\EinheitenVerbrennung.xml')


#  Units Nuclear
import_units.truncate_units_nuclear()
import_units.import_units_nuclear(BASE_DIR+'\EinheitenKernkraft.xml')

# Units Solar
import_units.truncate_units_solar()
for i in range(100):
     file = BASE_DIR+'\EinheitenSolar_'+str(i)+'.xml'
     if (os.path.isfile(file)):
         print ('Importing '+file)
         import_units.import_units_solar(file)

# Units Wind
import_units.truncate_units_wind()
import_units.import_units_wind(BASE_DIR+'\EinheitenWind.xml')