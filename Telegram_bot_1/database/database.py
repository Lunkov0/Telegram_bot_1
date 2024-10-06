import psycopg2
from database.config import HOST, USER, PASSWORD, DB_NAME, PORT


class DataBase:
    '''Для работы с Postgres создан класс DataBase
    Создаем таблицы:
        treatments - список предоставляемых услуг
        appointments - список записей на прием
        schedule - основное расписание
        schedule_changes - изменения в расписании
    Декоратор connecting_to_the_database используется для подключения и отключения от БД'''
    @staticmethod
    def connecting_to_the_database(func):
        def wrapper(*args):
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DB_NAME)
            connection.autocommit = True
            cursor = connection.cursor()

            res = func(cursor, *args)

            connection.close()

            return res
        return wrapper

    @staticmethod
    @connecting_to_the_database
    def create_table_treatments(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatments(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                duration TIME,
                price INTEGER,
                description VARCHAR(400)
                );
        ''')

    @staticmethod
    @connecting_to_the_database
    def create_table_appointments(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments(
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(50),
                appointment_time TIMESTAMP,
                contact_phone VARCHAR(25),
                users_tg_id INTEGER,
                services_id INTEGER
                );
        ''')

    # Стандартное расписание
    @staticmethod
    @connecting_to_the_database
    def create_table_schedule(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule(
                id SERIAL PRIMARY KEY,
                day_of_the_week SMALLINT,
                start_time TIME,
                end_time TIME
                );
        ''')

    # Изменения в расписании
    @staticmethod
    @connecting_to_the_database
    def create_table_schedule_changes(cursor):
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedule_changes(
                    id SERIAL PRIMARY KEY,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    is_it_a_working_day SMALLINT
                );
            ''')

    @staticmethod
    @connecting_to_the_database
    def create_table_constant_breaks(cursor):
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS constant_breaks(
                    start_time TIME,
                    end_time TIME
                );
            ''')

    def __init__(self):
        self.create_table_treatments()
        self.create_table_appointments()
        self.create_table_schedule()
        self.create_table_schedule_changes()
        self.create_table_constant_breaks()

    @staticmethod
    @connecting_to_the_database
    def add_treatment(cursor, *args):
        cursor.execute(f"""
                    INSERT INTO treatments
                    (name, duration, price, description)
                    VALUES(%s, %s, %s, %s)""", *args
                       )


    @staticmethod
    @connecting_to_the_database
    def get_all_treatments(cursor):
        cursor.execute('SELECT * FROM treatments')
        res = cursor.fetchall()
        return res


    @staticmethod
    @connecting_to_the_database
    def treatments_get_names(cursor):
        cursor.execute('SELECT id, name FROM treatments')
        res = cursor.fetchall()
        return res


    @staticmethod
    @connecting_to_the_database
    def del_treatment(cursor, *args):
        cursor.execute(f"""
                    DELETE FROM treatments
                    WHERE name=%s""", args
                       )


    @staticmethod
    @connecting_to_the_database
    def get_treatment_id(cursor, *args):
        cursor.execute(f"""
                    SELECT id 
                    FROM treatments
                    WHERE name = %s;
                    """, args)
        return cursor.fetchone()


    @staticmethod
    @connecting_to_the_database
    def get_treatment_duration(cursor, name):
        cursor.execute(f'''
            SELECT duration
            FROM treatments
            WHERE name = %s
        ''', (name,))
        return cursor.fetchone()


    @staticmethod
    @connecting_to_the_database
    def get_treatment_name(cursor, id):
        cursor.execute(f'''
            SELECT name
            FROM treatments
            WHERE id = %s
        ''', (id,))
        return cursor.fetchone()


    @staticmethod
    @connecting_to_the_database
    def get_treatment_duration_by_id(cursor, id):
        cursor.execute(f'''
            SELECT duration
            FROM treatments
            WHERE id = %s
        ''', (id,))
        return cursor.fetchone()


    @staticmethod
    @connecting_to_the_database
    def add_appointment(cursor, *args):
        cursor.execute(f"""INSERT INTO appointments
                    (full_name, appointment_time, contact_phone, users_tg_id, services_id)
                    VALUES(%s, %s, %s, %s, %s)""", *args)

    @staticmethod
    @connecting_to_the_database
    def get_my_appointments(cursor, *args):
        cursor.execute(f'''SELECT *
                           FROM appointments
                           WHERE users_tg_id = %s
                           AND appointment_time > now()''', args)
        return cursor.fetchall()


    @staticmethod
    @connecting_to_the_database
    def get_all_appointments(cursor):
        cursor.execute(f'''SELECT *
                        FROM appointments
                        WHERE appointment_time > now()''')
        return cursor.fetchall()


    @staticmethod
    @connecting_to_the_database
    def del_appointment(cursor, *args):
        cursor.execute(f"""
                    DELETE FROM appointments
                    WHERE users_tg_id = %s""", args)

    @staticmethod
    @connecting_to_the_database
    def del_treatment(cursor, *args):
        cursor.execute(f"""
                    DELETE FROM treatments
                    WHERE name=%s""", args
                       )

    @staticmethod
    @connecting_to_the_database
    def schedule_get(cursor):
        cursor.execute('SELECT * FROM schedule')
        return cursor.fetchall()

    @staticmethod
    @connecting_to_the_database
    def get_weekday_schedule(cursor, *args):
        cursor.execute('''SELECT start_time, end_time FROM schedule
                       WHERE day_of_the_week = %s''', args)
        return cursor.fetchall()

    @staticmethod
    @connecting_to_the_database
    def schedule_set_s(cursor, *args):
        cursor.execute('UPDATE schedule '
                       'SET start_time = %s '
                       'WHERE day_of_the_week = %s', args)

    @staticmethod
    @connecting_to_the_database
    def schedule_set_f(cursor, *args):
        cursor.execute('UPDATE schedule '
                       'SET end_time = %s '
                       'WHERE day_of_the_week = %s', args)


# '''************************************ schedule of changes *************************************'''
    @staticmethod
    @connecting_to_the_database
    def get_all_schedule_changes(cursor):
        cursor.execute(f"""
                        SELECT * FROM schedule_changes
                        WHERE start_date > now()
                        ORDER BY start_date ASC
                        """)
        return cursor.fetchall()


    # Добавляет данные если такого кортежа еще нет
    @staticmethod
    @connecting_to_the_database
    def add_schedule_changes(cursor, *args):
        cursor.execute(f"""
                    SELECT COUNT(*) FROM schedule_changes
                    WHERE start_date = %s AND end_date = %s
                    """, args[:2]
                       )

        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(f"""
                        INSERT INTO schedule_changes
                        (start_date, end_date, is_it_a_working_day)
                        VALUES(%s, %s, %s)""", args
                           )


    @staticmethod
    @connecting_to_the_database
    def get_all_schedule_changes(cursor):
        cursor.execute(f"""SELECT * FROM schedule_changes
                    WHERE start_date > now()""")
        return cursor.fetchall()

    @staticmethod
    @connecting_to_the_database
    def get_schedule_changes(cursor, *args):
        cursor.execute(f"""
                    SELECT * FROM schedule_changes
                    WHERE date_trunc('day', start_date) = %s::date""", args  # We leave only the date for the search
                       )
        return cursor.fetchall()

    @staticmethod
    @connecting_to_the_database
    def delete_schedule_changes(cursor, *args):
        cursor.execute(f"""
                    DELETE FROM schedule_changes
                    WHERE date_trunc('day', start_date) = %s::date""", args  # We leave only the date for the search
                       )

    @staticmethod
    @connecting_to_the_database
    def delete_table_constant_breaks(cursor):
        cursor.execute(f'''DELETE FROM constant_breaks''')  # Таким образом очищается вся таблица

    @staticmethod
    @connecting_to_the_database
    def add_constant_breaks(cursor, *args):
        cursor.execute(f"""INSERT INTO constant_breaks
                        (start_time, end_time)
                        VALUES(%s, %s);""", args)


    @staticmethod
    @connecting_to_the_database
    def get_constant_breaks(cursor):
        cursor.execute(f"""SELECT * FROM constant_breaks;""")
        return cursor.fetchall()


    # @staticmethod
    # @connecting_to_the_database
    # def drop(cursor):
    #     cursor.execute(f"""DROP TABLE appointments;""")


dataBase = DataBase()
# dataBase.drop()
print(dataBase.get_all_appointments())
x = dataBase.get_treatment_duration('wr')[0]
e = dataBase.get_treatment_duration_by_id(4)[0]
print(e)
