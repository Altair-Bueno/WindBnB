from typing import List

from src.models.average_stay import AverageStayFilter, AverageStay
from src.services import average_stay_json
from src.utils import match_filter_average_stay


class AverageStayService:

    def __init__(self):
        pass

    async def find_average_stay(self, average_stay_filter: AverageStayFilter) -> float:
        result: float = 0.0
        if average_stay_filter.mes is None:
            average_stay_filter.mes = "Total"
        wanted_name = average_stay_filter.provincia + ", " + average_stay_filter.mes
        average_stay_list: List[AverageStay] = average_stay_json
        index = 1
        while index < average_stay_list.__len__() - 1 and result == 0.0:
            current_element: AverageStay = average_stay_list.__getitem__(index)
            current_name = current_element.nombre
            if match_filter_average_stay(wanted_name, current_name):
                result = current_element.Data.__getitem__(0).valor
            index += 1
        return result
