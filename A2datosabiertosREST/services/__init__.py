import json
from os.path import join
import requests
from definitions import ROOT_DIR
from models.gas_stations import GasStation
# from polars import read_json

gas_station_file_path = join(ROOT_DIR, "data", "gas_stations.json")
raw_gas_stations = requests.get("https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/")
with open(gas_station_file_path, "w") as outfile:
    gas_station = raw_gas_stations.json()
    json.dump(gas_station, outfile, indent=4)
    gas_station_json = GasStation(**gas_station)
