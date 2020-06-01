import sys
import asyncio
import concurrent
# import aioschedule as schedule
import schedule
import time
import psycopg2
import pandas
from myform import Ui_Form
from loguru import logger
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import (
    QApplication, QWidget)
from PyQt5 import uic


class MainWindow(QWidget):
    """Main window."""

    def __init__(self):
        super().__init__()
        uic.loadUi('myform.ui', self)
        self.show()

        self.ip_address = "192.168.1.33"
        self.ip_port = "5000"
        self.db_user = "postgres"
        self.db_dom = "AquaPiDB"
        self.db_pass = "aquaPi"
        self.server_ip = f"http://{self.ip_address}:{self.ip_port}"  # here
        self.df = None
        try:
            self.central = QtWidgets.QWidget()
            self.form = Ui_Form()
            self.form.setupUi(self.central)
        except:
            logger.exception("Couldn't Load Ui File")

        self.db = self.sql_connection()

        self.last_id = 1

        # Schedule tasks here
        schedule.every().second.do(self.temperature_displays)
        #schedule.every().second.do(self.graph_display)

    def temperature_displays(self):
        logger.info("=" * 125)
        logger.info("temp_display: Entered".center(125))
        try:
            self.df = self.tank_db()
            if self.df is not None:

                logger.debug(f"{self.df}")
                c = self.df['temperature_c'].iat[-1]
                f = self.df['temperature_f'].iat[-1]
                self.form.tank_display_c.display(c)
                self.form.tank_display_f.display(f)
                logger.debug(f"°C: {c}")
                logger.debug(f"°F: {f}")
            else:
                logger.warning("df empty")
        except:
            logger.exception("temp_display: Failed")
        finally:
            logger.info("temp_display: Exited".center(125))
            logger.info("=" * 125)

    def sql_connection(self):
        logger.info("=" * 125)
        logger.info("sql_connection: Entered".center(125))
        try:
            connection = psycopg2.connect(
                host=self.ip_address,
                dbname=self.db_dom,
                user=self.db_user,
                password=self.db_pass
            )
            logger.debug(connection)
            #logger.debug(connection.cursor().execute('SELECT * FROM tank_temperature;').fetchone())
            logger.debug("Connection is established: Database has been created ")
            return connection
        except Error:
            logger.exception(Error)
        finally:
            logger.info("sql_connection: Exited".center(125))
            logger.info("=" * 125)

    def tank_db(self):
        logger.info("=" * 125)
        logger.info("tank_db: Entered".center(125))
        try:
            #cursor = self.sql_connection()
            with self.db.cursor() as cur:
              cur.execute(f'SELECT * FROM tank_temperature WHERE id > {self.last_id};')
              rows = cur.fetchall()

              if rows:
                self.last_id = rows[-1][0]
                df = pandas.DataFrame(rows, columns=['id', 'date', 'temperature_c', 'temperature_f'])
                return df

            """if self.df is not None:
                logger.debug("df already loaded, updating df")
                last_id = self.df['id'][:1]
                logger.debug(f"DB still in Memory, last row id := {last_id}")
                updated_df = self.db_cursor.execute(f'SELECT * FROM tank_temperature WHERE id > {last_id}')
                logger.success(f"New DB Data Received: {updated_df}")
                return updated_df
            else:
                logger.debug("No DB Data Loaded")
                logger.debug(rows)

                df = pandas.DataFrame(rows, columns=['id', 'date', 'temperature_c', 'temperature_f'])
                logger.debug(f"Loading Entire DB:"
                             f"{self.df}")"""
                #return df
        except:
            logger.exception("tank_db Error")
        finally:
            logger.info("tank_db: Exited".center(125))
            logger.info("=" * 125)

    def graph_display(self):
        logger.info("=" * 125)
        logger.info("graph_display: Entered".center(125))
        try:
            df = self.tank_db()
            y = df['temperature_c'].to_numpy(dtype=float)
            x = df['date']
            x = [t.timestamp() for t in self.x]
            x = [round(t) for t in self.x]
            plot.plot().setData(x, y)
        except:
            logger.exception("oops")
        finally:
            logger.info("graph_display: Exited".center(125))
            logger.info("=" * 125)


def gui():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


def scheduler():
    # Recheck schedule every second
    while True:
        schedule.run_pending()
        time.sleep(1)


async def start(executor):
    loop = asyncio.get_event_loop()

    # Add sync functions here
    blocking_tasks = [
        loop.run_in_executor(executor, gui),
        loop.run_in_executor(executor, scheduler)
    ]
    completed, pending = await asyncio.wait(blocking_tasks, return_when=asyncio.FIRST_EXCEPTION)


if __name__ == '__main__':
    # Create a limited thread pool.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=3,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            start(executor)
        )
    finally:
        event_loop.close()
