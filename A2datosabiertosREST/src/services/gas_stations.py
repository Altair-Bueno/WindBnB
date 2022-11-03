from typing import List
from src.models.gas_stations import EESSPrecio, EESSPrecioFilter
from src.services import gas_station_json
from src.models.area import Area
from src.services.error import NoGasStations
from src.utils import match_filter


class GasStationService:
    def __init__(self):
        pass

    async def find_gas_stations(self, gas_station_filter: EESSPrecioFilter, limit: int) -> List[EESSPrecio]:
        result: List[EESSPrecio] = []
        index: int = 0
        gas_station_list: List[EESSPrecio] = gas_station_json.ListaEESSPrecio
        if limit == -1:
            limit = gas_station_list.__len__()

        while result.__len__() < limit and index < gas_station_list.__len__() - 1:
            current_eessprecio = gas_station_list.__getitem__(index)
            if match_filter(gas_station_filter, current_eessprecio):
                result.append(current_eessprecio)
            index += 1

        if result.__len__() <= 0:
            if gas_station_filter.rotulo is not None:
                gas_station_filter.rotulo = f"{gas_station_filter.rotulo} "
            else:
                gas_station_filter.rotulo = ""
            raise NoGasStations(f"No {gas_station_filter.rotulo}gas stations found in {gas_station_filter.provincia}")
        else:
            return result

    def find_by_area(self, kilometers: int, latitude: float, longitude: float, limit: int) -> List[EESSPrecio]:
        area: Area = Area(kilometers, latitude, longitude)
        result: List[EESSPrecio] = []
        index: int = 0
        gas_station_list: List[EESSPrecio] = gas_station_json.ListaEESSPrecio
        if limit == -1:
            limit = gas_station_list.__len__()

        while result.__len__() < limit and index < gas_station_list.__len__() - 1:
            current_eessprecio = gas_station_list.__getitem__(index)
            if area.is_in_area(float(current_eessprecio.latitud.replace(",", ".")),
                               float(current_eessprecio.longitud.replace(",", "."))):
                result.append(current_eessprecio)
            index += 1

        if result.__len__() <= 0:
            raise NoGasStations(f"No gas stations found within {kilometers}km from [{latitude}º, {longitude}º]")
        else:
            return result
