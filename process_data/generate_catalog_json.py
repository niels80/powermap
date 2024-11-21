import pytz
import os
import io
import simplejson as json
from common import helperfunctions as helper
from pathlib import Path

OUTPATH = str(os.environ["OUTPATH"])
NR_FOLDERS = 50

TZONE = pytz.timezone(str(os.environ["TIMEZONE"]))


def generate_catalog_json():

    sqlConnection = helper.getSqlConnection(os.environ["POWERMAP_DB"])
    sqlCursor = sqlConnection.cursor()

    # Catalog

    catalog = {}

    sqlstr = "SELECT c.*,0 AS 'XXX_SEPARATOR_XXX',cg.* FROM catalog c LEFT JOIN catalog_categories cg ON (c.category_id=cg.id) ORDER BY c.id"
    sqlCursor.execute(sqlstr)
    results = sqlCursor.fetchall()
    colnames = [column[0] for column in sqlCursor.description]
    n = colnames.index('XXX_SEPARATOR_XXX')
    for row in results:

        dat_catalog    = dict(zip(colnames[:n], row[:n]))
        dat_category   = dict(zip(colnames[n+1:], row[n+1:]))
        data = {
            'entry' : dat_catalog,
            'category': dat_category
        }
        catalog[dat_catalog['id']] = data

    with io.open(OUTPATH +"/catalog.json", 'w',encoding='utf8') as outfile:
        outfile.write(json.dumps(catalog, use_decimal=True, default=str, ensure_ascii=False))
        outfile.close()



if __name__ == "__main__":
    generate_catalog_json()