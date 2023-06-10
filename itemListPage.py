from bs4 import BeautifulSoup as bs
import requests
import singleItemPage


def getItemPageUrls(url):
    sub_category_href_list = []
    baseUrl = url
    pageUrls = [url]
    data = {}

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
            name = datas.find("h1", id='listing-profile-heading').text.strip()

            # Get address
            contact_details_div = datas.find("div", class_='contact-details')
            rows = contact_details_div.find_all("div", class_='row')

            for detail in rows:
                strong_name = detail.find("div", class_="col-md-12")
                detail_text = strong_name.find_next_sibling()


                data['Name'] = name

                key = strong_name.strong.text.strip()
                value = detail_text.text.strip()

                if key == "Email":
                    detail_text = detail_text.find("a")
                    value = cfDecodeEmail(detail_text.get('href').replace('mailto:', '').split('#')[1])

                data[key] = value
            print(data)

        if arrow_link == '#':
            break

        next_url = baseUrl + arrow_link
        pageUrls.append(next_url)
        # print(next_url)
        url = next_url

    print(data)
    # return pageUrls

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i + 2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email