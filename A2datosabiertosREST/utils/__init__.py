from os.path import join

from requests import get
from definitions import ROOT_DIR
from models.gas_stations import GasStation, EESSPrecioFilter, EESSPrecio
from json import dump

gas_station_file_path = join(ROOT_DIR, "data", "gas_stations.json")


def download_gas_stations() -> GasStation:
    raw_gas_stations = get(
        "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/")
    with open(gas_station_file_path, "w") as outfile:
        gas_station = raw_gas_stations.json()
        dump(gas_station, outfile, indent=4)
        gas_station_json: GasStation = GasStation(**gas_station)
    return gas_station_json


def match_filter(gas_station_filter: EESSPrecioFilter, gas_station: EESSPrecio):
    return (gas_station_filter.provincia is None or gas_station.provincia.upper() == gas_station_filter.provincia.upper())\
           and (gas_station_filter.rotulo is None or gas_station_filter.rotulo.upper() in gas_station.rotulo.upper())
