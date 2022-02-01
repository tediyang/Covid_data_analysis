import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

# read the data using pandas 
covid_data = pd.read_csv('covid_data.csv')

# check if any column contains a null value.
covid_data.isnull().any()

# drop nan values 
covid_data.dropna(inplace= True)

# since the data for world is included we have to drop it so it doesn't affect some analysis. 
# First, set the index to location
new_covid_data = covid_data.set_index('location')
# Second, drop world from the data.
new_covid_data = new_covid_data.drop('World', axis=0)

# reset the index
new_covid_data.reset_index(inplace=True)

# Get the total deaths and total cases that occurred every month.
new_covid_data['date'] = pd.to_datetime(new_covid_data['date'])
new_covid_data = new_covid_data.set_index('date')
group = new_covid_data.groupby(pd.Grouper(freq='M'))
total_death_and_cases_by_months_per_1000 = group[['new_deaths', 'new_cases']].sum()//1000
tot_per_mon = total_death_and_cases_by_months_per_1000

# set index 
tot_per_mon.index = ['Dec,19','Jan,20','Feb,20','Mar,20','Apr,20','May,20','Jun,20']

# total death and covid cases by months per 1000 on Multiserial bar chart 
def plot_bar():
    index = np.arange(7)
    bw = 0.3
    width = 0.6
    plt.axis([0,7,0,3000])
    plt.title('A Bar Chart showing months with total deaths and covid cases recored per 1000 Worldwide' \
        ,fontsize=7, fontweight= 'bold')
    plt.bar(index,tot_per_mon['new_deaths'],width, bw,color='r')
    plt.bar(index+bw,tot_per_mon['new_cases'], 0.48, bw,color='b')
    plt.xticks(index+0.19*bw, tot_per_mon.index)
    plt.ylabel('persons per thousand')
    plt.xlabel('date (Month, Year)')
    plt.legend(['Total deaths', 'Total cases'])
    plt.show()

plot_bar()

# total survivors by months per 1000
total_death_and_cases_by_months = group[['new_deaths', 'new_cases']].sum()
total_death_and_cases_by_months['survivors'] = (total_death_and_cases_by_months['new_cases'] \
    - total_death_and_cases_by_months['new_deaths'])//1000

# total surivors by months per 1000 on bar chat.
def survivor_bar_chart():
    index = np.arange(7)
    plt.title('A Bar Chart showing months with the total survivors recored per 1000 Worldwide' \
        ,fontsize=7, fontweight= 'bold')
    plt.bar(index,total_death_and_cases_by_months['survivors'], alpha=0.3)
    plt.bar(index,tot_per_mon['new_cases'], color="g", width= 0.5, alpha = 0.4)
    plt.ylabel('persons per thousand')
    plt.xlabel('date (Month, Year)')
    plt.xticks(index, tot_per_mon.index)
    plt.legend(['survivors', 'Total cases'], loc=2)
    plt.show()

survivor_bar_chart()

# countries with high and low number of deaths recorded.
country_deaths = new_covid_data[['new_deaths', 'new_cases']]\
    .groupby(new_covid_data['location']).sum().sort_values(by=['new_deaths'], ascending=False)
country_cases = new_covid_data[['new_deaths', 'new_cases']]\
    .groupby(new_covid_data['location']).sum().sort_values(by=['new_cases'], ascending=False)
country_deaths.head(10)
country_cases.tail(10)

# grouping the countries into continents. 
country = new_covid_data[['new_deaths', 'new_cases']].groupby(new_covid_data['location']).sum()

def continent_grouping(file):
    continent = []
    try:
        with open(file, mode='r') as afr:
            for loca in afr.readlines():
                for location in country.index:
                    loca = loca.strip('\n')
                    if location == loca:
                        continent.append(location)
    except IOError:
        print("'africa.txt' does not exist")
    
    return continent

files = ['africa.txt', 'asia.txt', 'australia and oceania.txt',\
     'europe.txt', 'north america.txt', 'south america.txt']
continents = []

# list consisting of all the lists of continents 
for file in files:
    continents.append(continent_grouping(file))
continents

# Add continent column to the dataframe
country.loc[continents[0], 'continent'] = 'Africa'
country.loc[continents[1], 'continent'] = 'Asia'
country.loc[continents[2], 'continent'] = 'Australia and Oceania'
country.loc[continents[3], 'continent'] = 'Europe'
country.loc[continents[4], 'continent'] = 'North america'
country.loc[continents[5], 'continent'] = 'South america'

# Pie chart showing number of deaths by continent 
continent_group = country[['new_deaths', 'new_cases']].groupby(country['continent']).sum()
def pie_chart():
    colors = ['yellow','green','red','blue', 'orange', 'purple']
    explode = [0.3,0,0.3,0,0,0]
    plt.title('A Pie Chart showing the total deaths by continents at the end of June 2020 \n \
        Total Deaths = 297035')
    plt.pie(continent_group['new_deaths'],labels= continent_group.index,colors=colors,explode=explode,\
shadow=True,autopct='%1.1f%%',startangle=180)
    plt.axis('equal')
    plt.show()

pie_chart()

# Pie chart showing number of cases by continent 
continent_group = country[['new_deaths', 'new_cases']].groupby(country['continent']).sum()
def pie_chart_():
    colors = ['yellow','green','red','blue', 'orange', 'purple']
    explode = [0.3,0,0.3,0,0,0]
    plt.title('A Pie Chart showing the total cases by continents at the end of June 2020 \n \
        Total Cases = 5122304')
    plt.pie(continent_group['new_cases'],labels= continent_group.index,colors=colors,explode=explode,\
shadow=True,autopct='%1.1f%%',startangle=180)
    plt.axis('equal')
    plt.show()

pie_chart_()

total_deaths_recorded_by_june_2020 = continent_group['new_deaths'].sum()
total_cases_recorded_by_june_2020 = continent_group['new_cases'].sum()
total_deaths_recorded_by_june_2020
total_cases_recorded_by_june_2020

