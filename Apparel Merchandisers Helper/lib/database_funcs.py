import sqlite3

def CREATE_DATABASE(data):
    # Create/connect to data base
    db = sqlite3.connect('DB/styles.db')
    # Create a cursor
    cr = db.cursor()

    # define columns list depend on data keys and type
    columns = []
    for key, value in data.items():
        column_type = 'TEXT'
        
        if isinstance(value, int):
            column_type = 'INTEGER'
        
        columns.append('{} {}'.format(key, column_type))

    # Create table 
    cr.execute("CREATE TABLE IF NOT EXISTS styles ({})".format(', '.join(columns)))

    db.commit()
    db.close()

def SAVE_TO_DATABASE(data):
    # Create/connect to data base
    db = sqlite3.connect('DB/styles.db')
    # Create a cursor
    cr = db.cursor()

    # define columns and placeholder
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))

    # insert data to style table
    cr.execute(f"INSERT INTO styles ({columns}) VALUES ({placeholders})", tuple(data.values()))

    db.commit()
    db.close()

def DATABASE_GET_DATA():
    # Create/connect to data base
    db = sqlite3.connect('DB/styles.db')
    # Create a cursor
    cr = db.cursor()

    result = cr.execute("SELECT * FROM styles")
    data = result.fetchall()

    for index, record in enumerate(data):
        data[index] = list(data[index])
        data[index].pop()
        

    db.commit()
    db.close()

    return data
