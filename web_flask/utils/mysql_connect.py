import pymysql

class mysql_connect():
    def __init__(self, user = 'admin', password = "jung0204",
    host='betterdatabase.cyooqkxaxvqu.us-east-1.rds.amazonaws.com',
    port = 3306, database = 'better'):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.log = ""
        try:
            self.db = pymysql.connect(host = self.host, port = self.port,
            user = self.user, passwd = self.password,
            db = self.database, charset='utf8')
            self.connect = True
        except Exception as e:
            self.connect = False
            self.log = e
        self.cursor = self.db.cursor()

    def __del__(self):
        print("deleted")
        self.db.close()

    def querry(self, sql):
        try:
            with self.cursor as cursor:
                cursor.execute(sql)
                return True, cursor
        except Exception as e:
            return False, e

    def get_items_list(self, sql):
        ch, cursor = self.querry(sql)
        if ch:
            fetch = cursor.fetchone()
            result = [fetch]
            while fetch:
                fetch = cursor.fetchone()
                result.append(fetch)
            self.cursor = cursor
            return result
        else:
            return cursor

    def send_wav(self, idx, wav):
        print(self.querry(
            'insert into better_wave(waveid, wave_data) values("{}", "{}")'.format(idx, wav)
        ))
        self.db.commit()

    def get_wav_idx(self):
        # idx = self.get_items_list('select max(waveid) from better_wave')
        idx = self.get_items_list('select max(waveid) from better_wave')

        return idx

    def get_wav(self):
        sql = "SELECT wave_data FROM better_wave WHERE waveid = (SELECT max(waveid) FROM better_wave);"
        wav = eval(self.get_items_list(sql)[0][0])

        return wav

if __name__ == "__main__":
    conn = mysql_connect()
    a = conn.get_wav()
    import numpy as np
    print(eval(a)[:10], type(a))
    a_np = np.array(a)
    print(a_np.shape)