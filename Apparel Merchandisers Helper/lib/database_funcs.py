import sqlite3
from settings import CUSTOMER_OPT


def DB_CREATE():
    # Create/connect to styles database
    db = sqlite3.connect("DB/styles.db")
    db.execute("PRAGMA foreign_keys = ON;")
    # Create a cursor
    cr = db.cursor()

    # Create style_group table
    cr.execute(
        """CREATE TABLE IF NOT EXISTS style_group (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT,
                brand TEXT DEFAULT 'NON',
                brand_team TEXT,
                garment_type TEXT,
                piece1_type TEXT,
                piece2_type TEXT,
                total_qty INTEGER,
                rcvd_date TEXT
            )"""
    )

    # create pos table
    cr.execute(
        """CREATE TABLE IF NOT EXISTS pos (
                po_num INTEGER PRIMARY KEY,
                group_id INTEGER,
                style_name TEXT,
                size_range TEXT,
                ratio TEXT,
                po_qty INTEGER,
                shipping_date TEXT,
                FOREIGN KEY (group_id) REFERENCES style_group(group_id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )"""
    )

    # create pos table
    cr.execute(
        """CREATE TABLE IF NOT EXISTS colors (
                po_num INTEGER,
                team TEXT,
                color_code TEXT,
                piece1_color TEXT,
                piece2_color TEXT,
                color_qty INTEGER,
                FOREIGN KEY (po_num) REFERENCES pos(po_num)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )"""
    )

    # create fabrics table
    cr.execute(
        """CREATE TABLE IF NOT EXISTS fabrics (
                group_id INTEGER,
                fabric_type TEXT,
                description TEXT,
                fabric_gsm INTEGER,
                FOREIGN KEY (group_id) REFERENCES style_group(group_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )"""
    )

    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (7, 44315, '2T-4T', 1000)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (7, 44316, '4-7', 1500)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (7, 44317, '8-16', 2000)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (8, 54317, '8-16', 3000)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (9, 54318, '8-16', 4000)")

    db.commit()
    db.close()

    # Create/connect to paths database
    db = sqlite3.connect("DB/paths.db")

    # Create a cursor
    cr = db.cursor()

    # Create paths table
    cr.execute(
        """CREATE TABLE IF NOT EXISTS paths (
                customer TEXT PRIMARY KEY,
                path TEXT
            )"""
    )

    cr.executemany("INSERT OR IGNORE INTO paths VALUES (?, ?)", [(customer,'') for customer in CUSTOMER_OPT])

    db.commit()
    db.close()


def DB_SAVE_MAIN_INFO(data):
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
    db.execute("PRAGMA foreign_keys = ON;")
    # Create a cursor
    cr = db.cursor()

    main_info = data[0]
    fabrics_info = data[1]

    # insert the data to style_group table
    cr.execute(
        """INSERT INTO style_group VALUES(
                NULL,
                :group_name,
                :customer,
                :brand_team,
                :garment_type,
                :piece1_type,
                :piece2_type,
                :total_qty,
                :rcvd_date
            )""",
        main_info,
    )

    # get the inserted group_id
    group_id = cr.lastrowid

    # insert fabrics data to fabrics table
    cr.executemany(
        "INSERT INTO fabrics VALUES(?, ?, ?, ?)",
        [
            (
                group_id,
                fabric["fabric_type"],
                fabric["fabric_description"],
                fabric["fabric_gsm"],
            )
            for fabric in fabrics_info
        ],
    )

    db.commit()
    db.close()


def DB_GET_TABLE_DATA():
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
    db.execute("PRAGMA foreign_keys = ON;")
    # Create a cursor
    cr = db.cursor()

    cr.execute(
        """SELECT 
                g.group_id, group_name, brand, brand_team, garment_type, 
                piece1_type|| '\n' ||piece2_type, 
                GROUP_CONCAT(po_num, '\n'), GROUP_CONCAT(size_range, '\n'), GROUP_CONCAT(ratio, '\n'), 
                GROUP_CONCAT(po_qty, '\n'), total_qty, rcvd_date
            FROM 
                style_group AS g
            LEFT JOIN 
                pos AS p ON g.group_id = p.group_id
            GROUP BY
                g.group_id"""
    )

    data = cr.fetchall()

    db.commit()
    db.close()

    return data


def DB_GET_PATHS_DATA():
    # connect to paths database
    db = sqlite3.connect("DB/paths.db")
    # create cursor object
    cr = db.cursor()

    # get the data from database
    cr.execute("SELECT * FROM paths")
    result = cr.fetchall()

    # convert the result into dict
    data = {record[0]: record[1] for record in result}

    db.commit()
    db.close()

    return data


def DB_GET_PATH(customer):
    # connect to paths database
    db = sqlite3.connect("DB/paths.db")
    # create cursor object
    cr = db.cursor()

    # get the data from database
    cr.execute("SELECT path FROM paths WHERE customer = ?",(customer,))
    result = cr.fetchone()

    db.commit()
    db.close()

    return result[0]


def DB_INSERT_PATH(customer):
    # connect to paths database
    db = sqlite3.connect("DB/paths.db")
    # create cursor object
    cr = db.cursor()

    # try to insert the customer and return true otherwise return false
    try:
        cr.execute("INSERT INTO paths VALUES (?, ?)",(customer, ""))
        db.commit()
        db.close()
        return True
    except:
        db.commit()
        db.close()
        return False


def DB_UPDATE_PATH(customer, path):
    # connect to paths database
    db = sqlite3.connect("DB/paths.db")
    # create cursor object
    cr = db.cursor()

    cr.execute("UPDATE paths SET path = ? WHERE customer = ?", (path, customer))

    db.commit()
    db.close()


def DB_DELETE_STYLE(id):
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
    db.execute("PRAGMA foreign_keys = ON;")
    # Create a cursor
    cr = db.cursor()

    cr.execute("DELETE FROM style_group WHERE group_id = ?", (id,))

    db.commit()
    db.close()
