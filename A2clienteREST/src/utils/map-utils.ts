import { LeafletMouseEvent, Map } from "leaflet";
import { Coordinates } from "../data/types/map"
import { EESSPrecio } from "../api/A2datosabiertosREST/models/EESSPrecio"
import house_icon from "../resources/house-icon.png";
import gas_station_icon from "../resources/gas-station-icon.png";

export function addHouseToMap(L, coordinates: Coordinates, map: Map) {
    L.marker([
        coordinates.latitude,
        coordinates.longitude
    ], {
        title: "Vivienda",
        icon: L.icon({
            iconUrl: house_icon,
            iconSize: [50, 50],
        })
    }).addTo(map);
}

export function addGasStationsToMap(L, gasStations: EESSPrecio[], map: Map) {
    let last: any = undefined;
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
        }).on("click", (event: LeafletMouseEvent) => {
            if (event.target.getPopup() === undefined) {
                event.target.bindPopup(`
                    ${gasStation.precioGasolina95E5 ? `Gasolina 95: ${gasStation.precioGasolina95E5}<br>` : ''}
                    ${gasStation.precioGasolina98E5 ? `Gasolina 98: ${gasStation.precioGasolina98E5}<br>` : ''}
                    ${gasStation.precioGasoleoA ? `Gasoil: ${gasStation.precioGasoleoA}<br>` : ''}
                    ${gasStation.precioGasoleoPremium ? `Gasoil Premium: ${gasStation.precioGasoleoPremium}<br>` : ''}
                `);
            }
            event.target.openPopup();
            if (last !== undefined) {
                last.closePopup();
            } else {
                event.target.openPopup();
            }
            last = event.target;
        }).addTo(map);
    })
}

