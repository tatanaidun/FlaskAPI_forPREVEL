import pickle
import json
import numpy as np
import pandas as pd

__data_columns = None
__model = None
__airlines=None
__sources=None
__stop_details=None
__destinations=None
data=None

def get_source_names():
    return __sources

def get_destination_names():
    return __destinations

def get_stop_details():
    return __stop_details

def get_airline_names():
    return __airlines

def get_data():
    print(data)
    return data

def get_estimated_price(Airline,Source,Destination,Departure,Arrival,Stops):
    try:
        airline_index= __data_columns.index("airline_" + Airline.lower())
    except:
        airline_index=-1
    try:    
        source_index= __data_columns.index("source_" + Source.lower())
    except:
        source_index=-1
    try:
        destination_index=__data_columns.index("destination_" + Destination.lower())
    except:
        destination_index=-1

        

    x=np.zeros(len(__data_columns))

    x[0]= __stop_details.get(Stops.lower())
    x[1]= int(pd.to_datetime(Departure, format="%Y-%m-%dT%H:%M").day)
    x[2]= int(pd.to_datetime(Departure, format ="%Y-%m-%dT%H:%M").month)
    x[3]= int(pd.to_datetime(Departure, format ="%Y-%m-%dT%H:%M").hour)
    x[4]= int(pd.to_datetime(Departure, format ="%Y-%m-%dT%H:%M").minute)

    x[5]= int(pd.to_datetime(Arrival, format ="%Y-%m-%dT%H:%M").hour)
    x[6]= int(pd.to_datetime(Arrival, format ="%Y-%m-%dT%H:%M").minute)

    x[7]= abs(x[3]-x[5])
    x[8]= abs(x[4]-x[6])


    if airline_index>=0:
        x[airline_index]=1
    if source_index>=0:
        x[source_index]=1
    if destination_index>=0:
        x[destination_index]=1

    
    return round(__model.predict([x])[0],2)

def load_saved_artifacts():
    global __data_columns
    global __airlines
    global __model
    global __sources
    global __destinations
    global __stop_details
    global data

    with open("./artifacts/artifacts.json", 'r') as j:
        data= json.loads(j.read())
        __airlines = data['airlines']
        __sources= data['sources']
        __destinations= data['destinations']
        __data_columns= data['data_columns']
        __stop_details= data.get('stop_details')

    with open("./artifacts/flight_rf.pkl",'rb') as f:
        __model =  pickle.load(f)
    
    


# if __name__ == '__main__':
#     load_saved_artifacts()
#     print()
#     print()
#     print(data)