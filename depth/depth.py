import requests
from bs4 import BeautifulSoup
import time
import openpyxl


def dfs_depth(urls, depth, referer, whole_pages): 
  

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    if depth == 0: 
        return 
    for url in urls:
        if referer != "":
            headers["Referer"] = referer
        try:
            response = requests.get(url, headers=headers)
        except:
            continue
        response.close()
        soup = BeautifulSoup(response.content, "html.parser")

        links = []

        for a in soup.findAll("a"):
            try:
                href = a['href']
                if href.startswith('#') or href.startswith('javascript:') or len(href) == 0:
                    continue
                if href.startswith('//'):
                    href = "https:" + href
                elif href.startswith('/'):
                    href = url + href
                if href.startswith('http') and href not in links:
                    if href not in whole_pages:
                        whole_pages.append(href)
                        links.append(href)
            except:
                continue

        time.sleep(1)

    print("\t[ " + str(depth) + " ]\t")
    depth -= 1
    
    if len(links) > 0:  #크롤링할 링크목록이 남아있다면
        links = list(set(links)) 
        dfs_depth(links, depth, referer=url, whole_pages=whole_pages)


if __name__ == "__main__":
    sites = ["https://www.starbucks.co.kr/"]
    referer = ""
    cookie = ""
    whole_pages = []
    dfs_depth(sites, 3, referer, whole_pages)

    print(whole_pages)

    book = openpyxl.Workbook()
    sheet = book.create_sheet()
    for addr in whole_pages:
        sheet.append([addr])
    book.save("result.xlsx")
    book.close()
