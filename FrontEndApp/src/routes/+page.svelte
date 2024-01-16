<script>
    import { onMount } from 'svelte';
  
    /**
     * @type {any[]}
     */
    let eventData = [];
   
    onMount(() => {
      const eventSource = new EventSource('http://172.17.0.7:5000/sse');
      eventSource.onmessage = (event) => {
        // Handle incoming SSE data
        console.log(event.data)
        const data = JSON.parse(event.data);
        eventData = [...eventData, data];
      };
  
      eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        // Handle errors
      };
  
      return () => {
        // Cleanup on component destruction
        console.log("return");
        eventSource.close();
      };
    });
  </script>
  
  <div>
    <h1>Server-Sent Events</h1>
    <ul>
      {#each eventData as event (event.id)}
        <li>{event.data}</li>
      {/each}
    </ul>
  </div>
