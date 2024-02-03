<script>
    import { onMount } from "svelte";
    import "leaflet/dist/leaflet.css";

    /**
     * @type {number}
     */
    export let latitude;
    /**
     * @type {number}
     */
    export let longitude;
    
    /**
     * @type {import("svelte/store").Writable<object>}
     */
    export let infractionsStore; // Declare a prop for the infractions store

    let map;

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
                            L.marker([
                                infraction.location.value.coordinates[0],
                                infraction.location.value.coordinates[1],
                            ])
                                .addTo(map)
                                .bindPopup("infraction.description");
                        });
                    },
                );

                // Unsubscribe from the store when component is destroyed
                return unsubscribe;
            });
        }
    });
</script>

<div id="map"></div>

<style>
    #map {
        height: 100vh;
    }
</style>
