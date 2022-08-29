import pymysql
import random

def load_context():
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
    rdm = random.randint(1, 10)

    sql = f"SELECT * FROM better_context_qa where better_context_qa.context_qa_id =  {rdm}"
    with db:
        with db.cursor() as cur:
            cur.execute(sql)
            result_sql = cur.fetchall()[0]

           
    context, question, answer = result_sql[1], result_sql[2], result_sql[3]

    return context, question, answer