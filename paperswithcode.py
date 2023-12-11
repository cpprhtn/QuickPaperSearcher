import requests
from bs4 import BeautifulSoup
import pandas as pd

def url_to_soup(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

url = "https://paperswithcode.com"
soup = url_to_soup(url)

# 논문 제목과 링크 경로 가져오기
# paper_div = soup.find("div", class_="row infinite-item item paper-card")
# paper_title = paper_div.find("h1").find("a").text.strip()
# paper_link = paper_div.find("h1").find("a")["href"]

# print("제목:", paper_title)
# print("링크 경로:", paper_link)
a_tag = soup.find_all("div", class_="row infinite-item item paper-card")#.find("a")
print(len(a_tag))

titles = []
authors_list = []
abstracts = []

for i in a_tag:
    path = i.find("a").get("href")
    # print(path)
    soup = url_to_soup(url+path)
    # print(soup)
    title = soup.find('h1').get_text(strip=True)
    authors = soup.find_all('span', class_='author-span')[1:]
    authors = [i.get_text(strip=True) for i in authors]
    abstract = soup.find('div', class_='paper-abstract').get_text(strip=True)

    titles.append(title)
    authors_list.append(authors)
    abstracts.append(abstract[:-11])
    # break

# Create a DataFrame
data = {
    'Title': titles,
    'Authors': authors_list,
    'Abstract': abstracts
}

df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
df.to_csv(f'paperswithcode.csv', index=False)