from json import load
from os.path import join, exists
from definitions import ROOT_DIR
from models.gas_stations import GasStation
from utils import download_gas_stations

gas_station_file_path = join(ROOT_DIR, "data", "gas_stations.json")
if not exists(gas_station_file_path):
    gas_station_json = download_gas_stations()
else:
    with open(gas_station_file_path, "r") as file:
        if file.__sizeof__() > 0:
            gas_station = load(file)
            gas_station_json: GasStation = GasStation(**gas_station)
