import requests
from bs4 import BeautifulSoup
import pandas as pd

def url_to_soup(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


url = input("URL을 입력하세요: ")
sota = url[26:]
soup = url_to_soup(url)

a_tag = soup.find_all("div", class_="paper-card infinite-item")#.find("a")
print(len(a_tag))

titles = []
authors_list = []
abstracts = []

for i in a_tag:
    path = i.find("a").get("href")
    # print(path)
    soup = url_to_soup(url[:26]+path)
    title = soup.find('div', class_='paper-title').find('h1').get_text(strip=True)
    # print(title)
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
df.to_csv(f'paperswithcode_{sota[6:]}.csv', index=False)