import o9k.database.db as db
import o9k.o9k_utils.utils as utils

NF = "https://www.openpowerlifting.org/u/nicholasfiorito"
WS = "https://www.openpowerlifting.org/u/walisiddiqui"

usage_msg = "Usage:\n \
          C | CREATE [openpowerlifting link, ...]\n \
          R | READ [openpowerlifting link, ...]\n \
          U | UPDATE [openpowerlifting link]\n \
          D | DELETE [openpowerlifting link, ...]\n \
          E | EXIT\n\n"

create = ["C", "CREATE"]
read = ["R", "READ"]
update = ["U", "UPDATE"]
delete = ["D", "DELETE"]
ex = ["E", "EXIT"]


def float_cast(value):
    return str(value)


def error_msg(msg):
    print(msg)
    print(usage_msg)


def init_o9k(database=None):
    print(f'Welcome to Over9000\n\n')
    print("Initialzing database...")
    main_db = db.Database(database)
    print(usage_msg)

    return main_db


def main():
    main_db = init_o9k(database="pyconsole_over9000.db")

    while True:
        op = input("give an operation:\n").split(" ")

        if op[0] in create:
            if len(op) > 2:
                link = op[1:]
            elif len(op) == 2:
                link = [op[1]]
            else:
                error_msg("Provide at least one openpowerlifting link to CREATE / C")
                continue
            res = main_db.create_entry(link)
            print(res)
            continue
        if op[0] in read:
            if len(op) > 2:
                link = op[1:]
            elif len(op) == 2:
                link = list(op[1])
            else:
                link = "*"
            res = main_db.read_entry(link, link, "RESULTS")
            for result in res:
                print(result)
            continue
        if op[0] in update:
            pass
        if op[0] in delete:
            pass
        if op[0] in ex:
            break
        else:
            error_msg("unsupported operation")
            continue
    print("Exiting Over9000")
    main_db.conn.close()


def single_main():
    main_db = init_o9k()

    while True:
        op = input("give an operation:\n").split()

        if op[0] in create:
            if len(op) > 2:
                link = op[1:]
            elif len(op) == 2:
                link = list(op[1])
            else:
                error_msg("Provide at least one openpowerlifting link to CREATE / C")
                continue
            res = main_db.create_entry(link)
            print(res)
            break
        if op[0] in read:
            break
        if op[0] in update:
            break
        if op[0] in delete:
            break
        if op[0] in ex:
            exit(1000)
        else:
            error_msg("unsupported operation")
            break

        print("Exiting Over9000")
        main_db.conn.close()
        exit(int(111))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
