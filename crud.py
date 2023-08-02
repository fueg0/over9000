import sqlite3
import csv

DATABASE = "over9000.db"
OVER9000_TABLE = "OVER9000"
RESULTS_TABLE = "RESULTS"


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
        # LIFTER_NAME was natively NAME
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OVER9000 (
                ID TEXT,
                LIFTER_NAME TEXT,
                CSV TEXT,
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
        # LIFTER_STATE was natively STATE,
        # MEETDATE was natively DATE,
        # LIFTER_NAME was natively NAME
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RESULTS (
                CSV_ID TEXT,
                LIFTER_NAME TEXT,
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
                PLACE TEXT,
                DOTS TEXT,
                WILKS TEXT,
                GLOSSBRENNER TEXT,
                GOODLIFT TEXT,
                TESTED TEXT,
                COUNTRY TEXT,
                LIFTER_STATE TEXT,
                FEDERATION TEXT,
                PARENTFEDERATION TEXT,
                MEETDATE TEXT,
                MEETCOUNTRY TEXT,
                MEETSTATE TEXT,
                MEETTOWN TEXT,
                MEETNAME TEXT
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
