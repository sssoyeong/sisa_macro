import pandas as pd

course_list = pd.read_excel('시사점 과정리스트(231011)_차시.xlsx', header=3)
course_list = course_list.drop(columns='Unnamed: 0')
course_list.columns = ['대분류', '중분류', '소분류', '과정명', '학습시간']
course_list.head(5)

