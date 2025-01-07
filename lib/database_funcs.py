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
                customer TEXT DEFAULT 'NON',
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
                smu TEXT,
                style_name TEXT,
                size_range TEXT,
                ratio TEXT,
                po_qty INTEGER,
                cost_price REAL,
                shipping_date TEXT,
                FOREIGN KEY (group_id) REFERENCES style_group(group_id) 
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )"""
    )

    # create colors table
    cr.execute(
        """CREATE TABLE IF NOT EXISTS colors (
                po_num INTEGER,
                team TEXT DEFAULT '',
                color_code TEXT DEFAULT '',
                piece1_color TEXT DEFAULT '',
                piece2_color TEXT DEFAULT '',
                color_qty INTEGER ,
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

    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (3, 44315, '2T-4T', 1000)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (3, 44316, '4-7', 1500)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (3, 44317, '8-16', 2000)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (1, 54317, '8-16', 3000)")
    # cr.execute("INSERT INTO pos (group_id, po_num, size_range, po_qty) VALUES (2, 54318, '8-16', 4000)")

    # cr.execute("INSERT INTO colors VALUES (44315, 'LL', 'PUBK', 'PUR', 'BLK', 500)")
    # cr.execute("INSERT INTO colors VALUES (44315, 'BC', 'KLBK', 'KLY', 'BLK', 500)")
    # cr.execute("INSERT INTO colors VALUES (44315, 'LL', 'RDBK', 'RED', 'BLK', 500)")

    # cr.execute("INSERT INTO colors VALUES (44316, 'LL', 'PUBK', 'PUR', 'BLK', 500)")
    # cr.execute("INSERT INTO colors VALUES (44316, 'BC', 'KLBK', 'KLY', 'BLK', 500)")
    # cr.execute("INSERT INTO colors VALUES (44316, 'LL', 'RDBK', 'RED', 'BLK', 500)")

    # cr.execute("INSERT INTO colors VALUES (44317, 'LL', 'PUBK', 'PUR', 'BLK', 500)")
    # cr.execute("INSERT INTO colors VALUES (44317, 'BC', 'KLBK', 'KLY', 'BLK', 500)")
    # cr.execute("INSERT INTO colors VALUES (44317, 'LL', 'RDBK', 'RED', 'BLK', 500)")

    # cr.execute("INSERT INTO colors VALUES (54317, NULL, 'SND', 'SND', 'SND', 500)")

    # cr.execute("INSERT INTO colors VALUES (54318, NULL, 'RED', 'RED', 'RED', 500)")

    # cr.execute("INSERT INTO colors VALUES (54318, '', 'BLK', 'BLK', 'BLK', 500)")
    # cr.execute("ALTER TABLE style_group RENAME brand TO customer")

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
                g.group_id, group_name, customer, brand_team, garment_type, 
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


def DB_GET_TOP_LEVEL_DATA(id):
    # Create/connect to data base
    db = sqlite3.connect("DB/styles.db")
    db.execute("PRAGMA foreign_keys = ON;")
    # Create a cursor
    cr = db.cursor()

    # get the main data from style_group table and fabrics table
    cr.execute(
        """SELECT 
                g.group_id, group_name, customer, brand_team, garment_type, 
                piece1_type, piece2_type, total_qty, rcvd_date,
                GROUP_CONCAT(fabric_type) AS fabric_types, GROUP_CONCAT(description), GROUP_CONCAT(fabric_gsm)
            FROM 
                style_group AS g
            LEFT JOIN 
                fabrics AS f ON g.group_id = f.group_id
            WHERE g.group_id = ?
            GROUP BY g.group_id""", (id,)
    )

    data = cr.fetchone()
    # convert the data into dict
    main_data = {
        "group_id": data[0],
        "group_name": data[1],
        "customer": data[2],
        "brand_team": data[3],
        "garment_type": data[4],
        "piece1_type": data[5],
        "piece2_type": data[6],
        "total_qty": data[7],
        "rcvd_date": data[8],
        "fabric_types": data[9].split(",") if data[9] else [""],
        "fabric_descriptions": data[10].split(",") if data[10] else [""],
        "fabric_gsms": data[11].split(",") if data[11] else [""],
    }

    cr.execute(
        """SELECT 
                p.po_num, style_name, smu, size_range, ratio,
                GROUP_CONCAT(team), 
                GROUP_CONCAT(color_code), 
                GROUP_CONCAT(piece1_color), 
                GROUP_CONCAT(piece2_color), 
                GROUP_CONCAT(color_qty), 
                po_qty, cost_price, shipping_date
            FROM 
                pos AS p
            LEFT JOIN 
                colors AS c ON p.po_num = c.po_num
            WHERE p.group_id = ?
            GROUP BY 
                p.po_num, style_name, smu, size_range, ratio,
                po_qty, cost_price, shipping_date
                """, (id,)
    )

    data = cr.fetchall()
    # convert the data into dict
    pos_data = [
        {
            "po_num": record[0],
            "style_name": record[1],
            "smu": record[2],
            "size_range": record[3],
            "ratio": record[4],
            "teams": record[5].split(",") if record[5] else [""],
            "color_codes": record[6].split(",") if record[6] else [""],
            "piece1_colors": record[7].split(",") if record[7] else [""],
            "piece2_colors": record[8].split(",") if record[8] else [""],
            "color_qtys": list(map(int, record[9].split(","))) if record[9] else [0],
            "po_qty": record[10],
            "price": record[11],
            "shipping_date": record[12],
        }
        for record in data
    ]

    db.commit()
    db.close()

    return main_data, pos_data

# add a new po to the database with one color
def DB_ADD_PO(po_data, color_data):
    # conntet to styles database
    db= sqlite3.connect("DB/styles.db")
    db.execute("PRAGMA foreign_keys = ON;")
    cr = db.cursor()

    # insert the po data to pos table
    cr.execute(
        """INSERT INTO pos VALUES(
                :po_num, :group_id, :smu, :style_name, :size_range, :ratio, :po_qty, :price, :shipping_date
            )""",
        po_data,
    )

    # insert the color data to colors table
    cr.execute(
        """INSERT INTO colors VALUES(
                :po_num, :teams, :color_codes, :piece1_colors, :piece2_colors, :color_qtys
            )""",
        color_data,
    )

    db.commit()
    db.close()