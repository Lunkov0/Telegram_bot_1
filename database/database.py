import psycopg2
from config import HOST, USER, PASSWORD, DB_NAME, PORT


'''Для работы с Postgres создан класс DataBase
Создаем таблицы:
    services - список предоставляемых услуг
    appointments - список записей на прием
    
Декоратор connecting_to_the_database используется для подключения и отключения от БД

Реализованны функции:
    add_service - добавить услугу
    add_appointment - добавить запись
    '''
class DataBase:
    def connecting_to_the_database(func):
        def wrapper(*args):
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DB_NAME)
            connection.autocommit = True
            cursor = connection.cursor()

            res = func(connection, cursor, *args[1:])

            connection.close()

            return res
        return wrapper

    @connecting_to_the_database
    def create_table_services(connection, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                duration TIME,
                description VARCHAR(400)
                );
        ''')

    @connecting_to_the_database
    def create_table_appointments(connection, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments(
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(50),
                appointment_time TIME,
                contact_phone VARCHAR(15),
                users_tg_id VARCHAR(21),
                services_id INTEGER
                );
        ''')

    def __init__(self):
        self.create_table_services()
        self.create_table_appointments()

    @connecting_to_the_database
    def services_add(connection, cursor, *args):
        cursor.execute(f"""
                    INSERT INTO services
                    (name, duration, description)
                    VALUES(%s, %s, %s)""", args
                       )

    @connecting_to_the_database
    def services_get_names(connection, cursor):
        cursor.execute('SELECT name FROM services')
        res = cursor.fetchall()
        return res

    @connecting_to_the_database
    def appointment_add(connection, cursor, *args):
        cursor.execute(f"""INSERT INTO appointments
                    (full_name, appointment_time, contact_phone, users_tg_id, services_id)
                    VALUES(%s, %s, %s, %s, %s);""", args)


q = DataBase()
# q.add_service('Artem', '2:00', 'Some description')
# q.add_appointment('qqqqq', '1:15', '89242194144', 9999, 1111)
print(q.services_get_names())
