import mysql.connector


def db_connection(sys_name):
    # Initialize database name
    database = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database=sys_name
    )
    # Initialize cursor
    cursor = database.cursor()

    return database, cursor


if __name__ == '__main__':
    db_connection('or_system_2022')
