import re
import logging

data = {}
logger = logging.getLogger(__name__)

def get_message(msg: str):
    try:
        ap = re.split('(?<!\\\\)(?:\\\\\\\\)*;', msg)
        mid = str(ap[0])
        if mid in data:
            dp = str(data[mid])
            for i in range(1, len(ap)):
                dp = dp.replace("%%" + str(i) + "%%", str(ap[i].replace("\\", "")))
            return dp
        else:
            mid = str(mid)
            logger.warning("Someone requested message id " + mid + " but it's not avaiable.")
            return "The requested message (" + mid + ") wasn't found"
    except Exception as e:
        logger.critical("An exception occured: " + str(e) + " while looking up a message.")
        return "Due to an exception the requested message couldn't be displayed"


def load_in_data(msgfile: str):
    import csv
    with open(msgfile, "r") as csvfile:
        datareader=csv.reader(csvfile, delimiter=';')
        for row in datareader:
            key = str(row[0])
            msg = str(row[1])
            data[str(key)] = str(msg)
    pass
