<script >
  import { onMount } from 'svelte';

  let videoStreamSrc = "http://150.140.186.118:1111/";
  const refreshRate = 1000; // Refresh rate in milliseconds

  function refreshImage() {
      fetch(videoStreamSrc)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response;
        })
        .then(() => {
          videoStreamSrc = "http://150.140.186.118:1111/?" + new Date().getTime();
        })
        .catch(error => {
          console.error('Error fetching image:', error);
        });
  }

  onMount(() => {
      const refreshInterval = setInterval(refreshImage, refreshRate);
      return () => clearInterval(refreshInterval); // Cleanup on component unmount
  });
</script>
<h1>Camera</h1>
<img src={videoStreamSrc} alt="Video Stream">
