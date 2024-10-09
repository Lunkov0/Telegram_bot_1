import psycopg2
import asyncio
import asyncpg
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
    async def connecting_to_the_database(func):
        def wrapper(*args):
            conn = asyncpg.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DB_NAME)
            conn.autocommit = True

            res = func(conn, *args)

            conn.close()

            return res
        return wrapper

    @staticmethod
    @connecting_to_the_database
    def create_table_treatments(conn):
        conn.execute('''
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
    def create_table_appointments(conn):
        conn.execute('''
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
    def create_table_schedule(conn):
        conn.execute('''
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
    def create_table_schedule_changes(conn):
        conn.execute('''
                CREATE TABLE IF NOT EXISTS schedule_changes(
                    id SERIAL PRIMARY KEY,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    is_it_a_working_day SMALLINT
                );
            ''')

    @staticmethod
    @connecting_to_the_database
    def create_table_constant_breaks(conn):
        conn.execute('''
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
    def add_treatment(conn, *args):
        conn.execute(f"""
                    INSERT INTO treatments
                    (name, duration, price, description)
                    VALUES(%s, %s, %s, %s)""", *args
                       )


    @staticmethod
    @connecting_to_the_database
    def get_all_treatments(conn):
        conn.execute('SELECT * FROM treatments')
        res = conn.fetchall()
        return res


    @staticmethod
    @connecting_to_the_database
    def treatments_get_names(conn):
        conn.execute('SELECT id, name FROM treatments')
        res = conn.fetchall()
        return res


    @staticmethod
    @connecting_to_the_database
    def del_treatment(conn, *args):
        conn.execute(f"""
                    DELETE FROM treatments
                    WHERE name=%s""", args
                       )


    @staticmethod
    @connecting_to_the_database
    def get_treatment_id(conn, *args):
        conn.execute(f"""
                    SELECT id 
                    FROM treatments
                    WHERE name = %s;
                    """, args)
        return conn.fetchone()


    @staticmethod
    @connecting_to_the_database
    def get_treatment_duration(conn, name):
        conn.execute(f'''
            SELECT duration
            FROM treatments
            WHERE name = %s
        ''', (name,))
        return conn.fetchone()


    @staticmethod
    @connecting_to_the_database
    def get_treatment_name(conn, id):
        conn.execute(f'''
            SELECT name
            FROM treatments
            WHERE id = %s
        ''', (id,))
        return conn.fetchone()


    @staticmethod
    @connecting_to_the_database
    def get_treatment_duration_by_id(conn, id):
        conn.execute(f'''
            SELECT duration
            FROM treatments
            WHERE id = %s
        ''', (id,))
        return conn.fetchone()


    @staticmethod
    @connecting_to_the_database
    def add_appointment(conn, *args):
        conn.execute(f"""INSERT INTO appointments
                    (full_name, appointment_time, contact_phone, users_tg_id, services_id)
                    VALUES(%s, %s, %s, %s, %s)""", *args)

    @staticmethod
    @connecting_to_the_database
    def get_my_appointments(conn, *args):
        conn.execute(f'''SELECT *
                           FROM appointments
                           WHERE users_tg_id = %s
                           AND appointment_time > now()''', args)
        return conn.fetchall()


    @staticmethod
    @connecting_to_the_database
    def get_all_appointments(conn):
        conn.execute(f'''SELECT *
                        FROM appointments
                        WHERE appointment_time > now()''')
        return conn.fetchall()


    @staticmethod
    @connecting_to_the_database
    def del_appointment(conn, *args):
        conn.execute(f"""
                    DELETE FROM appointments
                    WHERE users_tg_id = %s""", args)

    @staticmethod
    @connecting_to_the_database
    def del_treatment(conn, *args):
        conn.execute(f"""
                    DELETE FROM treatments
                    WHERE name=%s""", args
                       )

    @staticmethod
    @connecting_to_the_database
    def schedule_get(conn):
        conn.execute('SELECT * FROM schedule')
        return conn.fetchall()

    @staticmethod
    @connecting_to_the_database
    def get_weekday_schedule(conn, *args):
        conn.execute('''SELECT start_time, end_time FROM schedule
                       WHERE day_of_the_week = %s''', args)
        return conn.fetchall()

    @staticmethod
    @connecting_to_the_database
    def schedule_set_s(conn, *args):
        conn.execute('UPDATE schedule '
                       'SET start_time = %s '
                       'WHERE day_of_the_week = %s', args)

    @staticmethod
    @connecting_to_the_database
    def schedule_set_f(conn, *args):
        conn.execute('UPDATE schedule '
                       'SET end_time = %s '
                       'WHERE day_of_the_week = %s', args)


# '''************************************ schedule of changes *************************************'''
    @staticmethod
    @connecting_to_the_database
    def get_all_schedule_changes(conn):
        conn.execute(f"""
                        SELECT * FROM schedule_changes
                        WHERE start_date > now()
                        ORDER BY start_date ASC
                        """)
        return conn.fetchall()


    # Добавляет данные если такого кортежа еще нет
    @staticmethod
    @connecting_to_the_database
    def add_schedule_changes(conn, *args):
        conn.execute(f"""
                    SELECT COUNT(*) FROM schedule_changes
                    WHERE start_date = %s AND end_date = %s
                    """, args[:2]
                       )

        count = conn.fetchone()[0]
        if count == 0:
            conn.execute(f"""
                        INSERT INTO schedule_changes
                        (start_date, end_date, is_it_a_working_day)
                        VALUES(%s, %s, %s)""", args
                           )


    @staticmethod
    @connecting_to_the_database
    def get_all_schedule_changes(conn):
        conn.execute(f"""SELECT * FROM schedule_changes
                    WHERE start_date > now()""")
        return conn.fetchall()

    @staticmethod
    @connecting_to_the_database
    def get_schedule_changes(conn, *args):
        conn.execute(f"""
                    SELECT * FROM schedule_changes
                    WHERE date_trunc('day', start_date) = %s::date""", args  # We leave only the date for the search
                       )
        return conn.fetchall()

    @staticmethod
    @connecting_to_the_database
    def delete_schedule_changes(conn, *args):
        conn.execute(f"""
                    DELETE FROM schedule_changes
                    WHERE date_trunc('day', start_date) = %s::date""", args  # We leave only the date for the search
                       )

    @staticmethod
    @connecting_to_the_database
    def delete_table_constant_breaks(conn):
        conn.execute(f'''DELETE FROM constant_breaks''')  # Таким образом очищается вся таблица

    @staticmethod
    @connecting_to_the_database
    def add_constant_breaks(conn, *args):
        conn.execute(f"""INSERT INTO constant_breaks
                        (start_time, end_time)
                        VALUES(%s, %s);""", args)


    @staticmethod
    @connecting_to_the_database
    def get_constant_breaks(conn):
        conn.execute(f"""SELECT * FROM constant_breaks;""")
        return conn.fetchall()

    # @staticmethod
    # @connecting_to_the_database
    # def drop(conn):
    #     conn.execute(f"""DROP TABLE appointments;""")


dataBase = DataBase()
# dataBase.drop()
print(dataBase.get_all_appointments())
x = dataBase.get_treatment_duration('wr')[0]
e = dataBase.get_treatment_duration_by_id(4)[0]
print(e)
