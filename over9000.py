import crud


def create_db():
    pass


def load_db():
    pass


def get_open_data(link):
    pass


class Database:
    def __init__(self, connection):
        self.conn = connection

    def create_entry(self, lifter_id):
        pass

    def read_entry(self, lifter_id):
        pass

    def update_entry(self, lifter_id, field, new_val):
        pass

    def delete_entry(self, lifter_id):
        pass

    def refresh_entry(self, lifter_id):
        pass

