import psycopg2
from config import HOST, USER, PASSWORD, DB_NAME, PORT


'''Для работы с Postgres создан класс DataBase
Создаем таблицы:
    services - список услуг, время на услугу, описание
    
Декоратор connecting_to_the_database используется для подключения и отключения от БД

Реализованны функции:
    add_service - добавить услугу'''
class DataBase:
    def connecting_to_the_database(func):
        def wrapper(*args):
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DB_NAME)
            connection.autocommit = True
            cursor = connection.cursor()

            # Шо за первый объект? self?
            func(cursor, *args[1:])

            connection.close()
        return wrapper

    @connecting_to_the_database
    def create_table_services(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services(
                name VARCHAR(50),
                duration TIME,
                description VARCHAR(400)
                );
        ''')

    def __init__(self):
        self.create_table_services()

        # cursor.execute('''SELECT * FROM public.services''')
        # print(cursor.fetchall())

    @connecting_to_the_database
    def add_service(cursor, name, duration, description):
        cursor.execute(f"""
                    INSERT INTO services
                    (name, duration, description)
                    VALUES('{name}', '{duration}', '{description}');
                       """)


q = DataBase()
q.add_service("Artem", "1:15", "friend")

