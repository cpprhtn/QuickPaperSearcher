import pandas as pd

# 두 개의 CSV 파일 경로 설정
csv1_path = 'arxiv.csv'
csv2_path = 'papers_with_code.csv'

# CSV 파일들을 데이터프레임으로 읽어오기
df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

# 'Title'을 기준으로 데이터 병합
merged_df = pd.merge(df1, df2, on='Title', how='inner')

# 결과 출력
print(merged_df)