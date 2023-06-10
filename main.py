import singleItemPage
import itemListPage

if __name__ == '__main__':
    url = 'https://rainbowpages.lk/advertising/'
    # itemListPage.getItemPageUrls(url)
    singleItemPage.loadCategories(url)


# from bs4 import BeautifulSoup as bs
# import requests
#
# main_url = "https://rainbowpages.lk/"
# respnse = requests.get(main_url)
#
# soup = bs(respnse.text, 'html.parser')
#
# # -----------------Get all categories-----------------
#
# items = soup.find_all("div", class_='category-item')
#
# get_category_url = lambda category_name: [item.find('a')['href'] for item in items if
#                                           item.text.strip() == category_name]
#
# for item in items:
#     category_name = item.text.strip()
#
#     category_url = get_category_url(category_name)
#
#     full_url = main_url + category_url[0]
#
#     print(full_url)
#
#     # Category page
#
#     category_response = requests.get(full_url)
#     category_data = bs(category_response.text, 'html.parser')
#
#     sub_categories = category_data.find_all("h4", class_='category-title')
#
#     for sub_category in sub_categories:
#         sub_category_href = sub_category.find('a')['href']
#
#         print(sub_category_href)
#
#         # Sub Category page
#
#         sub_category_response = requests.get(sub_category_href)
#         sub_category_data = bs(sub_category_response.text, 'html.parser')
#
#         sub_category_items = sub_category_data.find_all("h4", class_='media-heading')
#
#         next_page_arrow = sub_category_data.find("a", attrs={"aria-label": "Next"})
#         arrow_link = next_page_arrow['href']
#
#         if arrow_link != '#':
#             next_page_link = sub_category_href + arrow_link
#             print(next_page_link)
#
#             for sub_category_item in sub_category_items:
#                 sub_category_item_href = sub_category_item.find('a')['href']
#
#                 # print(sub_category_item_href)
#
#                 sub_category_item_response = requests.get(sub_category_item_href)
#                 sub_category_item_data = bs(sub_category_item_response.text, 'html.parser')
#
#                 sub_category_item_name = sub_category_item_data.find("h1", id='listing-profile-heading')
#
#                 print(sub_category_item_name.text.strip())
#
#             # details inside the sub category item
#
#         print('-----------------')
#
#
#
#
#
#
#
#
#
# # -----------------Get all categories-----------------
#
# # print(soup.prettify())
