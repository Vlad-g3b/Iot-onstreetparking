

<h1> Backend: </h1>
Setup:
   <ul>
    <li> use the dockerfile to create the container for the API endpoint which exposes the port 5000 with IP: 172.17.0.7 (after you create the image : docker run --name backend-fastapi -it -p 5000:5000 -v .:/app backendhub-app:latest </li>
    <li> in the config.properties you can put your own user,pass... for the connection to the database</li>
   </ul>
   This API exposes the following enpoints(work in progress):  
   <ul>
    <li> GET /getAllTrafficViolation = returns a json array of all the traffic violation registred in the database </li>
    <li> GET /sse = it is used to get data in realtime from the context broker </li>
    <li> POST /notify = recieves data and register it into the database </li>
    <li> see http://172.17.0.7:5000/docs for all of the endpoints exposed </li>
   </ul>
   How to install mysql into a docker container:
   <ul>
     <li> Use this link https://hub.docker.com/_/mysql</li>
     <li> Install MySql WorkBench https://dev.mysql.com/downloads/ (or use sqlplus ? from terminal) </li>
     <li> (better to) Create another user that will be put into the config.properties see this (https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql)</li>
     <li> It must have the address : 172.17.0.3 </li>
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
  
<h1>Orion Context Broker + MongoDB + cygnus</h1>
<ul>
<li>
sudo docker run --name mongodb -d mongo:4.4   
(it must have IP: 172.17.0.5)
</li>   
<li>   
sudo docker run -d --name orion1 --link mongodb:mongodb -p 1026:1026 fiware/orion -dbhost mongodb    
(it must have IP: 172.17.0.6)
</li>
<li>
docker run --name cygnus -p 8081:8081 -p 5050:5050 -e CYGNUS_MYSQL_HOST=172.17.0.3 -e CYGNUS_MYSQ_LUSER=root -e CYGNUS_MYSQL_PASS=password -e CYGNUS_LOGLEVEL='DEBUG' fiware/cygnus-ngsi
(it must have IP: 172.17.0.4)
</li>
</ul>

<h1>Frontend:</h1>
   <ul>
    <li> use the dockerfile to create the container for frontend which exposes the port 8082 with IP: 172.17.0.8   ( after your create the image : docker run --name frontend-app -it -p 8082:8082 -v .:/usr/src/app  svelte-image:latest )</li>
    <l1> http://172.17.0.8:8082/map </l1>
   </ul>
   <h1>AI:</h1>
   <ul>
      <li>
         put this https://drive.google.com/file/d/1JVP2z69kGyZJ6KqDb02bhA5DbRn1bf3R/view?usp=drive_link 
         into AiCarDetection/input
      </li>
      <li>
also you have install ultralytics, numpy,cv2
I used https://docs.ultralytics.com/quickstart/ I dont remember exactly how I made this to work on my pc :(
      </li>
   </ul>
![image](https://github.com/Vlad-g3b/Iot-onstreetparking/assets/61354498/81de87bb-9117-4506-891c-f4d5373f34dc)
