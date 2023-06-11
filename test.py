from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient

import csv

client = MongoClient()  # Connect to the default MongoDB server
db = client['rainbowpages']  # Get a database named 'rainbowpages'
collection = db['constructions']  # Get a collection named 'data'


def singleItem(url):
    data = {}
    datas = bs(requests.get(url).text, 'html.parser')

    # Get name
    name_element = datas.find("h1", id='listing-profile-heading')
    name = name_element.text.strip() if name_element else ''

    try:
        # Get address
        contact_details_div = datas.find("div", class_='contact-details')
        rows = contact_details_div.find_all("div", class_='row')
    except AttributeError as e:
        print("Error: Contact details not found for sub-category:", url)
        print("Exception:", str(e))
        continue


    # data['Sub Category'] = sub_category1
    # data['Name'] = name

    for detail in rows:
        strong_name = detail.find("div", class_="col-md-12")
        detail_text = strong_name.find_next_sibling()

        key = strong_name.strong.text.strip()
        value = detail_text.text.strip() if detail_text else ''

        if key == "Email":
            detail_text = detail_text.find("a") if detail_text else None
            value = cfDecodeEmail(detail_text.get('href').replace('mailto:', '').split('#')[1]) if detail_text else ''

        if value:
            data[key] = value

    try:
        writer.writerow({'Sub Category': data.get('Sub Category', ''), 'Name': data.get('Name', ''),
                         'Address': data.get('Address', ''), 'Telephone': data.get('Telephone', ''),
                         'Email': data.get('Email', ''), 'Website': data.get('Website', ''),
                         'Fax': data.get('Fax', '')})
        print(data)
        collection.insert_one(data)
    except Exception as e:
        print("Error occurred while writing to CSV or inserting into MongoDB:")
        print("Exception:", str(e))

    data.clear()




def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i + 2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email