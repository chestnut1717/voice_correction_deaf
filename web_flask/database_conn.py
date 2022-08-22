
import pymysql


host = "betterdatabase.cyooqkxaxvqu.us-east-1.rds.amazonaws.com"
username = "admin"
password = "jung0204"
port = 3306
database = "better"

db = pymysql.connect(
                    host=host, 
                    port=port, 
                    user=username, passwd=password, 
                    db=database, charset='utf8'
                    )
print(db)

sql = "SELECT * FROM better_qa"

with db:
    with db.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
        for data in result:
            print(data)
