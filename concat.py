import pandas as pd

# 첫 번째 CSV 파일 읽기
csv1 = pd.read_csv('arxiv.csv')

# 두 번째 CSV 파일 읽기
csv2 = pd.read_csv('papers_with_code.csv')

# 두 DataFrame을 수직으로 이어붙이기
concatenated_df = pd.concat([csv1, csv2], ignore_index=True)

# 결과를 새로운 CSV 파일로 저장
concatenated_df.to_csv('concat.csv', index=False)

