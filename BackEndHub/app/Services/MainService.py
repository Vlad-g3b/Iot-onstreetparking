from app.Helper.DBConnection import DBConnection
import logging

#This should've call another script that handle the DB querys...
class MainService():


    def __init__(self):
        self.data = None
        self.tableNameTF = 'TrafficViolation'
        self.tableNamePS = 'ParkingSite'
        self.database = 'OnStreetParking'
 
 ######################
 #      Insert        #
 ######################
 
    def insertTrafficViolation(self, tf_id, tf_desc, tf_location, tf_ref):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                tf_ref = tf_ref.replace('"','')
                cursor.execute(f"Insert into {self.database}.{self.tableNameTF} (tf_id, tf_desc, tf_location, tf_ref_parksite) values ('{tf_id}','{tf_desc}','{tf_location}','{tf_ref}') ")
                print(cursor.rowcount, "record inserted.")                
            connection.commit()

    def insertOnStreetParking(self,idd,desc,location,max_ps):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Insert into {self.database}.{self.tableNamePS} (ps_id, ps_description, ps_location, ps_max_parking_spots) values ('{idd}','{desc}','{location}','{max_ps}') ")
                print(cursor.rowcount, "record inserted.")                
            connection.commit()

 ######################
 #      Get           #
 ######################

    def getTrafficViolationById(self, tf_id):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved from {self.database}.{self.tableNameTF} where tf_id= '{tf_id}' ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList[0]
 
    def getTrafficViolationStats(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT tf_ref_parksite, count(*) FROM {self.database}.{self.tableNameTF} group by tf_ref_parksite ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList

    def getTrafficViolationList(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved from {self.database}.{self.tableNameTF} order by tf_resolved asc, tf_date_resolved desc")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList
    
    def getTrafficViolationListUnresolved(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved from {self.database}.{self.tableNameTF} where tf_resolved = 0 order by tf_resolved asc")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList
           
    def getTrafficViolationListByPsId(self, ps_id):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved from {self.database}.{self.tableNameTF} where tf_ref_parksite = '{ps_id}' ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList
     
    def getParkingSiteList(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select ps_id, ps_description, ps_location, ps_max_parking_spots from {self.database}.{self.tableNamePS} ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList
        
    def getParkingSiteById(self, ps_id):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select ps_id, ps_description, ps_location, ps_max_parking_spots from {self.database}.{self.tableNamePS} where ps_id = '{ps_id}' ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList[0]
    
    
 ######################
 #      Update        #
 ######################
    
    def updateTFResolved(self, tf_id,tf_resolved):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"update {self.database}.{self.tableNameTF} set tf_resolved = {tf_resolved}, tf_date_resolved = now() where tf_id = '{tf_id}' ")
                print(cursor.rowcount, "records")                
            connection.commit()
