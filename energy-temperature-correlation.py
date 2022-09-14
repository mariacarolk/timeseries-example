import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def has_null(df: pd.DataFrame) -> bool:
    return df.isnull().any()

energy = pd.read_csv('energy.csv', sep=';', parse_dates=[0], infer_datetime_format=True)
temperature = pd.read_csv('temperature.csv', sep=';', parse_dates=[0], infer_datetime_format=True)

energy = energy.set_index(keys = ['referencia'])
energy_filt = energy['2019' : '2020']

temperature = temperature.set_index(keys = ['referencia'])
temperature_filt = temperature['2019' : '2020']

if has_null(df=temperature_filt['temp-media-sp']):
    temperature_filt.dropna(subset=['temp-media-sp'], inplace=True)
if has_null(df=temperature_filt['temp-media-rj']):
    temperature_filt.dropna(subset=['temp-media-rj'], inplace=True)
if has_null(df=temperature_filt['temp-media-mg']):
    temperature_filt.dropna(subset=['temp-media-mg'], inplace=True)

#calculate the average temperature in the 3 states
temperature_filt['temp-media'] = (temperature_filt['temp-media-sp'] +
                                  temperature_filt['temp-media-rj'] +
                                  temperature_filt['temp-media-mg']) / 3

temperature_filt['temp-media'] = np.round(temperature_filt['temp-media'], decimals = 1)
temp_resampled = temperature_filt.resample(rule='1m').mean()

with sns.axes_style('whitegrid'):
    graph = sns.lineplot(data=temp_resampled, x='referencia', y='temp-media', marker ='1', palette='pastel')
    graph.set(title='Average temperature', ylabel='Temperature', xlabel='Year/Month')
    graph.figure.set_size_inches(10, 4)

with sns.axes_style('whitegrid'):
    graph = sns.lineplot(data=energy_filt, x='referencia', y='residencial', marker ='1', palette='pastel')
    graph.set(title='Residential energy consumption', ylabel='Consumption', xlabel='Year/Month')
    graph.figure.set_size_inches(10, 4)

#analyses if there is a correlation between the temperature and the residencial electrical energy consumption
#in the years 2019 to 2020
consumption_array = np.array(energy_filt['residencial'].to_list())
temperature_array = np.array(temp_resampled['temp-media'].to_list())
corrcoef = np.corrcoef(consumption_array, temperature_array)
print(corrcoef)