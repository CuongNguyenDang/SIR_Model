"""
Collect data from git reposistory
$python collect_data [continent]
"""


import pandas as pd
import os
import sys
import time

url = "https://github.com/CSSEGISandData/COVID-19"

GIT_INFECTIOUS_PATH = "repo/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
GIT_DEAD_PATH = "repo/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

INFECTIOUS_PATH = "data/time_series_covid19_confirmed_global.csv"
DEAD_PATH = "data/time_series_covid19_deaths_global.csv"
POPULATION_PATH = "data/populations.csv"


def collect(continent = None):
    if os.path.isdir("repo"):
        os.system("cd repo; git pull")
    else:
        os.system(f"git clone {url} repo")
        # Repo.clone_from("https://github.com/CSSEGISandData/COVID-19","repo")

    if not os.path.isdir("data"):
        os.system("mkdir data")
    os.system(f"cp {GIT_INFECTIOUS_PATH} data")
    os.system(f"cp {GIT_DEAD_PATH} data")
    time.sleep(5)
    os.system("rm -rf repo")

    infectious = pd.read_csv(INFECTIOUS_PATH)
    deads = pd.read_csv(DEAD_PATH)
    populations = pd.read_csv(POPULATION_PATH)

    # remove and rename some columns 
    infectious = infectious.drop(columns=['Lat', 'Long'])
    deads = deads.drop(columns=['Lat', 'Long'])

    l = list(deads.columns)
    l[1] = 'Country'
    infectious.columns = l
    deads.columns = l
    
    # save populations, continents in dictionary
    pops = {}
    conts = {}
    for _, row in populations.iterrows():
        country = row['Country']
        pop = row['Year_2016']
        conts[country] = row['Continent']
        pops[country] = pop
    
    # insert new column: Continent
    value = []
    for i in range(len(infectious)):
        value.append(conts[infectious.iloc[i]['Country']])
    infectious.insert(2,"Continent",value)
    deads.insert(2,"Continent",value)

    # select this continent
    if continent:
        infectious = infectious[infectious.Continent == continent]
        deads = deads[deads.Continent == continent]

    # print(infectious,'\n', deads)
    return (infectious, deads, pops)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        collect()
    else:
        continent = sys.argv[1]
        collect(continent)
    