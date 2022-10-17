
from XueXi import app


class accessdb(object):
    """description of class"""
    
    def __init__(self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"

    @staticmethod
    def get_data(dbname):
        result=[];

        import pyodbc   
        DBfile =app.config.get("DB")  # 数据库文件需要带路径
        print(DBfile)
        conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+ DBfile +";Uid=;Pwd=;") 


        cursor = conn.cursor() 
        SQL = "SELECT * from "+dbname;
        cursor.execute(SQL)
        data=cursor.fetchall();
        column_names=[column[0] for column in cursor.description]

        myrows=1
        for row in data:
            result.append(dict(zip(column_names,row)))  
            #if myrows>2:
            #    break
            myrows=myrows+1
            #for row in cursor.execute(sql): 
        # print(row) 
        cursor.close() 
        conn.close()
        return result
    

    @staticmethod
    def sql_data(SQL):
        result=[];

        import pyodbc   
        DBfile =app.config.get("DB")  # 数据库文件需要带路径
        print(DBfile)
        conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+ DBfile +";Uid=;Pwd=;") 

        
        cursor = conn.cursor() 
        cursor.execute(SQL)
        data=cursor.fetchall();
        column_names=[column[0] for column in cursor.description]

        myrows=1
        for row in data:
            result.append(dict(zip(column_names,row)))  
            #if myrows>2:
            #    break
            myrows=myrows+1
            #for row in cursor.execute(sql): 
        # print(row) 
        cursor.close() 
        conn.close()
        return result
    
    @staticmethod
    def sql_nodata(SQL,*para):
        result=[];

        import pyodbc   
        DBfile =app.config.get("DB")  # 数据库文件需要带路径
        print(DBfile)
        conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+ DBfile +";Uid=;Pwd=;") 

        
        cursor = conn.cursor() 
        cursor.execute(SQL,para)
        conn.commit()
        cursor.close() 
        conn.close()
        return result
