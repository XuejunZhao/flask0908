import json
import time


with open('data.json') as json_file:
    data = json.load(json_file)
    print data
