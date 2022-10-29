from typing import List
from models.gas_stations import GasStation, EESSPrecio
from services import gas_station_json
from models.area import Area


class GasStationService:
    def __init__(self):
        pass

    async def find_by_provincia(self, provincia: str, limit: int) -> List[EESSPrecio]:
        result: List[EESSPrecio] = []
        index: int = 0
        gas_station_list: List[EESSPrecio] = gas_station_json.ListaEESSPrecio
        if limit == -1:
            limit = gas_station_list.__len__()

        while result.__len__() < limit and index < gas_station_list.__len__() - 1:
            current_eessprecio = gas_station_list.__getitem__(index)
            if current_eessprecio.Provincia == provincia:
                result.append(current_eessprecio)
            index += 1
        return result

    async def find_by_area(self, kilometers: int, latitude: float, longitude: float, limit: int) -> List[EESSPrecio]:
        result: List[EESSPrecio] = []
        area: Area = Area(kilometers, latitude, longitude)

        index: int = 0
        gas_station_list: List[EESSPrecio] = gas_station_json.ListaEESSPrecio
        if limit == -1:
            limit = gas_station_list.__len__()

        while result.__len__() < limit and index < gas_station_list.__len__() - 1:
            current_eessprecio = gas_station_list.__getitem__(index)
            latitud = float(current_eessprecio.Latitud)
            if area.max_latitude > current_eessprecio.Latitud > area.min_latitude:
                result.append(current_eessprecio)
            index += 1
        return result
