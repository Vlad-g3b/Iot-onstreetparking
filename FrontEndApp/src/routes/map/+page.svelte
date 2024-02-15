<script>
    import { onMount } from "svelte";
    import { writable } from 'svelte/store';
    /**
     * @type {typeof import("./Map.svelte").default}
     */
    let Map;
    const infractionsStore = writable([]);
    async function getListItems() {
    const res = await fetch('http://172.17.0.7:5000/getAllUnresolvedTrafficViolation');
      if (res.ok) {
          return await res.text();
      } else {
          // Sometimes the API will fail!
          throw new Error('Request failed');
      }
    }

    onMount(() => {
        if (typeof window !== 'undefined') {
      import('./Map.svelte').then(module => {
        Map = module.default;
      }).catch(error => {
        console.error('Error importing Map component:', error);
      });
    }
        const eventSource = new EventSource("http://172.17.0.7:5000/sse");
        eventSource.onmessage = (event) => {
            // Handle incoming SSE data
            const infractions = JSON.parse(event.data);
            const infractionsTF = infractions.filter(item => item.type == 'TrafficViolation')
            infractionsStore.set(infractionsTF);
            console.log(infractionsTF);
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



{#await getListItems()}
	<p>...waiting</p>
{:then list}
  {#if Map}
    <Map {infractionsStore} {list} latitude={38.248747} longitude={21.738999} />
  {:else}
    <p>Loading...</p>
  {/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}