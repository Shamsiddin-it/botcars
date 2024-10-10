import psycopg2
from secret import *
import telebot

def connection_open():
    conn = psycopg2.connect(
        database = "bot",
        host = 'localhost',
        user = "postgres",
        password = password1,
        port = 5432
    )
    return conn

def close_connection(conn,cur):
    cur.close()
    conn.close()


def create_db_cars():
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(
        """
        create table if not exists cars(
        car_id serial primary key,
        name varchar(100),
        company varchar(100),
        number varchar(10),
        price numeric(10,2)
        );
        """
    )
    conn.commit()
    close_connection(conn,cur)


bot = telebot.TeleBot(API_KEY,parse_mode=None)

