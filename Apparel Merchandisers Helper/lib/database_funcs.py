import sqlite3

def DB_CREATE():
    # Create/connect to data base
    db = sqlite3.connect('DB/styles.db')
    # Create a cursor
    cr = db.cursor()

    # Create style_group table
    cr.execute("""CREATE TABLE IF NOT EXISTS style_group (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT,
                rcvd_date TEXT,
                packing_method TEXT,
                total_qty INTEGER,
                brand TEXT,
                brand_team TEXT,
                piece1_type TEXT,
                piece2_type TEXT,
                piece1_fabric TEXT,
                piece2_fabric TEXT,
                piece1_gsm INTEGER,
                piece2_gsm INTEGER
            )"""
    )

    # create pos table
    cr.execute("""CREATE TABLE IF NOT EXISTS POs (
                po INTEGER PRIMARY KEY,
                group_id INTEGER,
                style_name TEXT,
                size_range TEXT,
                ratio TEXT,
                po_qty INTEGER,
                shipping_date TEXT,
                FOREIGN KEY (group_id) REFERENCES style_group(group_id)
            )"""
    )

    db.commit()
    db.close()


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

def DB_DELETE_STYLE(style):
    # Create/connect to data base
    db = sqlite3.connect('DB/styles.db')
    # Create a cursor
    cr = db.cursor()

    cr.execute("DELETE FROM styles WHERE style = ?", (style,))

    db.commit()
    db.close()

