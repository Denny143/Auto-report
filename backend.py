import sqlite3
from bs4 import BeautifulSoup
import re
import sys,io

class Database:

    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS cabinets (id INTEGER PRIMARY KEY, Cabinet_type TEXT, Dimension TEXT, Product_ID TEXT, Brand TEXT )")
        self.conn.commit()


    def insert(self,Cabinet_type,Dimension,Product_ID,Brand):
        self.cur.execute("INSERT INTO cabinets VALUES (NULL,?,?,?,?)",(Cabinet_type,Dimension,Product_ID,Brand))
        self.conn.commit()


    def view(self):
        self.cur.execute("SELECT * FROM cabinets")
        rows=self.cur.fetchall()
        return rows

    def search(self,Cabinet_type="",Dimension="",Product_ID="",Brand=""):
        self.cur.execute("SELECT * FROM cabinets WHERE Cabinet_type=? OR Dimension=? OR Product_ID=? OR Brand=?", (Cabinet_type,Dimension,Product_ID,Brand))
        rows=self.cur.fetchall()
        return rows

    def delete(self,id):

        self.cur.execute("DELETE FROM cabinets WHERE id=?",(id,))
        self.conn.commit()


    def update(self,id,Cabinet_type,Dimension,Product_ID,Brand):
        self.cur.execute("UPDATE cabinets SET Cabinet_type=?,Dimension=?,Product_ID=?,Brand=? WHERE id=?",(Cabinet_type,Dimension,Product_ID,Brand,id))
        self.conn.commit()

    def report(self):
        self.cur.execute("SELECT * FROM cabinets")
        row=self.cur.fetchone()
        rows=[]
        while row is not None:
            i=row[3]

            with open("Ikea.html") as fp:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')
                soup = BeautifulSoup(fp,"html.parser")

            SAD=soup.find_all(string=re.compile(str(i)))
            rows +=[("There","are",len(SAD),row[1],"cabinets")]
            row = self.cur.fetchone()

        return rows

    def __del__(self):
        self.conn.close()
