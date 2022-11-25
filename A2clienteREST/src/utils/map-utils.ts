import L, { Map } from "leaflet";
import { Coordinates } from "../data/types/map"
import { EESSPrecio } from "../api/A2datosabiertosREST/models/EESSPrecio"
import house_icon from "../resources/house-icon.png";
import gas_station_icon from "../resources/gas-station-icon.png";

export function addHouseToMap(coordinates: Coordinates, map: Map) {
    L.marker([
        coordinates.latitude,
        coordinates.longitude
    ], {
        title: "Vivienda",
        icon: L.icon({
            iconUrl: house_icon,
            iconSize: [50, 50],
        })
    }).on("click", () => {
            L.popup()
    }).addTo(map);
}

export function addGasStationsToMap(gasStations: EESSPrecio[], map: Map) {
    gasStations.forEach((gasStation: EESSPrecio) => {
        L.marker([
            +gasStation.latitud.replace(",", "."), 
            +gasStation.longitudWGS84.replace(",", ".")
        ], {
            title: gasStation.rtulo,
            icon: L.icon({
                iconUrl: gas_station_icon,
                iconSize: [38, 38],
            }),
            riseOnHover: true,
        }).on("click", () => {
            L.popup()
        }).addTo(map);
    })
}

