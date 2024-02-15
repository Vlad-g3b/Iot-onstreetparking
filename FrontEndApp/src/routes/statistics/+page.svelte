<script >
import { onMount } from 'svelte';
import Chart from '../components/Chart.svelte';
import { writable } from 'svelte/store';

const infractionsStore = writable([]);
  async function getListItems() {
  const res = await fetch('http://172.17.0.7:5000/getStats');
    if (res.ok) {
        return await res.text();
    } else {
        // Sometimes the API will fail!
        throw new Error('Request failed');
    }
  }

</script>
<title>Statistics</title>
<header>
    <h1>Statistics</h1>
</header>

{#await getListItems()}
	<p>...waiting</p>
{:then infractionsStore}
  {#if Chart}
    <Chart  {infractionsStore}/>
  {:else}
    <p>Loading...</p>
  {/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
