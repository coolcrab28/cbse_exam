from uuid import uuid4
import mysql.connector as msc
import platform
import os

"""
Please include the 'modules' folder in the same directory as this file for the following functions to work...
"""

from modules.prettytable import  from_db_cursor

def clr():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')

db = msc.connect(
  host="localhost",
  user="root",
  password="1234" #change this
)

msg = """
choose an option:

[1] Show data
[2] Enter data
[3] Update an entry
[4] Delete an entry
[99999] Delete ALL data ⚠️

[0] Exit
"""

def tb(cursor):
    table = from_db_cursor(cursor)
    table._max_width = {"email": 10,"address": 10}
    table.hrules = True
    print(table)
def showData():
    cur.execute("SELECT * FROM __sms_table__")
    tb(cur)

def inputData():
    try:
        clr()
        uid = int(str(uuid4().int)[:5])
        print("Enter data")
        adm_no = int(input("Admission Number: "))
        name = input("Name: ")
        cls = int(input("Class: "))
        sec = input("Section: ")
        roll = int(input("Roll No: "))
        age = int(input("Age: "))
        address = input("Address: ")
        phone = input("Phone No: ")
        email = input("Email: ")
        if len(name)==0 or len(sec)==0 or len(address)==0 or len(phone)==0 or len(email)==0:
            clr()
            print("Please fill all the fields")
            raise(ValueError)
        else:
            cur.execute("INSERT INTO __sms_table__ VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", (uid,adm_no,name, cls, sec, roll, age, address, phone, email))
            db.commit()
        clr()
        print("Data entered successfully!")
    except:
        print("Error!")

def updateData():
    clr()
    print("""update using:

[1] UID
[2] Admission Number """)
    c = int(input("\n> "))
    if c == 1:
        uid = int(input("Enter UID: "))
        cur.execute("SELECT * FROM __sms_table__ WHERE uid=%s", (uid,))
        r = cur.fetchone();clr()
        print(f"current data: {r}\n")
        print("""Choose what to update:
        
[1] Name
[2] Class
[3] Section
[4] Roll No
[5] Age
[6] Address
[7] Phone No
[8] Email """)
        d = {1: "name", 2: "class", 3: "section", 4: "roll_no", 5: "age", 6: "address", 7: "phone_no", 8: "email"}	
        c = int(input("\n> "))
        print(f"Enter new value for {d[c]}: ",end="")
        n = input("")
        print(c,n)

        m = (f"UPDATE __sms_table__ SET {d[c]}=\"{n}\" WHERE uid={uid}")
        print(m)
        cur.execute(m)
        print("Data updated successfully!")	
        



def pre_main():  
    global cur
    cur = db.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS __sms_db__") 
    cur.execute("USE __sms_db__")
    cur.execute("CREATE TABLE IF NOT EXISTS \
    __sms_table__ (uid INT PRIMARY KEY,adm_no INT NOT NULL, name VARCHAR(255) NOT NULL,\
    class INT NOT NULL, section VARCHAR(2) NOT NULL, roll_no INT NOT NULL, age INT NOT NULL,\
    address VARCHAR(255) NOT NULL, phone_no VARCHAR(10) NOT NULL, email VARCHAR(255) NOT NULL)")
def main():
    pre_main()
    clr()
    print("Welcome to Student Management System")
    print("""
   _____ __  __  _____ 
  / ____|  \/  |/ ____|
 | (___ | \  / | (___  
  \___ \| |\/| |\___ \ 
  ____) | |  | |____) |
 |_____/|_|  |_|_____/ 
                       
              -- Lakshya Mahajan, XII-C, SLPS          """)
    x = True
    while x:
        print(msg)
        try:
            inp = int(input("\n> "))
            if inp == 0:
                x = False
                clr()
                print("Bye Bye! Thank you for using Student Management System\n")
                exit()
            elif inp == 1:
                clr()
                showData()
            elif inp == 2:
                inputData()
            elif inp == 3:
                clr()
                updateData()
            # elif inp == 4:
            #     clr()
            #     deleteData()
            # elif inp == 99999:
            #     clr()
            #     delAll()
            # else:
            #     raise ValueError
        except ValueError:
            clr()
            print("Invalid input!")
        except KeyboardInterrupt:
            clr()
            print("Bye Bye! Thank you for using Student Management System\n")
            exit()

if __name__ == '__main__':
    main()