<script lang="ts">
    import { onMount } from 'svelte';
    let myList = [];
    export let infractionsStore: import("svelte/store").Writable<Array<object>>;
    onMount(() => {
      myList = JSON.parse(infractionsStore).TrafficViolationList;    
    });
    async function doPost (ep,data) {
		const res = await fetch('http://172.17.0.7:5000/' + ep, {
			method: 'POST',
            headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}, 
			body: JSON.stringify(data)
		})
		
		const json = await res.json();
 
    }
    function onColumnClick(id){
        console.log("click " + id)
        var data = {
                    "tf_id" : id,
                    "tf_type" : "TrafficViolation",
                    "is_resolved" : 1,
                    }
        doPost("updateResolved",data);
        var elem = document.getElementById("btn_"+id);
        console.log(elem);
        elem.innerHTML = 'Resolved'    
        elem.disabled = true  
      }    
  </script>
  
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 10px;
    }
  
    th, td {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
  
    th {
      background-color: #f2f2f2;
    }
  
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
  </style>
  
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Description</th>
        <th>Location</th>
        <th>Recorded Date</th>
        <th>Resolved Date</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {#each myList as row}
        <tr>
          {#each Object.values(row) as cell, index}
            {#if index != 3}
                {#if index == 6 && cell == 1}
                    <td>Resolved</td>
                {:else if index == 6}
                    <td>
                        <button id='btn_{row[0]}' on:click={onColumnClick(row[0])}> Unresolved </button>
                    </td>
                {:else}
                <td>{cell}</td>
                {/if}
            {/if}
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
  