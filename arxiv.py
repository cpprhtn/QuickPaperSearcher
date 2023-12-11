import requests
from bs4 import BeautifulSoup
import pandas as pd

search = input("What paper do you want to search? ")
# 웹페이지 URL
url = f"https://arxiv.org/search/?query={search}&searchtype=all&abstracts=show&order=-announced_date_first&size=50"

# 웹페이지 내용 가져오기
response = requests.get(url)
html_content = response.text

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 'arxiv-result' 클래스를 가진 모든 항목 찾기
arxiv_results = soup.find_all('li', class_='arxiv-result')

print("검색 결과 수: ", len(arxiv_results))

# Initialize lists to store data
titles = []
authors_list = []
abstracts = []

for result in arxiv_results:
    # 논문 제목 찾기
    title = result.find('p', class_='title is-5 mathjax').get_text(strip=True)
    
    # 저자 찾기
    authors = result.find('p', class_='authors').get_text(strip=True).replace('Authors:', '').split(', ')
    
    # Abstract 찾기
    abstract = result.find('p', class_='abstract mathjax').find('span', class_='abstract-full').get_text(strip=True)

    # Append data to lists
    titles.append(title)
    authors_list.append(authors)
    abstracts.append(abstract[:-6])

    # 결과 출력
    # print(f"Title: {title}")
    # print(f"Authors: {', '.join(authors)}")
    # print(f"Abstract: {abstract}\n")

# Create a DataFrame
data = {
    'Title': titles,
    'Authors': authors_list,
    'Abstract': abstracts
}

df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
df.to_csv(f'arxiv_papers_{search}.csv', index=False)