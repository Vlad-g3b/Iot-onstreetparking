<script>
    import { onMount } from 'svelte';
  
    /**
     * @type {any[]}
     */
    let eventData = [];
    let cnt = 0;
    onMount(() => {
      const eventSource = new EventSource('http://172.17.0.7:5000/sse');
      eventSource.onmessage = (event) => {
        // Handle incoming SSE data
        console.log(event)
        
        const data = JSON.parse(event.data);
        const item = JSON.parse(data.data);
        item['id'] = cnt 
        cnt += 1 
        console.log(item)
        eventData = [...eventData, item];
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
    <h1>test</h1>
      <ul>
      {#each eventData as event (event.id)}
        <li>{JSON.stringify(event.data[0])}</li>
      {/each}
    </ul>
  </div>
