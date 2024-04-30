import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import openpyxl
import time
import requests

book = openpyxl.Workbook() # openpyxl에 새 시트를 만들고 
sheet = book.create_sheet()


from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links(url):
        links = []
        try :
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.findAll("a"):
                try :
                    href = a['href']
                    if href.startswith('#') or href.startswith('javascript:') or len(href) == 0:
                        continue
                    if href.startswith('//'):
                        href = "https:" + href
                    elif href.startswith('/'):
                        href = url + href
                    if href.startswith('http') and href not in url:
                            links.append(href)
                        
                except Exception as e:
                     print("Error1:", e)
        except Exception as e:
            print("Error2:", e)
        return links

def crawl_site(url, depth):
    if depth == 0:
        return []

    links_to_visit = get_links(url)
    if links_to_visit is None:
         return []
    
    child_links = []

    for link in links_to_visit:
        abs_link = urljoin(url, link)
        child_links.append((abs_link, depth))

        if depth > 1:
            child_links.extend(crawl_site(abs_link, depth - 1))

    return child_links

if __name__ == "__main__":
    start_url = "https://www.starbucks.co.kr/index.do"  # 시작할 URL
    depth = 2 # 크롤링 깊이

    crawled_links = crawl_site(start_url, depth)

    # 결과 출력
    print("Crawled Links:")
    for links, depth in crawled_links:
        print(f"{links} | Depth: {depth}")

        sheet.append([links])
    book.save("result.xlsx")
    book.close()