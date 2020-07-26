import pandas as pd
import re
import os

cities_initial_dataset = 'cities.csv'
state_cities_dataset = 'state_cities/'

def clear_original_dataset():
    # remove some unnecessary columns from the initial dataset
    df = pd.read_csv(cities_initial_dataset, usecols=[0,2,4,5], delimiter=';')

    # df.columns = df.columns.str.strip()

    df.to_csv(cities_initial_dataset, index=False)

# clear_original_dataset()


def create_50states_folders():
    f = open('50_STATES_USA.txt', 'r')
    states = f.readlines()
    
    if not os.path.exists(state_cities_dataset):
        try:
            # creating dataset folder
            os.mkdir(state_cities_dataset)
        except OSError:
            print('Error creating dataset directory!')

    for state in states:
        # print(state)
        # remove the '\n' from the state name
        state = re.sub('[\n]', '', state)

        # creating sub folders and sub csv files with file_name = state
        if not os.path.exists(state_cities_dataset+state):
           os.mkdir(state_cities_dataset+state)
           with open(state_cities_dataset+state+'/'+state+'.csv', 'w'):
              pass

# create_50states_folders()


def city_assign_state():

    df = pd.read_csv(cities_initial_dataset)

    # iterating all the rows
    for _, city in df.iterrows(): 

        # print(city['State'])
        
        # https://en.wikipedia.org/wiki/Statehood_movement_in_the_District_of_Columbia
        city['State'] = re.sub('District of Columbia', 'Washington', city['State'])

        # 'a' mode (append) instead of w to avoid overwriting
        with open(state_cities_dataset+city['State']+'/'+city['State']+'.csv', 'a') as f:
            f.write(city['City'] + ',' + str(city['Population'])+ ',' + city['Coordinates']+'\n')
        

# city_assign_state()

