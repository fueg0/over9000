from over9000 import *

if __name__ == '__main__':
    db = load_db()

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
    res = db.conn.execute("SELECT ID, NAME, CSV from OVER9000")
    for row in res:
        print(row)  # DEBUG print
    res = db.conn.execute("SELECT NAME,SEX,EVENT,EQUIPMENT,AGE,AGECLASS,BIRTHYEARCLASS,DIVISION,BODYWEIGHTKG,"
                          "WEIGHTCLASSKG,SQUAT1KG from RESULTS")
    for row in res:
        print(row)  # DEBUG print
    # EXAMPLE ENTRY:
    # conn.execute("INSERT INTO OVER9000 (ID,NAME,AGE,ADDRESS,SALARY) \
    #               VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    exit(0)
