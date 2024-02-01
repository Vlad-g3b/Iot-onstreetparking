<script>
  import { onMount } from 'svelte';
  import 'leaflet/dist/leaflet.css';

  export let xCoord;
  export let yCoord;
  let map;

  onMount(() => {
    if (typeof window !== 'undefined') {
      import('leaflet').then(L => {
        map = L.map('map').setView([xCoord, yCoord], 16); // Athens coordinates
    
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
    
        L.marker([xCoord, yCoord]).addTo(map)
          .bindPopup('infraction');
      });
    }
  });
</script>

<style>
  #map {
    height: 90vh;
  }
</style>

<div id="map"></div>
