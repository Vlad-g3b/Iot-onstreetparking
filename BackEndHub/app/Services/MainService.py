from app.Helper.DBConnection import DBConnection
import logging

#This should've call another script that handle the DB querys...
class MainService():


    def __init__(self):
        self.data = None
        self.tableName = 'TrafficViolation'
        self.database = 'OnStreetParking'
        
    
    def insertTrafficViolation(self, tf_id, tf_desc, tf_location, tf_ref):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                tf_ref = tf_ref.replace('"','')
                cursor.execute(f"Insert into {self.database}.{self.tableName} (tf_id, tf_desc, tf_location, tf_ref_parksite) values ('{tf_id}','{tf_desc}','{tf_location}','{tf_ref}') ")
                print(cursor.rowcount, "record inserted.")                
            connection.commit()

    def getTrafficViolationList(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select * from {self.database}.{self.tableName} ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList