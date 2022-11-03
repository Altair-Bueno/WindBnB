from math import cos


class Area():
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float

    def __init__(self, kilometers: int, latitude: float, longitude: float):
        latitude_offset = self.km_to_latitude(kilometers)
        longitude_offset = self.km_to_longitude(kilometers, latitude)

        self.min_latitude = latitude - latitude_offset
        self.max_latitude = latitude + latitude_offset
        self.min_longitude = longitude - longitude_offset
        self.max_longitude = longitude + longitude_offset

    def km_to_latitude(self, kilometers: int) -> float:
        return kilometers / 111.0

    def km_to_longitude(self, kilometers: int, latitude: float) -> float:
        return kilometers / (111 * cos(latitude))

    def is_in_area(self, latitude: float, longitude: float) -> bool:
        return self.min_latitude < latitude < self.max_latitude and self.min_longitude < longitude < self.max_longitude
