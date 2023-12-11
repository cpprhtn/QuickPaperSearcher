import os
import pandas as pd

# 폴더 경로 설정
folder_path = './pw_paper'

# 모든 CSV 파일 읽어오기
all_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 모든 CSV 파일을 하나의 데이터프레임으로 합치기
df_list = []
for file in all_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

merged_df = pd.concat(df_list, ignore_index=True)
merged_df['recommand'] = 1
# 새로운 CSV 파일로 저장
merged_df.to_csv('papers_with_code.csv', index=False)
