import sqlite3
import csv

NULL = "NULL"
DATABASE = "over9000.db"
OVER9000_TABLE = "OVER9000"
RESULTS_TABLE = "RESULTS"
OVER9000_HEADERS = ["ID", "NAME", "CSV", "SOCIALS", "TEAM"]
RESULTS_HEADERS = ["NAME", "SEX", "EVENT", "EQUIPMENT", "AGE", "AGECLASS", "BIRTHYEARCLASS", "DIVISION", "BODYWEIGHTKG", "WEIGHTCLASSKG", "SQUAT1KG", "SQUAT2KG", "SQUAT3KG", "SQUAT4KG", "BEST3SQUATKG", "BENCH1KG", "BENCH2KG", "BENCH3KG", "BENCH4KG", "BEST3BENCHKG", "DEADLIFT1KG", "DEADLIFT2KG", "DEADLIFT3KG", "DEADLIFT4KG", "BEST3DEADLIFTKG", "TOTALKG", "PLACE", "DOTS", "WILKS", "GLOSSBRENNER", "GOODLIFT", "TESTED", "COUNTRY", "STATE", "FEDERATION", "PARENTFEDERATION", "DATE", "MEETCOUNTRY", "STATE", "MEETTOWN", "MEETNAME", "CSV"]


def setup_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if OVER9000 table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='OVER9000';")
    if cursor.fetchone():
        print("Table OVER9000 exists.\n Continuing.")
    else:
        print("Table OVER9000 doesn't exist.\n Creating OVER9000")

        # create the SQLite database because it doesn't exist
        # create the OVER9000 table
        ### NOTES:
        # LIFTER_NAME was natively NAME # NOTE: CHANGED BACK
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OVER9000 (
                ID TEXT NOT NULL,
                NAME TEXT NOT NULL,
                CSV TEXT NOT NULL,
                SOCIALS TEXT,
                TEAM TEXT
            );
        """)
        print("Table OVER9000 created")

    # Check if RESULTS table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RESULTS';")
    if cursor.fetchone():
        print("Table RESULTS exists.\n Continuing.")
    else:
        print("Table RESULTS doesn't exist.\n Creating RESULTS")
        # create the RESULTS table because it doesn't exist
        ### NOTES:
        # LIFTER_STATE was natively STATE, # NOTE: CHANGED BACK
        # MEETDATE was natively DATE, # NOTE: CHANGED BACK
        # LIFTER_NAME was natively NAME # NOTE: CHANGED BACK
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RESULTS (
                NAME TEXT,
                SEX TEXT,
                EVENT TEXT,
                EQUIPMENT TEXT,
                AGE TEXT,
                AGECLASS TEXT,
                BIRTHYEARCLASS TEXT,
                DIVISION TEXT,
                BODYWEIGHTKG REAL,
                WEIGHTCLASSKG REAL,
                SQUAT1KG REAL,
                SQUAT2KG REAL,
                SQUAT3KG REAL,
                SQUAT4KG REAL,
                BEST3SQUATKG REAL,
                BENCH1KG REAL,
                BENCH2KG REAL,
                BENCH3KG REAL,
                BENCH4KG REAL,
                BEST3BENCHKG REAL,
                DEADLIFT1KG REAL,
                DEADLIFT2KG REAL,
                DEADLIFT3KG REAL,
                DEADLIFT4KG REAL,
                BEST3DEADLIFTKG REAL,
                TOTALKG REAL,
                PLACE REAL,
                DOTS REAL,
                WILKS REAL,
                GLOSSBRENNER REAL,
                GOODLIFT REAL,
                TESTED TEXT,
                COUNTRY TEXT,
                LIFTER_STATE TEXT,
                FEDERATION TEXT,
                PARENTFEDERATION TEXT,
                DATE TEXT,
                MEETCOUNTRY TEXT,
                STATE TEXT,
                MEETTOWN TEXT,
                MEETNAME TEXT,
                CSV TEXT NOT NULL
            );
        """)
        print("Table RESULTS created")

    # commit the changes and close the connection
    conn.commit()
    return conn


# Convert dict data to sql entries
def csv_to_sql(csv_data):
    pass


def create_entry(lifter_id, csv_data):
    pass



def read_entry(lifter_id):
    pass


def update_entry(lifter_id, field, new_val):
    pass


def delete_entry(lifter_id):
    pass


def refresh_entry(lifter_id):
    pass
