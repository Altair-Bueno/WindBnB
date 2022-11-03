from os.path import join
from typing import List
from pydantic import parse_obj_as

from requests import get
from src.definitions import ROOT_DIR
from src.models.gas_stations import GasStation, EESSPrecioFilter, EESSPrecio
from src.models.average_stay import AverageStay
from json import dump

gas_station_file_path = join(ROOT_DIR, "data", "gas_stations.json")
average_stay_file_path = join(ROOT_DIR, "data", "average_stay.json")


def download_gas_stations() -> GasStation:
    raw_gas_stations = get(
        "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/")
    with open(gas_station_file_path, "w") as outfile:
        gas_station = raw_gas_stations.json()
        dump(gas_station, outfile, indent=4)
        gas_station_json: GasStation = GasStation(**gas_station)
    return gas_station_json


def download_average_stay() -> List[AverageStay]:
    raw_average_stay = get(
        "https://servicios.ine.es/wstempus/js/es/DATOS_TABLA/49759?tip=AM")
    with open(average_stay_file_path, "w") as outfile:
        average_stay = raw_average_stay.json()
        dump(average_stay, outfile, indent=4)
        average_stay_json: List[AverageStay] = parse_obj_as(List[AverageStay], average_stay)
    return average_stay_json


def match_filter(gas_station_filter: EESSPrecioFilter, gas_station: EESSPrecio):
    return (gas_station_filter.provincia is None or gas_station.provincia.upper() == gas_station_filter.provincia.upper()) \
           and (gas_station_filter.rotulo is None or gas_station_filter.rotulo.upper() in gas_station.rotulo.upper())


def match_filter_average_stay(wanted_name: str, current_name: str):
    return wanted_name.upper() == current_name.upper()
