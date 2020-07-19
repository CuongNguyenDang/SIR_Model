"""
Collect data from git reposistory
$python collect_data

continents:
    Africa, Asia, Australia, Europe, None, North America, South America

get DataFrame:
    from collect_data import read_data
    infect_df, dead_df, recov_df, _ = read_data([continent])
"""


import pandas as pd
import os
import sys
import time

url = "https://github.com/CSSEGISandData/COVID-19"

GIT_INFECTIOUS_PATH = "repo/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
GIT_DEAD_PATH = "repo/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
GIT_RECOVERED_PATH = "repo/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

INFECTIOUS_PATH = "data/time_series_covid19_confirmed_global.csv"
DEAD_PATH = "data/time_series_covid19_deaths_global.csv"
RECOVERED_PATH = "data/time_series_covid19_recovered_global.csv"
POPULATION_PATH = "data/populations.csv"


def collect():
    if os.path.isdir("repo"):
        os.system("cd repo; git pull")
    else:
        os.system(f"git clone {url} repo")
        # Repo.clone_from("https://github.com/CSSEGISandData/COVID-19","repo")

    if not os.path.isdir("data"):
        os.system("mkdir data")
    os.system(f"cp {GIT_INFECTIOUS_PATH} data")
    os.system(f"cp {GIT_DEAD_PATH} data")
    os.system(f"cp {GIT_RECOVERED_PATH} data")
    time.sleep(5)
    os.system("rm -rf repo")

def read_data(continent = None):
    infectious = pd.read_csv(INFECTIOUS_PATH)
    deads = pd.read_csv(DEAD_PATH)
    recovered = pd.read_csv(RECOVERED_PATH)
    populations = pd.read_csv(POPULATION_PATH)

    # remove and rename some columns 
    infectious = infectious.drop(columns=['Lat', 'Long'])
    deads = deads.drop(columns=['Lat', 'Long'])
    recovered = recovered.drop(columns=['Lat', 'Long'])

    l = list(deads.columns)
    l[0],l[1] = 'Province', 'Country'
    infectious.columns = l
    deads.columns = l
    recovered.columns = l
    
    infectious = infectious.sort_values(by = list(infectious.columns)[1:])
    deads = deads.sort_values(by = list(deads.columns)[1:])
    recovered = recovered.sort_values(by = list(recovered.columns)[1:])

    # remove some rows which different in 3 file
    infectious = infectious[infectious.Country.isin(recovered.Country) & infectious.Province.isin(recovered.Province)].reset_index(drop = True)
    deads = deads[deads.Country.isin(recovered.Country) & deads.Province.isin(recovered.Province)].reset_index(drop = True)
    recovered = recovered[recovered.Country.isin(infectious.Country) & recovered.Province.isin(infectious.Province)].reset_index(drop = True)

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
    recovered.insert(2,"Continent",value)

    # select this continent
    if continent:
        infectious = infectious[infectious.Continent == continent]
        deads = deads[deads.Continent == continent]
        recovered = recovered[recovered.Continent == continent]
    return infectious, deads, recovered, pops


if __name__ == '__main__':
    collect()

