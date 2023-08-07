import csv
from io import StringIO
import crud
import requests
from bs4 import BeautifulSoup

NF = "https://www.openpowerlifting.org/u/nicholasfiorito"


# will set up DB if not existent and create a c sqlite onnection
# return a Database objectwith connection
def load_db():
    conn = crud.setup_db()
    return Database(conn)


def str_cast(value):
    return str("\"" + value + "\"")


def float_cast(value):
    return str(value)


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


def format_csv_headers(csv_data):
    formatted_csv_data = {k.upper(): v for k, v in csv_data.items()}
    # print(formatted_csv_data)
    return formatted_csv_data


def format_csv_data(csv_data):
    reals = ["BODYWEIGHTKG", "WEIGHTCLASSKG", "SQUAT1KG", "SQUAT2KG", "SQUAT3KG", "SQUAT4KG", "BEST3SQUATKG",
             "BENCH1KG", "BENCH2KG", "BENCH3KG", "BENCH4KG", "BEST3BENCHKG", "DEADLIFT1KG", "DEADLIFT2KG",
             "DEADLIFT3KG", "DEADLIFT4KG", "BEST3DEADLIFTKG", "TOTALKG", "PLACE", "DOTS", "WILKS", "GLOSSBRENNER",
             "GOODLIFT"]

    for meet in csv_data:
        for k, v in meet.items():
            if k in reals:
                meet[k] = float_cast(v)
            if not len(v):
                meet[k] = crud.NULL
            else:
                meet[k] = str_cast(v)
        #print(meet)   # DEBUG print

    return csv_data


class Database:
    def __init__(self, connection):
        self.over9000_headers = crud.OVER9000_HEADERS
        self.results_headers = crud.RESULTS_HEADERS
        self.conn = connection

    # TODO: abstract some of this to crud, crud.create() not doing anything righ now
    # create entry into OVER9000 and related entries into RESULTS
    def create_entry(self, lifter_id, csv_data):
        pass
        # csv_data = load_csv_data(get_csv_link(lifter_id))
        print("csv_data_as_dict: ", csv_data)  # DEBUG print

        # sql_data = crud.create_entry(lifter_id, csv_data)

        # OVER9000 table entry
        OVER9K_SQL_HEADERS = ",".join(self.over9000_headers)

        # cast into double quotes
        o9k_id = str_cast(lifter_id)
        o9k_name = str_cast(csv_data[0]["NAME"])
        o9k_csv = str_cast(csv_data[0]["CSV"])
        values_list = [o9k_id, o9k_name, o9k_csv, crud.NULL, crud.NULL]
        print("values list: ", values_list)  # DEBUG print
        OVER9K_SQL_VALUES = ",".join(values_list)

        sql_over9000_command = f"INSERT INTO {crud.OVER9000_TABLE} ({OVER9K_SQL_HEADERS}) " \
                               f"VALUES ({OVER9K_SQL_VALUES})"

        print("SQL_OVER9000_COMMAND: ", sql_over9000_command)  ## work on format_csv_data, values are not cast properly
        self.conn.execute(sql_over9000_command)
        self.conn.commit()

        # RESULTS table entries
        csv_data = format_csv_data(csv_data)
        RESULTS_SQL_HEADERS = ",".join(self.results_headers)
        for meet in csv_data:
            RESULTS_SQL_VALUES = ",".join(meet.values())

            sql_results_command = f"INSERT INTO {crud.RESULTS_TABLE} ({RESULTS_SQL_HEADERS}) " \
                                  f"VALUES ({RESULTS_SQL_VALUES})"

            print("SQL_RESULT_COMMAND: ", sql_results_command)
            self.conn.execute(sql_results_command)

        self.conn.commit()
        # CONTINUE here

    def read_entry(self, lifter_id):
        pass

    def update_entry(self, lifter_id, field, new_val):
        pass

    def delete_entry(self, lifter_id):
        pass

    def refresh_entry(self, lifter_id):
        pass
