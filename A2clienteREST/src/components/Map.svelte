<script lang="ts">
    import type { LeafletMouseEvent, Map } from "leaflet";
    import type { EESSPrecio } from "../api/A2datosabiertosREST";
    import type { Coordinates } from "../data/types/map";
    import gas_station_icon from "../resources/gas-station-icon.png";
    import house_icon from "../resources/house-icon.png";

    function setMap(mapElement: HTMLElement, coordinates: Coordinates) {
        (async () => {
            let last: any = undefined;
            const L = await import("leaflet")
            var map: Map = L.map(mapElement).setView([coordinates.latitude, coordinates.longitude], 13);
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(map);

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
        })()
    }

    export let coordinates: Coordinates;
    export let gasStations: EESSPrecio[];
</script>

<figure class="map" use:setMap={coordinates}/>