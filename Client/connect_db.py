import psycopg2

ip_address = '192.168.1.33'
db_dom = 'AquaPiDB'
db_user = 'postgres'
db_pass = 'aquaPi'

connection = psycopg2.connect(
    host=ip_address,
    dbname=db_dom,
    user=db_user,
    password=db_pass
)

cursor = connection.cursor()

cursor.execute('SELECT * FROM tank_temperature;')
rows = cursor.fetchall()
print(len(rows))
