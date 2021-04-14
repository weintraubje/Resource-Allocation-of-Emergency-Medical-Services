import pandas as pd
import numpy as np

def ems_data():
    '''
    Standardizes data import and clean
    '''
    
    df = pd.read_csv('EMS_Incident_Dispatch_Data.csv')
        
    # Remove a random zip code from Brooklyn that shows up in the data
    df = df.loc[df['ZIPCODE'] != 11229]
    
    # Drop columns where there is a negative value for time calculations        
    df = df.loc[(df['DISPATCH_RESPONSE_SECONDS_QY'] >= 0) & \
            (df['INCIDENT_RESPONSE_SECONDS_QY'] >= 0) & \
            (df['INCIDENT_TRAVEL_TM_SECONDS_QY'] >= 0)]
    
    return df



def limit_dates(df, start_date, end_date):
    ''' 
    Set INCIDENT_DATETIME to a datetime format and slice to include only relevant dates.
    Creates a new 'INCIDENT_DATE' column to allow for grouping
    '''
    
    # Format to DT
    df['INCIDENT_CLOSE_DATETIME'] = pd.to_datetime(df['INCIDENT_CLOSE_DATETIME'], format='%m/%d/%Y %I:%M:%S %p')
    
    # Create and apply mask
    mask = (df['INCIDENT_CLOSE_DATETIME'] > start_date) & (df['INCIDENT_CLOSE_DATETIME'] <= end_date)
    df = df.loc[mask]
    
    # New column for date only
    df['INCIDENT_DATE'] = df['INCIDENT_CLOSE_DATETIME'].dt.date
    
    return df