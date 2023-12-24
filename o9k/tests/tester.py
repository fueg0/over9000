from o9k.o9k_utils import utils
from o9k.database import db
from o9k.cli import py_console

# hot damn maybe school was right about writing unit tests
NF = "https://www.openpowerlifting.org/u/nicholasfiorito"
WS = "https://www.openpowerlifting.org/u/walisiddiqui"

DEBUG = False


# test create entry
def test_create_operation(op_link, debug=DEBUG):
    utils.debug_print(f"test_create_operation:: \nopenpowerlifting link: {op_link}", debug)
    db_test = py_console.init_o9k()

    db_test.create_entry(op_link)

    # assert for row, match MEET_ID to correct formatted_csv_data meet
    # assert NAME
    # assert SEX
    # assert EVENT
    # assert EQUIPMENT
    # assert AGE
    # assert AGECLASS
    # assert BIRTHYEARCLASS
    # assert DIVISION
    # assert BODYWEIGHTKG
    # assert WEIGHTCLASSKG
    # assert SQUAT1KG


def test_console(op_link, debug=DEBUG):
    utils.debug_print(f"test_console:: \nopenpowerlifting link: {op_link}", debug)
    db_test = py_console.init_o9k()

    db_test.create_entry(op_link)

    # assert for row, match MEET_ID to correct formatted_csv_data meet
    # assert NAME
    # assert SEX
    # assert EVENT
    # assert EQUIPMENT
    # assert AGE
    # assert AGECLASS
    # assert BIRTHYEARCLASS
    # assert DIVISION
    # assert BODYWEIGHTKG
    # assert WEIGHTCLASSKG
    # assert SQUAT1KG


if __name__ == '__main__':
    # CREATE
    # Create entry in DB
    links = ["https://www.openpowerlifting.org/u/nicholasfiorito",
             "https://www.openpowerlifting.org/u/walisiddiqui",
             "https://www.openpowerlifting.org/u/thomaszuccarello",
             "https://www.openpowerlifting.org/u/louieliu",
             "https://www.openpowerlifting.org/u/katedriscoll",
             "https://www.openpowerlifting.org/u/duncanmichaud"
             ]
    for link in links:
        csv_link = db.get_csv_link(link)
        print("LINK: ", link)  # DEBUG print
        print("CSV LINK: ", csv_link)  # DEBUG print

        test_create_operation_INPUT = [link]

        test_create_operation(test_create_operation_INPUT)
        test_db = db.Database()
        o9k_res = test_db.conn.execute("SELECT ID, NAME, CSV from USERS")

        select_query = f"SELECT Squat2Kg, Bench2Kg, Deadlift2Kg, MeetID from RESULTS"
        res = test_db.conn.execute(select_query)

        print("\nRESULTS\n")

        for row in o9k_res:
            print(row)  # DEBUG print

        for row in res:
            print(row)  # DEBUG print

        test_db.conn.close()

    test_db = db.Database()

    print("TEST READ")
    fields = ["Squat2Kg", "Bench2Kg", "Deadlift2Kg", "MeetID"]
    res_results = test_db.read_entry(csv_link, fields, "RESULTS")
    for res in res_results:
        print(res)

    fields = ["NAME", "CSV", "TEAM"]
    user_results = test_db.read_entry(csv_link, fields, "USERS")
    for res in user_results:
        print(res)

    print("TEST UPDATE")
    meet_id = 'Nicholas Fiorito - Raw Collegiate Cup and Massachusetts Collegiate States - MR-C'
    fields = ["Name"]
    new_vals = ["Nick Fuego"]
    table = "RESULTS"
    update_res = test_db.update_entry(meet_id, fields, new_vals, table)
    for res in update_res:
        print(res)

    meet_id = csv_link
    fields = ["NAME"]
    new_vals = ["Nick Fuego"]
    table = "USERS"
    update_res = test_db.update_entry(meet_id, fields, new_vals, table)
    for res in update_res:
        print(res)

    test_db.conn.close()
