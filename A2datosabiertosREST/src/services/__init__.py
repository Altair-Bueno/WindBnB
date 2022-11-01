from json import load
from os.path import exists
from typing import List

from src.models.gas_stations import GasStation
from src.models.average_stay import AverageStay
from src.utils import download_gas_stations, download_average_stay, gas_station_file_path, average_stay_file_path
from pydantic import parse_obj_as


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
