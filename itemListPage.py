import csv

from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient

import csv

client = MongoClient()  # Connect to the default MongoDB server
db = client['rainbowpages']  # Get a database named 'rainbowpages'
collection = db['interior']  # Get a collection named 'data'


def getItemDetails(category, sub_category1, url):

    sub_category_href_list = []
    baseUrl = url
    pageUrls = [url]
    data = {}

    with open(category+'.csv', 'w', newline='') as f:
        fieldnames = ['Sub Category', 'Name', 'Address', 'Telephone', 'Email', 'Website', 'Fax']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            category_data = bs(requests.get(url).text, 'html.parser')
            next_page_arrow = category_data.find("a", attrs={"aria-label": "Next"})

            if not next_page_arrow:
                break

            arrow_link = next_page_arrow['href'].split(' ')[0]

            sub_categories = category_data.find_all("h4", class_='media-heading')

            for sub_category in sub_categories:
                sub_category_href = sub_category.find('a')['href']
                sub_category_href_list.append(sub_category_href)

                datas = bs(requests.get(sub_category_href).text, 'html.parser')

                # Get name
                name_element = datas.find("h1", id='listing-profile-heading')
                name = name_element.text.strip() if name_element else ''

                try:
                    # Get address
                    contact_details_div = datas.find("div", class_='contact-details')
                    rows = contact_details_div.find_all("div", class_='row')
                except AttributeError as e:
                    print("Error: Contact details not found for sub-category:", sub_category_href)
                    print("Exception:", str(e))
                    continue

                data['Sub Category'] = sub_category1
                data['Name'] = name

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

            if arrow_link == '#':
                break

            next_url = baseUrl + arrow_link
            pageUrls.append(next_url)
            url = next_url

    print(data)





# def getItemDetails(category, sub_category1, url):
#
#     sub_category_href_list = []
#     baseUrl = url
#     pageUrls = [url]
#     data = {}
#
#     with open(category+'.csv', 'w', newline='') as f:
#         fieldnames = ['Sub Category', 'Name', 'Address', 'Telephone', 'Email', 'Website', 'Fax']
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         while True:
#             category_data = bs(requests.get(url).text, 'html.parser')
#             next_page_arrow = category_data.find("a", attrs={"aria-label": "Next"})
#
#             if not next_page_arrow:
#                 break
#
#             arrow_link = next_page_arrow['href'].split(' ')[0]
#
#             sub_categories = category_data.find_all("h4", class_='media-heading')
#
#             for sub_category in sub_categories:
#                 sub_category_href = sub_category.find('a')['href']
#                 sub_category_href_list.append(sub_category_href)
#
#                 datas = bs(requests.get(sub_category_href).text, 'html.parser')
#
#                 # Get name
#                 name_element = datas.find("h1", id='listing-profile-heading')
#                 name = name_element.text.strip() if name_element else ''
#
#                 # Get address
#                 contact_details_div = datas.find("div", class_='contact-details')
#                 rows = contact_details_div.find_all("div", class_='row')
#
#                 data['Sub Category'] = sub_category1
#                 data['Name'] = name
#
#                 for detail in rows:
#                     strong_name = detail.find("div", class_="col-md-12")
#                     detail_text = strong_name.find_next_sibling()
#
#                     key = strong_name.strong.text.strip()
#                     value = detail_text.text.strip() if detail_text else ''
#
#                     if key == "Email":
#                         detail_text = detail_text.find("a") if detail_text else None
#                         value = cfDecodeEmail(detail_text.get('href').replace('mailto:', '').split('#')[1]) if detail_text else ''
#
#
#                     if value:
#                         data[key] = value
#
#                 writer.writerow({'Sub Category': data.get('Sub Category', ''), 'Name': data.get('Name', ''),
#                                  'Address': data.get('Address', ''), 'Telephone': data.get('Telephone', ''),
#                                  'Email': data.get('Email', ''), 'Website': data.get('Website', ''),
#                                  'Fax': data.get('Fax', '')})
#                 print(data)
#                 collection.insert_one(data)
#                 data.clear()
#
#             if arrow_link == '#':
#                 break
#
#             next_url = baseUrl + arrow_link
#             pageUrls.append(next_url)
#             # print(next_url)
#             url = next_url
#
#     print(data)
#

# def getItemPageUrls(sub_category1, url):
#
#     sub_category_href_list = []
#     baseUrl = url
#     pageUrls = [url]
#     data = {}
#     with open('advertising.csv', 'w', newline='') as f:
#         fieldnames = ['Sub Category', 'Name', 'Address', 'Telephone', 'Email', 'Website', 'Fax']
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         while True:
#             category_data = bs(requests.get(url).text, 'html.parser')
#             next_page_arrow = category_data.find("a", attrs={"aria-label": "Next"})
#
#             if not next_page_arrow:
#                 break
#
#             arrow_link = next_page_arrow['href'].split(' ')[0]
#
#             sub_categories = category_data.find_all("h4", class_='media-heading')
#
#             for sub_category in sub_categories:
#                 sub_category_href = sub_category.find('a')['href']
#                 sub_category_href_list.append(sub_category_href)
#
#                 datas = bs(requests.get(sub_category_href).text, 'html.parser')
#
#                 # Get name
#                 name = datas.find("h1", id='listing-profile-heading').text.strip()
#
#                 # Get address
#                 contact_details_div = datas.find("div", class_='contact-details')
#                 rows = contact_details_div.find_all("div", class_='row')
#
#                 for detail in rows:
#                     strong_name = detail.find("div", class_="col-md-12")
#                     detail_text = strong_name.find_next_sibling()
#
#
#                     data['Sub Category'] = sub_category1
#                     data['Name'] = name
#
#                     key = strong_name.strong.text.strip()
#                     value = detail_text.text.strip()
#
#                     if key == "Email":
#                         detail_text = detail_text.find("a")
#                         value = cfDecodeEmail(detail_text.get('href').replace('mailto:', '').split('#')[1])
#
#                     data[key] = value
#
#                 writer.writerow({'Sub Category': data['Sub Category'], 'Name': data['Name'], 'Address': data['Address'],
#                                  'Telephone': data['Telephone'], 'Email': data['Email'], 'Website': data['Website']})
#                 print(data)
#
#             if arrow_link == '#':
#                 break
#
#             next_url = baseUrl + arrow_link
#             pageUrls.append(next_url)
#             # print(next_url)
#             url = next_url
#
#     print(data)
    # return pageUrls

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i + 2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

