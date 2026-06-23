import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname="Modul4+",
            port="5432",
            password="1234",
            user="postgres",
            host="localhost",
        )
        return conn
    except psycopg2.Error as e:
        print(e)
        return None