<script >
    import { onMount } from 'svelte';
  import Table from './Table.svelte';
  import { writable } from 'svelte/store';

  const infractionsStore = writable([]);
    async function getListItems() {
    const res = await fetch('http://172.17.0.7:5000/getAllTrafficViolation');
      if (res.ok) {
          return await res.text();
      } else {
          // Sometimes the API will fail!
          throw new Error('Request failed');
      }
    }

</script>
<title>TrafficViolation</title>
<header>
    <h1>Manage TrafficViolation</h1>
</header>
{#await getListItems()}
	<p>...waiting</p>
{:then infractionsStore}
  {#if Table}
    <Table  {infractionsStore}/>
  {:else}
    <p>Loading...</p>
  {/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}