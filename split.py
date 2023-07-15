import pandas as pd

data = pd.read_csv('tickers.csv')

data_category_range = data['Country'].unique()
data_category_range = data_category_range.tolist()

countries = []

for i,value in enumerate(data_category_range):
    data[data['Country'] == value].to_csv(str(value)+r'.csv',index = False, na_rep = 'N/A')
    countries.append(value)

print(countries)
