import sqlite3
import pandas as pd

class Data_Shop_CatsnDogs:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./db0.db")
        # self.conn2 = sqlite3.connect("./db1.db")
    def executeData(self, executeStr:str):
        cur = self.conn.cursor()
        try:
            cur.execute(executeStr)
            self.conn.commit()
            cur.close()
            return True
        except:
            cur.close()
            return False
        
    def queryAllDatas(self, queryStr:str) -> list:
        cur = self.conn.cursor()
        cur.execute(queryStr)
        data = cur.fetchall()
        cur.close()
        return data

    def queryManyDatas(self, queryStr, amount) -> list:
        cur = self.conn.cursor()
        cur.execute(queryStr)
        data = cur.fetchmany(amount)
        cur.close()
        return data

    def queryData(self, queryStr: str) -> object:
        cur = self.conn.cursor()
        cur.execute(queryStr)
        data = cur.fetchone()
        cur.close()
        return data

    def queryAllData(self) -> list:
        return self.queryManyDatas("select * from ShopData")