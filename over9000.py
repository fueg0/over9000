import csv
from io import StringIO
import crud
import requests
from bs4 import BeautifulSoup

NF = "https://www.openpowerlifting.org/u/nicholasfiorito"


def load_db():
    conn = crud.setup_db()
    return Database(conn)


def get_csv_link(link):
    # Fetch the page
    response = requests.get(link)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the h2 tag with "Competition Results" text
    h2_tag = soup.find_all('h2')
    print(h2_tag)
    h2_tag = h2_tag[1]
    print(h2_tag)

    # Find the a tag within the h2 tag and get its href value
    csv_link = h2_tag.find('a')['href']

    print(csv_link)
    return csv_link


def load_csv_data(csv_link):
    full_link = "https://www.openpowerlifting.org" + csv_link
    # Get the CSV data
    response = requests.get('https://www.openpowerlifting.org' + csv_link)  # you may need to adjust the URL
    data = response.content.decode('utf-8')

    # Parse the CSV data into a dictionary
    reader = csv.DictReader(StringIO(data))
    rows = list(reader)

    # Now rows is a list of dictionaries, each dictionary represents a row in the CSV
    for row in rows:
        print(row)  # or do whatever you need to do with the row

    return rows


class Database:
    def __init__(self, connection):
        self.conn = connection

    def create_entry(self, lifter_id):
        pass
        csv_data_as_dict = load_csv_data(get_csv_link(lifter_id))
        sql_entry = crud.create_entry(lifter_id, csv_data_as_dict)
        # CONTINUE here

    def read_entry(self, lifter_id):
        pass

    def update_entry(self, lifter_id, field, new_val):
        pass

    def delete_entry(self, lifter_id):
        pass

    def refresh_entry(self, lifter_id):
        pass

