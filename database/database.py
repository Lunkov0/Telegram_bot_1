import psycopg2
from config import host, user, password, db_name, port

try:
    # connect to exist database
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )

    # the cursor for perfoming database operations
    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT version();'
        )

        print(f'SOME {cursor.fetchone()}')

except Exception as _ex:
    print('[INFO] Error while working with PostgreSQL', _ex)
finally:
    if conn:
        conn.close()
        print('[INFO] PostgreSQL connection closed')
