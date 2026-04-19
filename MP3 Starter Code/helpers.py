import pandas as pd
import csv
from data_structures import BusTask


def clean_df_from_schedule(file):
    '''Take in a CSV file and returns a Pandas dataframe'''
    with open(file) as csvfile:
        d = []
        areader = csv.reader(csvfile)
        max_elems = 0
        for row in areader:
            if max_elems < len(row): max_elems = len(row)
        csvfile.seek(0)
        for i, row in enumerate(areader):
            d.append(row + ["" for x in range(max_elems-len(row))])
    return pd.DataFrame(d)

def route_cleanup(df):
    '''Takes in the output from the intial csv dataframes,
    renames the columns to include route direction,
    and converts datetime to minutes after midnight.
    Output is a pandas dataframe.'''
    
    cols = df.iloc[1]
    count = 0
    for col in cols:
        if count < len(cols)/2:
            cols[count] = col+" NB"
        else:
            cols[count] = col+" SB"
        count += 1
    df = df.drop([0,1])
    df.columns = cols
    df = df.reset_index(drop=True)
    cols = df.columns
    for col in cols:
        df[col] = pd.to_datetime(df[col], format="mixed").dt.time
        df[col] = df[col].apply(time_to_minutes_after_midnight)
    return df

def direction_col(df, direction='NB'):
    '''Takes in full dataframe of bidirectional route info and returns one
    column for a specific direction (specified in the "direction" arg)'''
    
    dir_cols = [col for col in df.columns if direction in col]
    df = df[dir_cols]
    return df.dropna()   


def time_to_minutes_after_midnight(time):
    '''Takes in datetime.time object and returns minutes after midnight.
    If time is after midnight on the following day, adds 24 hours (in minutes) to time.'''
    hours = time.hour * 60
    if time.hour < 5:
        hours += 24*60
    minutes = time.minute
    return hours + minutes

# deadhead = clean_df_from_schedule("MP3_deadheading.csv")
def make_deadhead_calculator(deadhead_table):
    '''Takes in a pandas dataframe of the deadheading table and returns a function that can be called to look up the deadhead time.'''
    def deadhead(origin, destination):
        '''Takes in a string of an origin and destination and returns the deadhead time in minutes.
        Example: dead_head_time("Emeryville Depot", "Berkeley BART") -> 10'''
        
        if (('NB' in origin) or ('SB' in origin)):
            origin = origin[:-3]
            
        if (('NB' in destination) or ('SB' in destination)):
            destination = destination[:-3]
            
        for idx, o_label in enumerate(deadhead_table[0]):
            if origin in o_label:
                o_num = idx
        for j, dest_label in enumerate(deadhead_table.loc[0,:]):
            if destination in dest_label:
                d_num = j
        return int(deadhead_table[d_num][o_num])
    return deadhead

def bus_task_maker(row, column_names):
    '''Takes in a row from a route direction column and returns a BusTask object'''
    berkeley = [idx for idx, s in enumerate(column_names) if 'Berkeley BART' in s]
    if len(column_names) == 3 and berkeley:
        return BusTask(column_names[0], row[0], column_names[2], row[2], row[berkeley[0]])
    elif len(column_names) == 2 and berkeley:
        return BusTask(column_names[0], row[0], column_names[1], row[1], row[berkeley[0]])
    elif len(column_names) == 3:
        return BusTask(column_names[0], row[0], column_names[2], row[2])
    else:
        return BusTask(column_names[0], row[0], column_names[1], row[1])
    
def bus_task_route(df):
    '''Takes in a route direction dataframe and returns a list of BusTask objects'''
    column_names = list(df.columns)
    if len(column_names) == 3:
        return [bus_task_maker(row, column_names) for row in zip(df[column_names[0]], df[column_names[1]], df[column_names[2]])]
    else:
        return [bus_task_maker(row, column_names) for row in zip(df[column_names[0]], df[column_names[1]])]    
    
def sorted_bus_tasks(*args):
    '''Takes in an arbitrary number of lists of BusTasks, combines them into one list, and sorts them by origin time'''
    unsorted = list()
    for arg in args:
        unsorted += bus_task_route(arg)
    return sorted(unsorted, key=lambda x: x.start_time, reverse=False)

def create_bus_task_lists(route_7, route_18, route_52):
    '''Function that takes in a bidirectional route dataframe, 
    splits it into each individual direction, creates BusTasks for each task,
    merges and sorts BusTasks for each route.
    
    Returns 3 lists: one list of BusTasks for each individual bus route
    '''
    route_7 = route_cleanup(route_7)
    route_7_nb = direction_col(route_7, 'NB')
    route_7_sb = direction_col(route_7, 'SB')
    route_7_tasks = sorted_bus_tasks(route_7_nb, route_7_sb)



    route_18 = route_cleanup(route_18)
    route_18_nb = direction_col(route_18, 'NB')
    route_18_sb = direction_col(route_18, 'SB')
    route_18_tasks = sorted_bus_tasks(route_18_nb, route_18_sb)

    route_52 = route_cleanup(route_52)
    route_52_nb = direction_col(route_52, 'NB')
    route_52_sb = direction_col(route_52, 'SB')
    route_52_tasks = sorted_bus_tasks(route_52_nb, route_52_sb)


    return route_7_tasks, route_18_tasks, route_52_tasks 


