import mysql.connector
import configparser
import os.path

class DBConnection():
    def __init__(self):
        config = configparser.ConfigParser()
        filename = r'app/config.properties'
        config.read(filename)
        dbhost = config.get('DatabaseSection', 'database.host')
        user = config.get('DatabaseSection','database.user')
        password = config.get('DatabaseSection','database.password')
        self.connection = mysql.connector.connect(host=dbhost,port="3306",user=user,password=password)
    
    def getConnection(self):
        return self.connection