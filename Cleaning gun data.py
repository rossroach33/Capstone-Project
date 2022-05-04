# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 11:38:00 2022

@author: Owner
"""

import pandas as pd
import datetime as dt

path = 'C:/Users/Owner/Documents/Data Mining/'
file_out = 'final_gun_data.csv'
file_out1 = 'gun_data_population_scaled.csv'

background=pd.read_csv(r"C:\Users\Owner\Downloads\background.csv")
gun=pd.read_csv(r"C:\Users\Owner\Downloads\gun_clean.csv")

gun['total_casualty'] = gun['n_killed'] + gun['n_injured']

gun['date'] = pd.to_datetime(gun['date'])
background['month'] = pd.to_datetime(background['month'])

gun['year'] = pd.to_datetime(gun['date']).dt.year
gun['month'] = pd.to_datetime(gun['date']).dt.month
gun['Date'] = gun['month'].astype(str) + '-' + gun['year'].astype(str)
gun = gun.drop(labels = ['date', 'year', 'month'], axis = 1)

total_gun = gun.groupby(['state','Date'], as_index = False).sum()
total_count = gun.groupby(['state','Date'], as_index = False).size()


background['year'] = pd.to_datetime(background['month']).dt.year
background['Month'] = pd.to_datetime(background['month']).dt.month
background['Date'] = background['Month'].astype(str) + '-' + background['year'].astype(str)
background = background.drop(labels = ['month', 'Month','year'], axis = 1)
background = background[0:4263]

merged_data = background.merge(total_gun, how = 'left', left_on = ['Date', 'state'], right_on = ['Date', 'state'])
merged_data = merged_data.merge(total_count, how = 'left', left_on = ['Date', 'state'], right_on = ['Date', 'state'])

merged_data = merged_data[1176:4262]
merged_data.reset_index()
final_data = merged_data.fillna(0)
final_data = final_data.rename(columns = {'total': 'background_checks', 'size': 'number_of_incidents'})
final_data = final_data.reset_index()
final_data = final_data.drop(columns = 'index')

final_data.to_csv(path + file_out, sep = ',', index = False)

data_scaled = final_data.copy()

data_scaled['handgun'] = (data_scaled['handgun'] / data_scaled['population']) * 100000
data_scaled['long_gun'] = (data_scaled['long_gun'] / data_scaled['population']) * 100000
data_scaled['background_checks'] = (data_scaled['background_checks'] / data_scaled['population']) * 100000
data_scaled['n_killed'] = (data_scaled['n_killed'] / data_scaled['population']) * 100000
data_scaled['n_injured'] = (data_scaled['n_injured'] / data_scaled['population']) * 100000
data_scaled['total_casualty'] = (data_scaled['total_casualty'] / data_scaled['population']) * 100000
data_scaled['number_of_incidents'] = (data_scaled['number_of_incidents'] / data_scaled['population']) * 100000

data_scaled.to_csv(path + file_out1, sep = ',', index = False)



