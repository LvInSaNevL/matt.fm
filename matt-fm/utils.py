import json
import datetime

# data = utils.array_from_json_file("/foo/bar")
def array_from_json_file(path):
	array = {}
	with open(path, encoding='utf-8') as f:
		array = json.loads(f)
	return array

colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

# utils.prettyPrint('OKAYGREEN', "Hello, World!")
def prettyPrint(color, text):
    print(colors[color] + text + colors['ENDC'])

badness = ("log     ",
           "minor   ",
           "moderate",
           "major   ",
           "critical")

# utils.logPrint("Hello, World!", 1, 'log.txt')
def logPrint(message, severity, file='log.txt'):
    emptyLog = "[ {} ][ {} ]: {}"
    logfile = open(file, 'a+', encoding='utf-8')
    message = "[ {} ][ {} ]: {} \n".format(badness[severity], datetime.datetime.now(), message)
    prettyPrint('WARNING', message)
    logfile.write(message)

def readAuth(target):
    with open("auth.json") as jsonfile:
        auth = json.load(jsonfile)
    return auth[target]