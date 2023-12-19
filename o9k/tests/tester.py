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
    csv_link = db.get_csv_link(NF)
    print("LINK: ", NF)  # DEBUG print
    print("CSV LINK: ", csv_link)  # DEBUG print

    test_create_operation_INPUT = [NF]

    test_create_operation(test_create_operation_INPUT)
    test_db = db.Database()
    o9k_res = test_db.conn.execute("SELECT ID, NAME, CSV from USERS")

    select_query = "SELECT Name,Sex,Division,BodyweightKG,WeightClassKg,Squat2Kg,Bench2Kg,Deadlift2Kg,MeetID from RESULTS where CSV = ?"
    res = test_db.conn.execute(select_query, (csv_link,))

    print("\nRESULTS\n")

    for row in res:
        print(row)  # DEBUG print

    test_db.conn.close()



