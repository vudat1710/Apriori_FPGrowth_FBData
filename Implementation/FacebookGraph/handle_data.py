import json, csv
import pandas as pd 

def handle(filepath):

    with open(filepath, 'r') as f:
        data = json.load(f)
    f.close()

    with open('likes2.csv', 'w') as f:    
        f_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for user_id in data.keys():
            f_writer.writerow(user_id + ' ' + data[user_id])
    f.close()

def handle2(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    f.close()

    with open('likes2.csv', 'w') as f:
        for user_id in data.keys():
            f.write(user_id + ' {' + ','.join(data[user_id]) + '}\n')
    f.close()

handle2('likes.json')

