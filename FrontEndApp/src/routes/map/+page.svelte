<script>
    import Map from "./Map.svelte";
    import { onMount } from "svelte";
    import { writable } from 'svelte/store';

    const infractionsStore = writable([]);

    onMount(() => {
        const eventSource = new EventSource("http://127.0.0.1:5000/sseFake");
        eventSource.onmessage = (event) => {
            // Handle incoming SSE data

            const infractions = JSON.parse(event.data);
            console.log(infractions)
            infractionsStore.set(infractions);
        };

        eventSource.onerror = (error) => {
            console.error("SSE Error:", error);
            // Handle errors
        };

        return () => {
            // Cleanup on component destruction
            console.log("return");
            eventSource.close();
        };
    });
</script>

<Map {infractionsStore} latitude={38.248747} longitude={21.738999} />
