from json import load
from os.path import join, exists
from typing import List

from definitions import ROOT_DIR
from models.gas_stations import GasStation
from models.average_stay import AverageStay
from utils import download_gas_stations, download_average_stay
from pydantic import parse_obj_as

gas_station_file_path = join(ROOT_DIR, "data", "gas_stations.json")
average_stay_file_path = join(ROOT_DIR, "data", "average_stay.json")

if not exists(gas_station_file_path):
    gas_station_json: GasStation = download_gas_stations()
else:
    with open(gas_station_file_path, "r") as file:
        if file.__sizeof__() > 0:
            gas_station = load(file)
            gas_station_json: GasStation = GasStation(**gas_station)

if not exists(average_stay_file_path):
    average_stay_json: List[AverageStay] = download_average_stay()
else:
    with open(average_stay_file_path, "r") as file:
        if file.__sizeof__() > 0:
            average_stay = load(file)
            average_stay_json: List[AverageStay] = parse_obj_as(List[AverageStay], average_stay)
