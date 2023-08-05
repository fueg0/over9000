from over9000 import *

if __name__ == '__main__':
    db = load_db()

    csv_link = get_csv_link(NF)
    print("LINK: ", NF)  # DEBUG print
    print("CSV LINK: ", csv_link)  # DEBUG print

    csv_data = load_csv_data(csv_link)
    formatted_csv_data = []
    for meet in csv_data:
        meet = format_csv_data(meet)
        meet["CSV"] = csv_link
        formatted_csv_data.append(meet)
    # add CSV link to data
    ## csv_data["CSV"] = csv_link
    print("Data from load_csv_data: \n", formatted_csv_data, "\n")

    db.create_entry(NF, formatted_csv_data)
    # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #               VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    # conn.execute("INSERT INTO OVER9000 (ID,NAME,AGE,ADDRESS,SALARY) \
    #               VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    exit(0)
