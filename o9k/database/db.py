import sqlite3
import csv

import requests
from bs4 import BeautifulSoup

NULL = "NULL"
DATABASE = "data\\over9000.db"
USERS_TABLE = "USERS"
RESULTS_TABLE = "RESULTS"
USER_HEADERS = ["ID", "NAME", "CSV", "SOCIALS", "TEAM"]
RESULTS_HEADERS = ["MeetID", "Name", "Sex", "Event", "Equipment", "Age", "AgeClass",
                   "BirthYearClass", "Division", "BodyweightKg", "WeightClassKg",
                   "Squat1Kg", "Squat2Kg", "Squat3Kg", "Squat4Kg", "Best3SquatKg",
                   "Bench1Kg", "Bench2Kg", "Bench3Kg", "Bench4Kg", "Best3BenchKg",
                   "Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Deadlift4Kg", "Best3DeadliftKg",
                   "TotalKg", "Place", "Dots", "Wilks", "Glossbrenner", "Goodlift",
                   "Tested", "Country", "State", "Federation", "ParentFederation",
                   "Date", "MeetCountry", "MeetState", "MeetTown", "MeetName", "CSV"]

reals = RESULTS_HEADERS[9:32]


#                       #
#   DATABASE CREATION   #
#                       #
# TODO: clean up setup code
def setup_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if USERS table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USERS';")
    if cursor.fetchone():
        print("Table USERS exists.\n Continuing.")
    else:
        print("Table USERS doesn't exist.\n Creating USERS")
        # create the USERS table
        ### NOTES:
        # LIFTER_NAME was natively NAME # NOTE: CHANGED BACK
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OVER9000 (
                ID TEXT NOT NULL,
                NAME TEXT NOT NULL,
                CSV TEXT NOT NULL,
                SOCIALS TEXT,
                TEAM TEXT,
                UNIQUE (ID) ON CONFLICT IGNORE
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Results (
                MeetID TEXT PRIMARY KEY,
                Name TEXT,
                Sex TEXT,
                Event TEXT,
                Equipment TEXT,
                Age TEXT,
                AgeClass TEXT,
                BirthYearClass TEXT,
                Division TEXT,
                BodyweightKg TEXT,
                WeightClassKg TEXT,
                Squat1Kg TEXT,
                Squat2Kg TEXT,
                Squat3Kg TEXT,
                Squat4Kg TEXT,
                Best3SquatKg TEXT,
                Bench1Kg TEXT,
                Bench2Kg TEXT,
                Bench3Kg TEXT,
                Bench4Kg TEXT,
                Best3BenchKg TEXT,
                Deadlift1Kg TEXT,
                Deadlift2Kg TEXT,
                Deadlift3Kg TEXT,
                Deadlift4Kg TEXT,
                Best3DeadliftKg TEXT,
                TotalKg TEXT,
                Place TEXT,
                Dots TEXT,
                Wilks TEXT,
                Glossbrenner TEXT,
                Goodlift TEXT,
                Tested TEXT,
                Country TEXT,
                State TEXT,
                Federation TEXT,
                ParentFederation TEXT,
                Date TEXT,
                MeetCountry TEXT,
                MeetState TEXT,
                MeetTown TEXT,
                MeetName TEXT
                CSV TEXT NOT NULL,
                UNIQUE (MeetID) ON CONFLICT IGNORE
            );
        """)
        print("Table RESULTS created")

    # commit the changes and close the connection
    conn.commit()
    return conn


#                       #
#   ENTRY PROCESSING    #
#                       #
def str_cast(value):
    return str("\"" + value + "\"")


def get_csv_link(link):
    # Fetch the page
    response = requests.get(link)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the h2 tag with "Competition Results" text
    h2_tag = soup.find_all('h2')
    print("H2 TAGS: ", h2_tag)  # DEBUG print
    h2_tag = h2_tag[1]
    print("CSV_LINK in get_csv_link: ", h2_tag)  # DEBUG print

    # Find the a tag within the h2 tag and get its href value
    csv_link = h2_tag.find('a')['href']

    print("get_csv_link", csv_link)  # DEBUG print
    return csv_link


def load_csv_data(csv_link):
    full_link = "https://www.openpowerlifting.org" + csv_link
    # Get the CSV data
    response = requests.get(full_link)  # you may need to adjust the URL
    data = response.content.decode('utf-8')

    # Parse the CSV data into a dictionary
    reader = csv.DictReader(StringIO(data))
    rows = list(reader)

    # Now rows is a list of dictionaries, each dictionary represents a row in the CSV
    print("in load_csv_data, printing data")  # DEBUG print
    for row in rows:
        # TODO: maybe just do all formatting in here?
        print(row)  # or do whatever you need to do with the row   # DEBUG print

    return rows


# Convert dict data to sql entries
def csv_to_sql(csv_data):
    for meet in csv_data:
        for k, v in meet.items():
            if not len(v):
                meet[k] = NULL
            else:
                meet[k] = str_cast(v)
# TODO: START HERE BUDDY, WE'RE DOING CREATE_ENTRY AND NEED ALL THE FORMATTING DONE OUTSIDE SO THE SQL QUERY IS EASY
    return csv_data


class Database:
    def __init__(self):
        self.user_headers = USER_HEADERS
        self.results_headers = RESULTS_HEADERS
        self.conn = setup_db()

    # TODO: abstract some of this to crud, crud.create() not doing anything right now
    # create entry into OVER9000 and related entries into RESULTS
    def create_entry(self, op_link):
        # TODO: OP_LINK IS A FUCKING LIST DONT FORGET
        csv_link = get_csv_link(op_link)
        csv_data = load_csv_data(csv_link)
        formatted_csv = csv_to_sql(csv_data)

        pass
        # csv_data = load_csv_data(get_csv_link(lifter_id))
        print("csv_data_as_dict: ", csv_data)  # DEBUG print

        # sql_data = crud.create_entry(lifter_id, csv_data)

        # OVER9000 table entry
        OVER9K_SQL_HEADERS = ",".join(self.user_headers)

        values_list = [op_link, csv_data[0]["NAME"], csv_link, NULL, NULL]
        print("values list: ", values_list)  # DEBUG print
        OVER9K_SQL_VALUES = ",".join(values_list)

        sql_over9000_command = f"INSERT INTO {USERS_TABLE} ({OVER9K_SQL_HEADERS}) " \
                               f"VALUES ({OVER9K_SQL_VALUES})"

        print("SQL_OVER9000_COMMAND: ", sql_over9000_command)  ## work on format_csv_data, values are not cast properly
        self.conn.execute(sql_over9000_command)
        self.conn.commit()

        # RESULTS table entries
        csv_data = format_csv_data(csv_data)
        RESULTS_SQL_HEADERS = ",".join(self.results_headers)

        # TODO: can use a multiple execute here if I knew how to SQL
        for meet in csv_data:
            RESULTS_SQL_VALUES = ",".join(meet.values())

            sql_results_command = f"INSERT INTO {RESULTS_TABLE} ({RESULTS_SQL_HEADERS}) " \
                                  f"VALUES ({RESULTS_SQL_VALUES})"

            print("SQL_RESULT_COMMAND: ", sql_results_command)
            self.conn.execute(sql_results_command)

        self.conn.commit()
        # CONTINUE here

    # SELECT from test
    def read_entry(self, lifter_id, fields):
        pass

    def update_entry(self, lifter_id, table, fields, new_vals):
        pass

    def delete_entry(self, lifter_id):
        pass

    def refresh_entry(self, lifter_id):
        pass
