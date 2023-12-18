import db

NF = "https://www.openpowerlifting.org/u/nicholasfiorito"
WS = "https://www.openpowerlifting.org/u/walisiddiqui"

usage_msg = "Usage:\n \
          C | CREATE [openpowerlifting link, ...]\n \
          R | READ [openpowerlifting link, ...]\n \
          U | UPDATE [openpowerlifting link]\n \
          D | DELETE [openpowerlifting link, ...]\n \
          E | EXIT\n\n"


def load_db():
    conn = db.Database()
    return conn


def float_cast(value):
    return str(value)


def error_msg(msg):
    print(msg)
    print(usage_msg)


def main():
    create = ["C", "CREATE"]
    read = ["R", "READ"]
    update = ["U", "UPDATE"]
    delete = ["D", "DELETE"]
    ex = ["E"]
    print(f'Welcome to Over9000\n\n')
    print("Initialzing database...")

    main_db = load_db()

    print(usage_msg)

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
        if op[0] in read:
            pass
        if op[0] in update:
            pass
        if op[0] in delete:
            pass
        if op[0] in ex:
            exit(1000)
        else:
            error_msg("unsupported operation")
            continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
