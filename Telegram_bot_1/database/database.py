import psycopg2
from database.config import HOST, USER, PASSWORD, DB_NAME, PORT
# from config import HOST, USER, PASSWORD, DB_NAME, PORT


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
                contact_phone VARCHAR(25),
                users_tg_id VARCHAR(25),
                services_id INTEGER
                );
        ''')

    # Стандартное расписание
    @connecting_to_the_database
    def create_table_schedule(connection, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule(
                id SERIAL PRIMARY KEY,
                day_of_the_week SMALLINT,
                start_time TIME,
                end_time TIME
                );
        ''')

    # Изменения в расписании
    @connecting_to_the_database
    def create_table_schedule_changes(connection, cursor):
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedule_changes(
                    id SERIAL PRIMARY KEY,
                    start_date DATE,
                    end_date DATE,
                    is_it_a_working_day SMALLINT
                );
            ''')

    def __init__(self):
        self.create_table_services()
        self.create_table_appointments()
        self.create_table_schedule()
        self.create_table_schedule_changes()

    @connecting_to_the_database
    def services_add(connection, cursor, *args):
        cursor.execute(f"""
                    INSERT INTO services
                    (name, duration, description)
                    VALUES(%s, %s, %s)""", args
                       )

    @connecting_to_the_database
    def services_get_names(connection, cursor):
        cursor.execute('SELECT id, name FROM services')
        res = cursor.fetchall()
        return res
        # return [val[0] for val in res]

    @connecting_to_the_database
    def appointment_add(connection, cursor, *args):
        cursor.execute(f"""INSERT INTO appointments
                    (full_name, appointment_time, contact_phone, users_tg_id, services_id)
                    VALUES(%s, %s, %s, %s, %s);""", args)

    @connecting_to_the_database
    def schedule_get(connection, cursor):
        cursor.execute('SELECT * FROM schedule')
        return cursor.fetchall()

    @connecting_to_the_database
    def schedule_set_s(connection, cursor, *args):
        cursor.execute('UPDATE schedule SET start_time = %s WHERE day_of_the_week = %s', args)


    @connecting_to_the_database
    def schedule_set_f(connection, cursor, *args):
        cursor.execute('UPDATE schedule SET end_time = %s WHERE day_of_the_week = %s', args)


# '''************************************ schedule of changes *************************************'''
    @connecting_to_the_database
    def schedule_changes_add(connection, cursor, *args):
        # is_it_a_working_day - 0=no, 1=yes, 2=work outside the schedule
        cursor.execute(f"""
                    INSERT INTO schedule_changes
                    (start_date, end_date, is_it_a_working_day)
                    VALUES(%s, %s, %s)""", args
                       )




dataBase = DataBase()
# dataBase.services_add('Что-то еще', '2:00', 'Some description')
# dataBase.appointment_add('Ramzan Ahmatovich', '1:15', '89242194144', 9999, 1111)
# dataBase.schedule_changes_add('2023-12-30', '2023-12-30', '13:00', '14:00')
print(dataBase.schedule_get())
