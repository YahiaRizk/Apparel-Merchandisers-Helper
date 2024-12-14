import sqlite3


def DB_CREATE():
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
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

    # cr.execute("INSERT INTO style_group (group_name, garment_type, total_qty, brand) VALUES ('', 'set', 1500, '')")

    db.commit()
    db.close()


def DB_SAVE_MAIN_INFO(data):
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
    # Create a cursor
    cr = db.cursor()

    main_info = data[0]
    fabrics_info = data[1]

    # insert the data to style_group table
    cr.execute(
        """INSERT INTO style_group VALUES(
                NULL,
                :group_name,
                :brand,
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


def DATABASE_GET_DATA():
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
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
    db = sqlite3.connect("DB/styles.db")
    # Create a cursor
    cr = db.cursor()

    cr.execute("DELETE FROM styles WHERE style = ?", (style,))

    db.commit()
    db.close()
