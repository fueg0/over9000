# MAIN
import over9000
STATES_GROUP = ["EXIT", "ERROR", "STARTING", "RUNNING", "WAITING", "CREATE", "READ", "UPDATE", "DELETE", "REFRESH", "UNSTARTED"]
STATE = "UNSTARTED"

if __name__ == '__main__':
    while STATES_GROUP.index(STATE) > 0:
        pass
        # switch case state maching for DB until exit or error