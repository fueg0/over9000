import sqlite3
import csv
from io import StringIO

import o9k.o9k_utils.utils as utils

import requests
from bs4 import BeautifulSoup

DEBUG = True
NULL = "NULL"
DATABASE = "..\\o9k.db"
USERS_TABLE = "USERS"
RESULTS_TABLE = "RESULTS"
USER_HEADERS = ["ID", "NAME", "CSV", "SOCIALS", "TEAM"]
RESULTS_HEADERS = ["Name", "Sex", "Event", "Equipment", "Age", "AgeClass",
                   "BirthYearClass", "Division", "BodyweightKg", "WeightClassKg",
                   "Squat1Kg", "Squat2Kg", "Squat3Kg", "Squat4Kg", "Best3SquatKg",
                   "Bench1Kg", "Bench2Kg", "Bench3Kg", "Bench4Kg", "Best3BenchKg",
                   "Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Deadlift4Kg", "Best3DeadliftKg",
                   "TotalKg", "Place", "Dots", "Wilks", "Glossbrenner", "Goodlift",
                   "Tested", "Country", "State", "Federation", "ParentFederation",
                   "Date", "MeetCountry", "MeetState", "MeetTown", "MeetName", "CSV", "MeetID"]

reals = RESULTS_HEADERS[9:32]


#                       #
#   DATABASE CREATION   #
#                       #
def setup_db(debug=DEBUG):
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
            CREATE TABLE IF NOT EXISTS USERS (
                ID TEXT PRIMARY KEY,
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
            CREATE TABLE IF NOT EXISTS RESULTS (
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
                MeetName TEXT,
                CSV TEXT NOT NULL,
                MeetID TEXT PRIMARY KEY,
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


def load_csv_data(csv_link, debug=DEBUG):
    full_link = "https://www.openpowerlifting.org" + csv_link
    # Get the CSV data
    response = requests.get(full_link)  # you may need to adjust the URL
    data = response.content.decode('utf-8')

    # Parse the CSV data into a dictionary
    reader = csv.DictReader(StringIO(data))
    rows = list(reader)

    # Now rows is a list of dictionaries, each dictionary represents a row in the CSV
    print("in load_csv_data, printing data")  # DEBUG print
    utils.debug_print(f"csv before processing: {rows}", debug)  # DEBUG print

    for meet in rows:
        meet["CSV"] = csv_link
        meet["MeetID"] = " ".join([meet["Name"], "-", meet["MeetName"], "-", meet["Division"]])
        for k, v in meet.items():
            if not len(v):
                meet[k] = NULL
            else:
                meet[k] = str_cast(v)

    return rows


# Convert dict data to sql entries
def csv_processing(csv_data, debug=DEBUG):
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

    def create_lifter(self, op_link, csv_data, csv_link, debug=DEBUG):
        LIFTER_HEADERS = ",".join(self.user_headers)

        lifter_entry = [str_cast(op_link), csv_data[0]["Name"], csv_data[0]["CSV"], NULL, NULL]
        utils.debug_print(f"values list: {lifter_entry}", debug)  # DEBUG print
        LIFTER_VALUES = ",".join(lifter_entry)

        create_lifter_command = f"INSERT INTO {USERS_TABLE} ({LIFTER_HEADERS}) " \
                                f"VALUES ({LIFTER_VALUES})"

        utils.debug_print(f"create_lifter SQL: {create_lifter_command}",
                          debug)  ## work on format_csv_data, values are not cast properly
        self.conn.execute(create_lifter_command)
        self.conn.commit()

    def create_results(self, csv_data, debug=DEBUG):
        RESULTS_HEADERS = ",".join(self.results_headers)

        # TODO: can use a multiple execute here if I knew how to SQL
        for meet in csv_data:
            RESULTS_SQL_VALUES = ",".join(meet.values())

            sql_results_command = f"INSERT INTO {RESULTS_TABLE} ({RESULTS_HEADERS}) VALUES ({RESULTS_SQL_VALUES})"

            utils.debug_print(f"create_results SQL: {sql_results_command}", debug)
            self.conn.execute(sql_results_command)
            self.conn.commit()

    # create entry into OVER9000 and related entries into RESULTS
    def create_entry(self, op_links, debug=DEBUG):
        utils.debug_print(f"create_entry:: \nop_links: {op_links}", debug)

        for op_link in op_links:
            utils.debug_print(f"create_entry:: \nop_link: {op_link}", debug)
            csv_link = get_csv_link(op_link)
            csv_data = load_csv_data(csv_link)

            # TODO: check if op_link exists before doing all the stuff
            utils.debug_print(f"csv after processing: {csv_data}", debug)  # DEBUG print
            # Create LIFTER entry
            self.create_lifter(op_link, csv_data, csv_link)

            # TODO: check if MeetID exists before doing all the stuff
            # Create RESULTS entry
            self.create_results(csv_data)

    def read_results(self, lifter_id, fields, debug=DEBUG):
        fields = ", ".join(fields)
        select_query = f"SELECT {fields} from RESULTS WHERE CSV = ?"
        utils.debug_print(f"read_entry:: {select_query}", debug)
        res = self.conn.execute(select_query, (lifter_id,))

        return res

    def read_user(self, lifter_id, fields, debug=DEBUG):
        fields = ", ".join(fields)
        select_query = f"SELECT {fields} from USERS WHERE CSV = ?"
        utils.debug_print(f"read_entry:: {select_query}", debug)
        res = self.conn.execute(select_query, (lifter_id,))

        return res

    # SELECT
    def read_entry(self, lifter_id, fields, table, debug=DEBUG):
        if table == "USERS":
            res = self.read_user(lifter_id, fields)
        elif table == "RESULTS":
            res = self.read_results(lifter_id, fields)
        else:
            res = "INVALID TABLE CHOICE"

        return res

    def update_results(self, lifter_id, fields, new_vals):
        # Ensure the lengths of fields and values match
        if len(fields) != len(new_vals):
            raise ValueError("The number of fields and values must be the same")

        # Create the 'SET' part of the SQL statement
        set_clause = ', '.join([f"{field} = ?" for field in fields])

        # Construct the complete SQL query
        update_query = f"UPDATE RESULTS SET {set_clause} WHERE MeetID = ?"

        # Execute the query
        self.conn.execute(update_query, (*new_vals, lifter_id))
        self.conn.commit()

        # TODO: this implementation is chiefed, gotta come back to this
        csv_link_query = f"SELECT CSV from RESULTS WHERE MeetID = ?"
        csv_link = self.conn.execute(csv_link_query, (lifter_id,))
        res = ""
        for link in csv_link:
            res = self.read_results(link[0], fields)
        return res

    def update_user(self, lifter_id, fields, new_vals):
        # Ensure the lengths of fields and values match
        if len(fields) != len(new_vals):
            raise ValueError("The number of fields and values must be the same")

        # Create the 'SET' part of the SQL statement
        set_clause = ', '.join([f"{field} = ?" for field in fields])

        # Construct the complete SQL query
        update_query = f"UPDATE USERS SET {set_clause} WHERE CSV = ?"

        # Execute the query
        self.conn.execute(update_query, (*new_vals, lifter_id))
        self.conn.commit()

        res = self.read_user(lifter_id, fields)
        return res

    def update_entry(self, lifter_id, fields, new_vals, table):
        if table == "USERS":
            res = self.update_user(lifter_id, fields, new_vals)
        elif table == "RESULTS":
            res = self.update_results(lifter_id, fields, new_vals)
        else:
            res = "INVALID TABLE CHOICE"

        return res

    def delete_user(self, lifter_id):
        # Construct the SQL delete query
        delete_query = "DELETE FROM USERS WHERE CSV = ?"

        res = self.read_user(lifter_id, ["NAME", "CSV", "TEAM"])

        # Execute the query
        self.conn.execute(delete_query, (lifter_id,))
        self.conn.commit()

        return res

    def delete_results(self, lifter_id):
        # Construct the SQL delete query
        delete_query = "DELETE FROM RESULTS WHERE MeetID = ?"

        csv_query = f"SELECT CSV from RESULTS WHERE MeetID = ?"
        csv_id = self.conn.execute(csv_query, (lifter_id,))
        res = self.read_results(csv_id, ["Squat2Kg", "Bench2Kg", "Deadlift2Kg", "MeetID"])

        # Execute the query
        self.conn.execute(delete_query, (lifter_id,))
        self.conn.commit()

        return res

    def delete_entry(self, lifter_id, table):
        if table == "USERS":
            res = self.delete_user(lifter_id)
        elif table == "RESULTS":
            res = self.delete_results(lifter_id)
        else:
            res = "INVALID TABLE CHOICE"

        return res

    def refresh_entry(self, lifter_id):
        pass


