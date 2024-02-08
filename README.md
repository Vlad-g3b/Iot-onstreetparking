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
     <li>  Use this link https://hub.docker.com/_/mysql</li>
     <li>  Install MySql WorkBench https://dev.mysql.com/downloads/ (or use sqlplus ? from terminal) </li>
     <li>  (better to) Create another user that will be put into the config.properties see this (https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql)</li>
  </ul>
