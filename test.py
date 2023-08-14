from database.over9000 import *

# hot damn maybe school was right about writing unit tests


# test create entry
def test_create_operation(database_object):
    db = database_object

    # CREATE
    # Create entry in DB
    csv_link = get_csv_link(NF)
    print("LINK: ", NF)  # DEBUG print
    print("CSV LINK: ", csv_link)  # DEBUG print

    csv_data = load_csv_data(csv_link)
    formatted_csv_data = []
    for meet in csv_data:
        meet = format_csv_headers(meet)
        meet["CSV"] = csv_link
        meet["MEET_ID"] = " ".join([meet["MEETNAME"], meet["DIVISION"]])
        formatted_csv_data.append(meet)
    # add CSV link to data
    ## csv_data["CSV"] = csv_link
    print("Data from load_csv_data: \n", formatted_csv_data, "\n")

    db.create_entry(NF, formatted_csv_data)
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    # assert ID = NF
    # assert NAME = formatted_csv_data["NAME"]
    # assert CSV = formatted_csv_data["CSV"]

    # READ
    # Read data from DB
    print("\nAFTER SELECT: \nOVER9000\n")  # DEBUG print

    for row in o9k_res:
        print(row)  # DEBUG print

    res = db.conn.execute("SELECT NAME,SEX,EVENT,EQUIPMENT,AGE,AGECLASS,BIRTHYEARCLASS,DIVISION,BODYWEIGHTKG,"
                          "WEIGHTCLASSKG,SQUAT1KG, MEET_ID from RESULTS")

    print("\nRESULTS\n")

    for row in res:
        print(row)  # DEBUG print

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
    db.conn.close()


def test_update_operation(database):
    db = database

    # UPDATE
    # Update value in DB
    print("\n update\n")
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    for lifter in o9k_res:
        # NOTE: NEEDS STR_CAST HERE BECAUSE OF THE DAMN COLON
        # NOTE: I should look into fix this casting thing. I forsee many errors in the future
        lifter_id = str_cast(lifter[0])
        print(lifter)  # DEBUG print
        print(lifter_id)  # DEBUG print
        new_val = str_cast("Nicholas Fuego")
        print(new_val)  # DEBUG print
        update_cmd = f"UPDATE OVER9000 set NAME = {new_val} where ID = {lifter_id}"
        print(update_cmd)  # DEBUG print
        # TODO: update name in results pivot for all results matching CSV
        db.conn.execute(update_cmd)
        print("Total number of rows updated :", db.conn.total_changes)
        db.conn.commit()

        update_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

        # assert len = 1 (should not be matching more than one lifter_id)
        # assert NAME == new NAME (set name as var)

        # UPDATE TEST
        # Select data from Db
        print("\nAFTER UPDATE: \nOVER9000\n")  # DEBUG print

        for row in update_res:
            print(row)  # DEBUG print

        print("restore name")
        db.conn.execute(f"UPDATE OVER9000 set NAME = \"Nicholas Fiorito\" where ID = {lifter_id}")
        db.conn.commit()

    # Check update revert worked
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    # assert len = 1 (should not be matching more than one lifter_id)
    # assert NAME == new NAME (set name as var)


    for row in o9k_res:
        print(row)  # DEBUG print

    db.conn.close()


def test_delete_operation(database):
    db = database
    print("delete")

    csv_link = get_csv_link(WS)
    print("LINK: ", WS)  # DEBUG print
    print("CSV LINK: ", csv_link)  # DEBUG print

    csv_data = load_csv_data(csv_link)
    formatted_csv_data = []
    for meet in csv_data:
        meet = format_csv_headers(meet)
        meet["CSV"] = csv_link
        meet["MEET_ID"] = " ".join([meet["MEETNAME"], meet["DIVISION"]])
        formatted_csv_data.append(meet)
    # add CSV link to data
    ## csv_data["CSV"] = csv_link
    print("Data from load_csv_data: \n", formatted_csv_data, "\n")

    db.create_entry(WS, formatted_csv_data)
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    print("\nAFTER SELECT: \nOVER9000\n")  # DEBUG print

    for row in o9k_res:
        print(row)  # DEBUG print

    db.conn.execute(f"DELETE from OVER9000 where ID = {str_cast(WS)};")
    print("Total number of rows updated OVER9000 :", db.conn.total_changes)


    db.conn.execute(f"DELETE from RESULTS where CSV = {str_cast(csv_link)};")
    print("Total number of rows updated RESULTS :", db.conn.total_changes)

    del_o9k_res = db.conn.execute("SELECT * from OVER9000")
    for row in del_o9k_res:
        print(row)  # DEBUG print
    del_results_res = db.conn.execute("SELECT * from RESULTS")
    for row in del_results_res:
        print(row)  # DEBUG print

    db.conn.commit()
    db.conn.close()



if __name__ == '__main__':
    # LOAD
    # Load/Connect to DB
    db = load_db()

    # CREATE
    # Create entry in DB
    csv_link = get_csv_link(NF)
    print("LINK: ", NF)  # DEBUG print
    print("CSV LINK: ", csv_link)  # DEBUG print

    csv_data = load_csv_data(csv_link)
    formatted_csv_data = []
    for meet in csv_data:
        meet = format_csv_headers(meet)
        meet["CSV"] = csv_link
        meet["MEET_ID"] = " ".join([meet["MEETNAME"], meet["DIVISION"]])
        formatted_csv_data.append(meet)
    # add CSV link to data
    ## csv_data["CSV"] = csv_link
    print("Data from load_csv_data: \n", formatted_csv_data, "\n")

    db.create_entry(NF, formatted_csv_data)
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    # SELECT
    # Select data from Db
    print("\nAFTER SELECT: \nOVER9000\n")  # DEBUG print

    for row in o9k_res:
        print(row)  # DEBUG print

    res = db.conn.execute("SELECT NAME,SEX,EVENT,EQUIPMENT,AGE,AGECLASS,BIRTHYEARCLASS,DIVISION,BODYWEIGHTKG,"
                          "WEIGHTCLASSKG,SQUAT1KG from RESULTS")

    print("\nRESULTS\n")

    for row in res:
        print(row)  # DEBUG print

    # UPDATE
    # Update value in DB
    print("\n update\n")
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    for lifter in o9k_res:
        # NOTE: NEEDS STR_CAST HERE BECASUE OF THE DAMN COLON
        lifter_id = str_cast(lifter[0])
        print(lifter)  # DEBUG print
        print(lifter_id)  # DEBUG print
        new_val = str_cast("Nicholas Fuego")
        print(new_val)  # DEBUG print
        update_cmd = f"UPDATE OVER9000 set NAME = {new_val} where ID = {lifter_id}"
        print(update_cmd)  # DEBUG print
        # TODO: update name in results pivot
        db.conn.execute(update_cmd)
        print("Total number of rows updated :", db.conn.total_changes)

        update_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")
        db.conn.commit()

        # UPDATE TEST
        # Select data from Db
        print("\nAFTER UPDATE: \nOVER9000\n")  # DEBUG print

        for row in update_res:
            print(row)  # DEBUG print

        print("reset name")
        update_res = db.conn.execute(f"UPDATE OVER9000 set NAME = \"Nicholas Fiorito\" where ID = {lifter_id}")
        db.conn.commit()

    # Check update revert worked
    o9k_res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")

    for row in o9k_res:
        print(row)  # DEBUG print

    test_delete_operation(db)

    # DELETE
    # Delete entry in DB

    db.conn.close()
    exit(0)
