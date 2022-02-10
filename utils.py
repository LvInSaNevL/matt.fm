from datetime import datetime


badness = ("log     ",
           "minor   ",
           "moderate",
           "major   ",
           "critical")

def logPrint(message, severity):
    emptyLog = "[ {} ][ {} ]: {}"
    logfile = open('log.txt', 'a')
    logfile.write("[ {} ][ {} ]: {} \n".format(badness[severity], datetime.now(), message))