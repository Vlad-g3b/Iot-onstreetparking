<h1> Backend: </h1>
Setup:
   <ul>
    <li> use the dockerfile to create the container for the API endpoint which exposes the port 5000 </li>
    <li> in the config.properties you can put your own user,pass... for the connection to the database</li>
   </ul>
   This API exposes the following enpoints(work in progress):  
   <ul>
    <li> GET /getAllTrafficViolation = returns a json array of all the traffic violation registred in the database </li>
    <li> GET /sse = it is used to get data in realtime from the context broker </li>
    <li> POST /notify = recieves data and register it into the database </li>
   </ul>
   How to install mysql into a docker container:
   <ul>
     <li> Use this link https://hub.docker.com/_/mysql</li>
     <li> Install MySql WorkBench https://dev.mysql.com/downloads/ (or use sqlplus ? from terminal) </li>
     <li> (better to) Create another user that will be put into the config.properties see this (https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql)</li>
   </ul>
   How to import the sql file for workbench :
   <ul>
     <li> Under Server Administration on the Home window select the server instance you want to restore database to (Create New Server Instance if doing it first time).</li>
     <li> Click on Manage Import/Export</li>
     <li> Click on Data Import/Restore on the left side of the screen.</li>
     <li> Select Import from Self-Contained File radio button (right side of screen)</li>
     <li> Select the path of .sql</li>
     <li> Click Start Import button at the right bottom corner of window.</li>
  </ul>
