<script lang="ts">
    import { onMount } from 'svelte';
    import L from 'leaflet' ;
    import 'leaflet/dist/leaflet.css';
    import 'leaflet.heat';
    
    //import 'leaflet.heat/dist/leaflet-heat.js';
    import { toast } from '@zerodevx/svelte-toast';
    import * as turf from '@turf/turf';

    export let latitude : number;
    export let longitude: number;
    export let infractionsStore: import("svelte/store").Writable<Array<object>>;
    export let list: Array<object>;
    let map: L.Map;

    let randomPointInPoly = function(polygon) {
    var bounds = polygon.getBounds(); 
    var x_min  = bounds.getEast();
    var x_max  = bounds.getWest();
    var y_min  = bounds.getSouth();
    var y_max  = bounds.getNorth();

    var lat = y_min + (Math.random() * (y_max - y_min));
    var lng = x_min + (Math.random() * (x_max - x_min));
    var point  = turf.point([lng, lat]);
    var poly   = polygon.toGeoJSON();
    var inside = turf.inside(point, poly);
        if (inside) {
            return point
        } else {
            return randomPointInPoly(polygon)
        }
}

async function doPost (ep,data) {
		const res = await fetch('http://172.17.0.7:5000/' + ep, {
			method: 'POST',
            headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}, 
			body: JSON.stringify(data)
		})
		
		const json = await res.json()
		let result = JSON.stringify(json)
        console.log(result)
	}

function addFakePoints(heatL: never[][], poll: any){
    for (let index = 0; index < 20; index++) {
        var point = randomPointInPoly(poll);
        let coordinates = point.geometry.coordinates.reverse();
        let newArray = [].concat(coordinates, [0.2]);
        heatL.push(newArray)
    }
    return heatL
}

 function createFakeLines(L){
    let heatL: never[][] = [];
    var latlngs = [
        [38.24342665110504, 21.732123117195943],
        [38.24397197980599, 21.732811804564857],
        [38.24401323644827, 21.732748603592494],
        [38.243467725225884, 21.732076950954465],
        [38.24342665110504, 21.732123117195943],
    ];
    L.polygon(latlngs, {color: 'red'}).addTo(map);
    var latlngs = [
        [38.246676750616274, 21.736152262797702],
        [38.24661018382857, 21.736259134505573],
        [38.247165869926, 21.737010921691972],
        [38.24726716641305, 21.736889309058878],
        [38.246676750616274, 21.736152262797702],
    ];       
    let poll = L.polygon(latlngs, {color: 'green'}).addTo(map);
    heatL = addFakePoints(heatL,poll);

    var latlngs = [
        [38.24539178223797, 21.734483343711513],
        [38.2453102994774, 21.734591605801274],
        [38.245707084233544, 21.735101339807244],
        [38.24576022488465, 21.734984055876662],
        [38.24539178223797, 21.734483343711513],
    ];       
    poll = L.polygon(latlngs, {color: 'blue'}).addTo(map);
    heatL = addFakePoints(heatL,poll);
    var latlngs = [
        [38.24478951618356, 21.733693932631247],
        [38.2446761479004, 21.733833771163855],
        [38.24523590207996, 21.734510409224875],
        [38.24534926949015, 21.734415679896337],
        [38.24478951618356, 21.733693932631247],
    ];       
    poll = L.polygon(latlngs, {color: 'yellow'}).addTo(map);
    heatL = addFakePoints(heatL,poll);
    var latlngs = [
        [38.245313842193454, 21.73308946929674],
        [38.245207560199766, 21.73325637335179],
        [38.24574959674297, 21.733919478651586],
        [38.245855877944145, 21.733793172880194],
        [38.245313842193454, 21.73308946929674],
    ];       
    poll = L.polygon(latlngs, {color: 'black'}).addTo(map);
    heatL = addFakePoints(heatL,poll);
    return heatL;
 }
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
                //get all the points from API make a list of coordiantes, and sum de intensities starting from 0.5??
                
                import("leaflet.heat").then(() => {
                     
                    var myList = JSON.parse(list).TrafficViolationList;    
                    let heatL = createFakeLines(L);
                    myList.forEach(element => {
                        let newArray = [].concat(JSON.parse(element[2]), [0.2]);
                        heatL.push(newArray)
                        console.log(element)
                        let markcoord = JSON.parse(element[2])
                        let content = 
                        `<div>ID:${element[0]} Description:${element[1]}</div>
                                    <button class="remove-marker-btn" data-marker-id="${element[0]}">Mark as resolved! </button>`;
                        
                        let marker = L.marker([
                            markcoord[0], markcoord[1]
                            ])
                                .addTo(map)
                                .bindPopup( content
                                );
                                marker.infractionId = element[0];
                    });
                    var heat2 = L.heatLayer(heatL, {radius: 20}).addTo(map);
                });
                // Subscribe to changes in the infractions store
                const unsubscribe = infractionsStore.subscribe(
                    (infractions) => {
                        // Clear existing markers

                        // Add markers for each infraction
                        infractions.forEach((infraction) => {
                            let marker = L.marker([
                                infraction.location.value.coordinates[0],
                                infraction.location.value.coordinates[1],
                            ])
                                .addTo(map)
                                .bindPopup(
                                    `<div>ID:${infraction.id}</div><button class="remove-marker-btn" data-marker-id="${infraction.id}">Mark as resolved! </button>`,
                                );

                            toast.push(`<div>Detected ${infraction.id} </div>`,{
                                                        theme: {
                                                            '--toastColor': 'mintcream',
                                                            '--toastBackground': 'rgba(72,187,120,0.9)',
                                                            '--toastBarBackground': '#2F855A'
                                                        }
                                                        });
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
                                var data = {
                                    "tf_id" : markerId,
                                    "tf_type" : "TrafficViolation",
                                    "is_resolved" : 1,
                                }
                                doPost("updateResolved",data);
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
