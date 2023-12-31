from bs4 import BeautifulSoup as bs
import requests
import itemListPage
import csv

def scrapeData(category, url):

    soup = bs(requests.get(url).text, 'html.parser')

    sub_categories = soup.find_all("h4", class_='category-title')

    for sub_category in sub_categories:
        sub_category_href = sub_category.find('a')['href']

        sub_category_name = sub_category.find('a').text.strip()

        itemListPage.getItemDetails(category, sub_category_name, sub_category_href)


















# def singleItemData(url):
#     response = requests.get(url)
#     data = bs(response.text, 'html.parser')
#
#     # Get name
#     name = data.find("h1", id='listing-profile-heading').text.strip()
#
#     # Get address
#     contact_details_div = data.find("div", class_='contact-details')
#     rows = contact_details_div.find_all("div", class_='row')
#
#     data = {}
#
#     for detail in rows:
#         strong_name = detail.find("div", class_="col-md-12")
#         detail_text = strong_name.find_next_sibling()
#
#         key = strong_name.strong.text.strip()
#         value = detail_text.text.strip()
#
#         if key == "Email":
#             detail_text = detail_text.find("a")
#             value = cfDecodeEmail(detail_text.get('href').replace('mailto:', '').split('#')[1])
#
#         data[key] = value
#
#     return data
#
#
# def cfDecodeEmail(encodedString):
#     r = int(encodedString[:2], 16)
#     email = ''.join([chr(int(encodedString[i:i + 2], 16) ^ r) for i in range(2, len(encodedString), 2)])
#     return email
