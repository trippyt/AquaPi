import sqlite3
from sqlite3 import Error
from loguru import logger
from datetime import datetime
import random

currentDate = datetime.now()
currentTime = datetime.now()
currentTemperature = round(random.random(), 2)


def sql_connection():
    try:
        con = sqlite3.connect('AquaPiDB.db')
        logger.debug("Connection is established: Database has been created ")
        return con
    except Error:
        logger.exception(Error)
    #finally:
        #con.close()


def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE tank_temperature(date datetime, time datetime, temperature_c float,"
                      " temperature_f float)")
    con.commit()


def sql_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute(
        '''INSERT INTO tank_temperature VALUES(?, ?, ?, ?)''', entities)
    con.commit()


def sql_update(con):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE tank_temperature')


entities = (currentDate.strftime("%d-%m-%y"), currentTime.strftime("%H:%M:%S"), currentTemperature, currentTemperature)
con = sql_connection()
#sql_table(con)
sql_insert(con, entities)



