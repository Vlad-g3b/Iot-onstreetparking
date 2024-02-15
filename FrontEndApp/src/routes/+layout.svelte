<script>
    import "./styles.css"
    import { SvelteToast } from '@zerodevx/svelte-toast'
</script>

<style>
  :root {
    --sidebar-width: 250px;
    --sidebar-bg-color: #333;
    --sidebar-text-color: #fff;
    --content-bg-color: #f9f9f9;
    --content-text-color: #333;
    --link-hover-color: #ccc;
    --transition-speed: 0.6s;
  }

  .container {
    display: flex;
    height: 100vh;
  }

  .sidebar {
    width: var(--sidebar-width);
    background-color: var(--sidebar-bg-color);
    color: var(--sidebar-text-color);
    padding: 20px;
  }
  .footer {
    background-color: var(--sidebar-bg-color);
    color: var(--sidebar-text-color);
    padding: 20px;
  }
  .sidebar h2 {
    margin-bottom: 20px;
  }

  .sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .sidebar li {
    margin-bottom: 10px;
  }

  .sidebar a {
    display: block;
    padding: 10px;
    color: inherit;
    text-decoration: none;
    transition: color var(--transition-speed);
  }

  .sidebar a:hover {
    background-color: var(--link-hover-color);
  }

  .content {
    flex: 1;
    background-color: var(--content-bg-color);
    color: var(--content-text-color);
    padding: 20px;
    transition: margin-left var(--transition-speed);
    overflow: auto;
  }

  @media screen and (max-width: 768px) {
    .container {
      flex-direction: column;
    }

    .sidebar {
      width: 100%;
      text-align: center;
    }

    .content {
      margin-top: 20px;
    }
  }
</style>
<SvelteToast />
<div class="container">
  <!-- Sidebar -->
  <div class="sidebar">
    <h2>Navigation</h2>
    <ul>
      <li><a href="/map">Live map</a></li>
      <li><a href="/live_feed">Live Feed</a></li>
      <li><a href="/tf_list">Traffic Violations</a></li>
      <li><a href="/ps_list">Parking Sites</a></li>
      <li><a href="/statistics">Statistics</a></li>

    </ul>
  </div>

  <!-- Main content area -->
  <div class="content">
    <slot></slot>
  </div>
</div>
  
<footer class="footer">
  <p>&copy; 2022 OnStreetParking. All rights reserved.</p>
</footer>