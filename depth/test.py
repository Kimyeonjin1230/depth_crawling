import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import openpyxl
import time

book = openpyxl.Workbook() # openpyxl에 새 시트를 만들고 
sheet = book.create_sheet()

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        return links
    except Exception as e:
        print("Error:", e)
        return []

def crawl_site(url, depth):
    if depth == 0:
        return []

    links_to_visit = get_links(url)
    child_links = []

    for link in links_to_visit:
        abs_link = urljoin(url, link)
        child_links.append(abs_link)

        if depth > 1:
            child_links.extend(crawl_site(abs_link, depth - 1))

    return child_links

if __name__ == "__main__":
    start_url = "https://www.starbucks.co.kr/index.do/"  # 시작할 URL
    depth = 2  # 크롤링 깊이

    crawled_links = crawl_site(start_url, depth)

    # 결과 출력
    print("Crawled Links:")
    for link in crawled_links:
        print(link)

        sheet.append([link])
    book.save("result.xlsx")
    book.close()
