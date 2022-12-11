from pdfminer.layout import (
    LAParams, LTTextBox, LTChar, LTText, LTRect, LTTextBoxHorizontal,
    LTTextLineHorizontal
)

from collections import defaultdict
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

import matplotlib.pyplot as plt
import cv2
import re
import json
import numpy as np
from matplotlib.patches import Rectangle

def extract_rows(filename, visualize=False) -> list:
    rows = []
    with open(filename, 'rb') as f:
        # Create a PDF resource manager
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        rows = defaultdict(lambda: [])
        for page_no, page in enumerate(PDFPage.get_pages(f), start=1):
            x0, y0, x1, y1 = page.mediabox
            width = x1 - x0
            height = y1 - y0
            interpreter.process_page(page)
            layout = device.get_result()
            text_objects = []
            for obj in layout:
                if isinstance(obj, LTTextBox):
                    for o in obj._objs:
                        if isinstance(o, LTTextLineHorizontal):
                            x0, y0, x1, y1 = o.bbox
                            y0 = height - y0
                            y1 = height - y1
                            text_objects.append(o)
                            # cv2.rectangle(
                            #     img, (int(x1), int(y1)), (int(x0), int(y0)),
                            #     (255, 255, 255), 1
                            # )
            # extract the text and map them to a row
            for text_object in text_objects:
                x0, y0, x1, y1 = text_object.bbox
                text = text_object.get_text()
                y0 = height - y0
                y1 = height - y1
                middle = y1 - y0 // 2
                rows[int(middle + (page_no * height))].append(text)
    # sort the rows based on key form lowest to highest
    sorted_rows = sorted(rows.items(), key=lambda x: x[0])
    return sorted_rows


# Open the PDF file
def extract_page_content(filename, visualize=False) -> dict:
    rows = extract_rows(filename, visualize)

    data_dict = {
        'id':0,
        'store_name':'',
        'product_columns':[],
        'products':[],
        'date':'',
        'total':0
    }

    add_product = False
    for row in rows:
        row = list(map(lambda x: x.strip(), row[1]))
        if 'Beskrivning' in row[0]:
            add_product = True
            data_dict['product_columns'] = row
            continue

        if 'Total:' in row[0]:
            data_dict['total'] = float(row[1])
            add_product = False
        
        if add_product and (len(row) == 5):
            row[2] = float(row[2])
            row[4] = float(row[4])
            data_dict['products'].append(row)

        receipt_id = re.findall(r'\d{25}', row[0])
        if receipt_id:
            data_dict['id'] = receipt_id[0]

        # regex to find this date: 2022-11-06
        date = re.findall(r'\d{4}-\d{2}-\d{2}', row[0])
        if date:
            data_dict['date'] = date[0]
    
    return data_dict
    # convert data_dict to json and print with tabs=4
    # print(json.dumps(data_dict, indent=4, ensure_ascii=False))
        


    # cv2.imshow('image', img)
    # cv2.waitKey(0)