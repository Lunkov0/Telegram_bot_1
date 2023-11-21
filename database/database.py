import psycopg2
from config import HOST, USER, PASSWORD, DB_NAME, PORT

try:
    # connect to exist database
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    
    conn.autocommit = True

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
