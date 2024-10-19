import mysql.connector

class conndb:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'sinhvien_ai'
    
    def queryResult(self, strsql):
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            conn = cnx.cursor()
            conn.execute(strsql)
            result = conn.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            conn.close()
            cnx.close()
    
    def queryExecute(self, strsql):
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            conn = cnx.cursor()
            conn.execute(strsql)
            cnx.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            conn.close()
            cnx.close()
