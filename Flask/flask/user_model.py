import mysql.connector
import json

class user_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host="localhost",user="root",password="Sid@3435",database="flask")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection successful")
        except:
            print("Connection error")
    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        
        result=self.cur.fetchall()
        if len(result) > 0:
            return json.dumps(result)
        else:
            return "No Data found"
        return "This is user_signup_model"
    
    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, role, password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}')")
        return "This is addone controller"

    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role']}',password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount > 0:
            return "User updated Successfully"
        else:
            return "Nothing to update"
    
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount > 0:
            return "User deleted Successfully"
        else:
            return "Nothing to delete"