from import_all import import_all
from process_data.generate_json import generate_json
from process_data.generate_kepler_data import generate_kepler_data
from process_data.generate_h3_index import generate_h3
from process_data.generate_histograms import generate_histograms

import_all()
generate_h3()
generate_json()
generate_kepler_data()
generate_histograms()

