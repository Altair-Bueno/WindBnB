from os.path import join
from requests import get
from definitions import ROOT_DIR
from models.gas_stations import GasStation
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
