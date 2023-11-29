"""
20231109 ~ 20231116
현황 체크

나
300 -> 375
그사람
250 -> 289
"""

import pandas as pd

list09 = pd.read_csv('history/course_list_231109.csv', index_col=0)
list16 = pd.read_csv('course_list_231116.csv', index_col=0)

list09_fin = pd.DataFrame([list09.loc[idx] for idx in list09.index if (list09['수료여부'][idx]=='TRUE')|(list09['수료여부'][idx]=='True')])
list16_fin = pd.DataFrame([list16.loc[idx] for idx in list16.index if (list16['수료여부'][idx]=='TRUE')|(list16['수료여부'][idx]=='True')])
print(list09_fin.shape, list16_fin.shape)


list09_fin_real = pd.DataFrame([list09_fin.loc[idx] for idx in list09_fin.index if list09_fin['소분류'][idx]!='생활교양자격증'])
list16_fin_real = pd.DataFrame([list16_fin.loc[idx] for idx in list16_fin.index if list16_fin['소분류'][idx]!='생활교양자격증'])

print(list09_fin_real.shape, list16_fin_real.shape)
print(list16_fin.shape[0]-list09_fin.shape[0])
print(list16_fin_real.shape[0]-list09_fin_real.shape[0])


"""
나: 생활교양자격증 넘긴 거 빼면 63개 수료, 보수적으로 60개 수료했다고 가정.
그: 39개 수료
"""
hers = list09_fin.loc[311:394]  # 40개
mine = list16_fin.tail(60)      # 60개

hour_hers = sum(hers['학습시간'])
hour_mine = sum(mine['학습시간'])
print('7일간 수료한 강의들 학습시간 합계', hour_hers, hour_mine)                #  499  / 1003
print('7일간 실질적으로 학습한 시간 합계', hour_hers*0.3, hour_mine*0.3)        # 149.7 / 300.9
print('7일간 실질적으로 쏟은 시간 하루당', hour_hers*0.3/7, hour_mine*0.3/7)    # 21.39 / 42.99


# 다시 계산해볼까?
course_list = list09.copy()
# course_list.loc[289:330]
sum(course_list.loc[289:330]['학습시간'])           # 339 hours
sum(course_list.loc[289:330]['학습시간'])*0.3/7     # 14.53 hours
# 그 사람이 14.53시간 쏟아부었다고? 아니, 하루 평균 7.26시간 부었다고 하는 게 훨씬 적절함. 적어도 두 개로 돌리고 있다는 말이 됨



##############################
'''총 수료해도 되는 시간 계산'''
# 2023.10.18 ~ 2023.11.30 (44일)
# 44 * 24 = 1056 hours
# 1056 / 0.3 = 3520 hours 수료 가능
# 463번 포함, 463번까지 가능


##############################
# 2023.11.16 16시 ~ 2023.11.21 09시
# 289개 ~ 318개
sum(course_list.loc[330:359]['학습시간'])         # 335 hours
sum(course_list.loc[330:359]['학습시간'])*0.3/4   # 25.125 hours (보수적으로 4일 동안 했다고 잡음)


#####
# 2023.11.21 09시 ~ 2023.11.29 09시 (8일)
# 318개 ~ 402개
sum(course_list.loc[359:444]['학습시간'])         # 1465 hours
sum(course_list.loc[359:444]['학습시간'])*0.3/8   # 54.9375 hours 