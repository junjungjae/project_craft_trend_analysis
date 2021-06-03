#  입력 엑셀파일의 컬럼명 가정: title, review, category

import pandas as pd
from df_xlsx_processing import export_xlsx
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('./dataset/origin_Csite_crawlingdata.csv', encoding='cp949')

res_df = export_xlsx.export_class101(df)
print(res_df)

