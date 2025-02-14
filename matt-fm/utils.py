import json
import datetime
import sys
import uuid

# data = utils.array_from_json_file("/foo/bar")
def array_from_json_file(path):
	array = {}
	with open(path, encoding='utf-8') as f:
		array = json.loads(f)
	return array

colors = [
    ('HEADER', '\033[95m'),
    ('OKBLUE', '\033[94m'),
    ('OKGREEN', '\033[92m'),
    ('WARNING', '\033[93m'),
    ('FAIL', '\033[91m'),
    ('ENDC', '\033[0m'),
    ('BOLD', '\033[1m'),
    ('UNDERLINE', '\033[4m')
]

# utils.prettyPrint('OKAYGREEN', "Hello, World!")
def prettyPrint(color, text):
    print(colors[color][1] + text + colors[5][1])

badness = ("log     ",
           "minor   ",
           "moderate",
           "major   ",
           "critical")


def logPrint(message, severity, file='log.txt'):
    '''
    <summary>

    Writes a message out to both the terminal (in a color, see the table below), as
    well as in a log file. By default it is `log.txt` but it can be changed by passing
    a file path in the `file` argument. 

    | Index | Severity | Colors |
    | ----- | -------- | ------ |
    |   0   | Log      | Blue   |
    |   1   | Minor    | Green  |
    |   2   | Moderate | Yellow | 
    |   3   | Major    | Red    |
    |   4   | Critical | White  |

    Note: A critical message (4) will also terminate the program
    '''
    emptyLog = "[ {} ][ {} ]: {}"
    logfile = open(file, 'a+', encoding='utf-8')
    message = "[ {} ][ {} ]: {} \n".format(badness[severity], datetime.datetime.now(), message)
    prettyPrint((severity + 1), message)
    logfile.write(message)
    if (severity == 4):
        sys.exit()

def readAuth(target):
    with open("auth.json") as jsonfile:
        auth = json.load(jsonfile)
    return auth[target]

def genUUID(length=8):
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","")
    return str(random[0:length])

def last_index(input_list:list) -> int:
    return len(input_list) - 1