import sqlite3

con = sqlite3.connect('studentData.db')
print ("Database Created")

con.execute('create table student(studid integer primary key autoincrement,name text,age number,email text,place text,username text,password text,status text default "No" NOT NULL,teacher text default "No" NOT NULL,admin text default "No" NOT NULL)')
print("Table Created")