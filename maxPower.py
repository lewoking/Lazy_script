import pandas as pd  

from sqlalchemy import create_engine  

import cx_Oracle  

db=cx_Oracle.connect('userid','password','10.10.1.10:1521/dbinstance')  

print (db.version)  

cr=db.cursor()  

sql='select * from sys_user'  

cr.execute(sql)  

rs=cr.fetchall()  

zz=pd.DataFrame(rs);  

print (zz)  

db.close() 