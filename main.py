from secret import *
from context import * 
from telebot import *
from telebot.types import ReplyKeyboardMarkup

create_db_cars()

@bot.message_handler(commands=['start','help'])
def welcome(message):
    btn1 = types.InlineKeyboardButton("add")
    btn2 = types.InlineKeyboardButton("get")
    btn3 = types.InlineKeyboardButton("get all")
    btn4 = types.InlineKeyboardButton("update")
    btn5 = types.InlineKeyboardButton("delete")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(btn1)
    markup.row(btn2,btn3)
    markup.row(btn4,btn5)
    bot.send_message(message.chat.id, "Welcome to cars bot", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handler(message):
    if message.text == "add":
        bot.send_message(message.chat.id, "Enter car mark: ")
        bot.register_next_step_handler(message, ask_company)
    elif message.text == "get":
        bot.send_message(message.chat.id, "enter car number to get: ")
        bot.register_next_step_handler(message,get_car)
    elif message.text == "get all":
        bot.send_message(message.chat.id, "Enter company to show: ")
        bot.register_next_step_handler(message,get_all)
    elif message.text == "update":
        bot.send_message(message.chat.id,"Enter car number to update: ")
        bot.register_next_step_handler(message,old_number)
    elif message.text == "delete":
        bot.send_message(message.chat.id, "Enter car number to delete it: ")
        bot.register_next_step_handler(message,delete)

# deleting
def delete(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f""" delete from cars where number = '{message.text}' """)
    conn.commit()
    close_connection(conn,cur)
    bot.send_message(message.chat.id, "deleted successfuly!")
# ----

# updating
def old_number(message):
    global old
    old = message.text
    bot.send_message(message.chat.id, "Enter new number: ")
    bot.register_next_step_handler(message,update)

def update(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f""" 
update cars
set number = '{message.text}' where number = '{old}' """)
    conn.commit()
    close_connection(conn,cur)
    bot.send_message(message.chat.id, "updated successfuly!")
# --


# all
def get_all(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f"select * from cars where company = '{message.text}'")
    cars = cur.fetchall()
    bot.send_message(message.chat.id, str(cars))
    close_connection(conn,cur)
# --

# geeting 
def get_car(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f"select * from cars where number = '{message.text}'")
    car = cur.fetchone()
    bot.send_message(message.chat.id, str(car))
    close_connection(conn,cur)
# ---

# adding
def ask_company(message):
    car_name = message.text
    bot.send_message(message.chat.id, "Enter car company: ")
    bot.register_next_step_handler(message, lambda msg: ask_number(msg, car_name))

def ask_number(message, car_name):
    car_company = message.text
    bot.send_message(message.chat.id, "Enter car number: ")
    bot.register_next_step_handler(message, lambda msg: add_car(msg, car_name, car_company))

def add_car(message, car_name, car_company):
    car_number = message.text
    conn = connection_open()
    cur = conn.cursor()
    cur.execute("INSERT INTO cars (name, company, number) VALUES (%s, %s, %s)", (car_name, car_company, car_number))
    conn.commit()
    close_connection(conn,cur)
    
    bot.send_message(message.chat.id, "Car details have been added successfully!")
# --


bot.infinity_polling()