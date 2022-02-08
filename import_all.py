import os.path

from import_functions import import_catalog as catalog
from import_functions import import_market_player
from import_functions import import_market_roles
from import_functions import import_units

BASE_DIR = 'E:\Temp\markststammdatenregister'

# catalog.import_categories(BASE_DIR+'\Katalogkategorien.xml')
# catalog.import_catalog(BASE_DIR+'\Katalogwerte.xml')
# catalog.import_balancing_areas(BASE_DIR+'\Bilanzierungsgebiete.xml')
#
# #Market roles
# import_market_roles.truncate_market_roles()
# import_market_roles.import_market_roles(BASE_DIR+'\Marktrollen.xml')
#
# #Market players
# import_market_player.truncate_market_player()
# for i in range(100):
#     file = BASE_DIR+'\Marktakteure_'+str(i)+'.xml'
#     if (os.path.isfile(file)):
#         print ('Importing '+file)
#         import_market_player.import_market_player(file)

# Units Thermal
import_units.truncate_units_thermal()
import_units.import_units_thermal(BASE_DIR+'\EinheitenVerbrennung.xml')
exit(0)

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