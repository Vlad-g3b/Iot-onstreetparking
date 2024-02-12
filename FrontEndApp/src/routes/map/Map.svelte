<script lang="ts">
    import { onMount } from 'svelte';
    import L from 'leaflet' ;
    import 'leaflet/dist/leaflet.css';
    import 'leaflet.heat';
    //import 'leaflet.heat/dist/leaflet-heat.js';

    
    export let latitude : number;
    export let longitude: number;
    export let infractionsStore: import("svelte/store").Writable<Array<object>>;

    let map: L.Map;

    onMount(() => {
        if (typeof window !== "undefined") {
            import("leaflet").then((L) => {
                map = L.map("map").setView([latitude, longitude], 16);

                L.tileLayer(
                    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    {
                        attribution: "&copy; OpenStreetMap contributors",
                    },
                ).addTo(map);
                import("leaflet.heat").then(() => {
                    var heat2 = L.heatLayer([
                    [38.248747, 21.738999, 0.5],
                    [38.248747, 21.738999, 0.5],
                    [38.248747, 21.738999, 4],

                    [38.248747, 21.738999, 0.2],
                    ], {radius: 25}).addTo(map);
                });
                // Subscribe to changes in the infractions store
                const unsubscribe = infractionsStore.subscribe(
                    (infractions) => {
                        // Clear existing markers
                        map.eachLayer((layer) => {
                            if (layer instanceof L.Marker) {
                                map.removeLayer(layer);
                            }
                        });

                        // Add markers for each infraction
                        infractions.forEach((infraction) => {
                            let marker = L.marker([
                                infraction.location.value.coordinates[0],
                                infraction.location.value.coordinates[1],
                            ])
                                .addTo(map)
                                .bindPopup(
                                    `<button class="remove-marker-btn" data-marker-id="${infraction.id}">Remove Marker</button>`,
                                );

                            // Store infraction ID in marker for identification
                            marker.infractionId = infraction.id;
                        });
                    },
                );

                // Handle click event for remove marker button
                document.addEventListener("click", function (event) {
                    if (event.target.classList.contains("remove-marker-btn")) {
                        const markerId = event.target.dataset.markerId;
                        // Find and remove marker from map
                        Object.values(map._layers).forEach((layer) => {
                            if (
                                layer instanceof L.Marker &&
                                layer.infractionId === markerId
                            ) {
                                map.removeLayer(layer);
                            }
                        });
                    }
                });

                // Unsubscribe from the store when component is destroyed
                return unsubscribe;
            });
        }
    });
</script>

<div id="map"></div>

<style>
    #map {
        height: 100%;
    }
</style>
