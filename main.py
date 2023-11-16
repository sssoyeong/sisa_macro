"""
20231109 ~ 20231116
현황 체크

나
300 -> 362
그사람
250 -> 289
"""

import pandas as pd

list09 = pd.read_csv('history/course_list_231109.csv', index_col=0)
list16 = pd.read_csv('course_list_231116.csv', index_col=0)

list09_fin = pd.DataFrame([list09.loc[idx] for idx in list09.index if list09['수료여부'][idx]=='TRUE'])
list16_fin = pd.DataFrame([list16.loc[idx] for idx in list16.index if list16['수료여부'][idx]=='TRUE'])
print(list09_fin.shape, list16_fin.shape)


list09_fin_real = pd.DataFrame([list09_fin.loc[idx] for idx in list09_fin.index if list09_fin['소분류'][idx]!='생활교양자격증'])
list16_fin_real = pd.DataFrame([list16_fin.loc[idx] for idx in list16_fin.index if list16_fin['소분류'][idx]!='생활교양자격증'])

print(list09_fin_real.shape, list16_fin_real.shape)

print(list16_fin.shape[0]-list09_fin.shape[0])
print(list16_fin_real.shape[0]-list09_fin_real.shape[0])


