import mysql.connector
import json

class info_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="Sid@3435",database="urbandb")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection successful")
        except:
            print("Connection failed")
    
    def info_getall_package(self):
        self.cur.execute("SELECT * FROM package")
        getall_data=[dict(x) for x in self.cur.fetchall()]
        if len(getall_data) > 0:
            return getall_data
        else:
            return {"getall_data":"No data found"}