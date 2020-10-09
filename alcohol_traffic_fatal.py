# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:17:01 2020

@author: rop
"""

# Does alcohol drinking increase traffic death rate?


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def print_wide_df(df):
    ''' show wide dataframe'''
    with pd.option_context('display.max_columns', None, 
                           'display.expand_frame_repr', False, 
                           'max_colwidth', -1):
        print(df)


url_alcohol = 'https://en.wikipedia.org/wiki/List_of_countries_by_alcohol_consumption_per_capita'
tables = pd.read_html(url_alcohol)
print(len(tables))
alco = tables[2]

print_wide_df(alco.head())
print(alco.shape)


# road fatalities
url_traffic = 'https://en.wikipedia.org/wiki/List_of_countries_by_traffic-related_death_rate'
tables = pd.read_html(url_traffic)
print(len(tables))
fatal = tables[1]

fatal.columns = ['Country', 'Continent', 
              'fatal_per_100k_inhabitants_per_yr', 
              'fatal_per_100k_vehicles', 
              'fatal_per_1bil_veh_km', 
              'fatal_latest', 
              'year_data']

fatal = fatal.drop(columns=['fatal_per_1bil_veh_km'])
fatal = fatal.dropna(subset=['Continent', 'fatal_per_100k_vehicles'], 
                     how='any')
cols_num = fatal.drop(columns=['Country', 'Continent']).columns

for col in cols_num:
    print(col)
    fatal[col] = [s[0] for s in fatal[col].str.split(r'[')]
    fatal[col] = pd.to_numeric(fatal[col], errors='coerce')
    
fatal['year_data'] = fatal['year_data'].astype(int)

print_wide_df(fatal.head())


# merging data
df_fatal = pd.merge(alco, fatal, how='inner', on='Country')

print_wide_df(df_fatal.head())
print(df_fatal.shape)


# plot
sns.set(palette='colorblind', style='white')

top_drink = df_fatal.nlargest(8, 'Total')
f, ax = plt.subplots()
sns.barplot(data=top_drink, y='Country', x='Total', ax=ax)
f.suptitle('Highest alcohol consumption per capita')


top_fatal = df_fatal.nlargest(8, 'fatal_per_100k_inhabitants_per_yr')
top_fatal_veh = df_fatal.nlargest(8, 'fatal_per_100k_vehicles')

f, ax = plt.subplots(ncols=2, figsize=(12, 5), dpi=150)
sns.barplot(data=top_fatal, y='Country', 
            x='fatal_per_100k_inhabitants_per_yr', ax=ax[0])
sns.barplot(data=top_fatal_veh, y='Country', 
            x='fatal_per_100k_vehicles', ax=ax[1])
#ax.xaxis.set_tick_params(rotation=45)
f.tight_layout(rect=(0, 0, 1, 0.95))
f.suptitle('Highest Fatality Rates')


varnames= ['fatal_per_100k_vehicles', 'fatal_per_100k_inhabitants_per_yr']

for varname in varnames:
    g = sns.lmplot(data=df_fatal, x='Total', y=varname, 
                   height=6, aspect=1.4, markers='o', scatter_kws={'alpha': 0.5})
    thai = df_fatal.loc[df_fatal['Country']=='Thailand', 
                   ['Total', varname]]
#    g.ax.annotate('Thailand', xy=(thai['Total'], thai[varname]), 
#                  xytext=(thai['Total']*1.05, thai[varname]*0.9), 
#                  arrowprops=dict(facecolor='gray'))
    max_drink_idx = df_fatal['Total'].idxmax()
    max_fatal_idx = df_fatal[varname].idxmax()
    max_drink_ctry = df_fatal.loc[max_drink_idx, 'Country']
    max_fatal_ctry = df_fatal.loc[max_fatal_idx, 'Country']
    g.ax.annotate(max_drink_ctry, 
                  xy=(df_fatal.loc[max_drink_idx, 'Total'], 
                      df_fatal.loc[max_drink_idx, varname]), 
                  xytext=(df_fatal.loc[max_drink_idx, 'Total']*1.05, 
                          df_fatal.loc[max_drink_idx, varname]*0.9), 
                  arrowprops=dict(facecolor='gray'))
    g.ax.annotate(max_fatal_ctry, 
                  xy=(df_fatal.loc[max_fatal_idx, 'Total'], 
                      df_fatal.loc[max_fatal_idx, varname]), 
                  xytext=(df_fatal.loc[max_fatal_idx, 'Total']*1.05, 
                          df_fatal.loc[max_fatal_idx, varname]*0.9), 
                  arrowprops=dict(facecolor='gray'))

plt.show()