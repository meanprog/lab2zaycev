import pandas as pd

df = pd.DataFrame(columns=['Пол','Возраст', 'Вид забега','ФИО'])
row = 0

def print_to_database(df):
    df.to_excel('marathon.xlsx')


