<script lang="ts">
  import "leaflet/dist/leaflet.css";
  import type { Map } from "leaflet";
  import type { EESSPrecio } from "../api/A2datosabiertosREST";
  import type { Coordinates } from "../data/types/map";

  function setMap(mapElement: HTMLElement) {
    (async () => {
      const L = await import("leaflet");
      const { addHouseToMap, addGasStationsToMap } = await import(
        "../utils/map-utils"
      );

      var map: Map = L.map(mapElement).setView(
        [coordinates.latitude, coordinates.longitude],
        13
      );
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      addHouseToMap(L, coordinates, map);
      addGasStationsToMap(L, gasStations, map);
    })();
  }

  /**
   * param: coordinates: Coordinates
   *
   * Coordinates of the house
   */
  export let coordinates: Coordinates;
  /**
   * param: gasStations: EESSPrecio[]
   *
   * Array of gas stations to be displayed as markers
   */
  export let gasStations: EESSPrecio[];
</script>

<figure class="map" use:setMap />

<style>
  .map {
    height: 40vh;
  }
</style>
