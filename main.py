import cv2
import os
import json

from parser import extract_page_content

# create the dir "unparsed" if it does not exists
if not os.path.exists('unparsed'):
    os.makedirs('unparsed')

if not os.path.exists('parsed'):
    os.makedirs('parsed')

# create database.json if it does not exist
if not os.path.exists('database.json'):
    with open('database.json', 'w') as f:
        json.dump([], f)

file_names = os.listdir('unparsed')

for filename in file_names:
    print(f'Parsing: {filename}')
    data_dict = extract_page_content(os.path.join('unparsed', filename))

    # read and write to json file
    with open('database.json', 'r') as f:
        list_of_receipts = list(json.load(f))

    add_receipt = True
    for receipt in list_of_receipts:
        if receipt['id'] == data_dict['id']:
            print('receipt already parsed')
            add_receipt = False
        
    if add_receipt:
        list_of_receipts.append(data_dict)
        with open('database.json', 'w') as f:
            json.dump(list_of_receipts, f, indent=4, ensure_ascii=False)

        # move the file to the folder for parsed receipts
        os.rename(
            os.path.join('unparsed', filename), os.path.join('parsed', filename)
        )
