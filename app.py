
from flask import Flask,request,jsonify,make_response

import util


app = Flask(__name__)


@app.route('/get_airline_names')
def get_airline_names():
    
    response= jsonify({
        'airlines':util.get_airline_names()
    })
    
    #response.headers.add('Access-Control-Allow-Origin','*')

    return response

@app.route('/get_source_names')
def get_source_names():
    
    response= jsonify({
        'sources':util.get_source_names()
    })
    
    #response.headers.add('Access-Control-Allow-Origin','*')
    
    return response

@app.route('/get_data')
def get_data():
    util.load_saved_artifacts()

    response = jsonify({
        'data': util.get_data()
    })
    print(util.get_data())
    #response.headers.add('Access-Control-Allow-Origin','*')
    return build_actual_response(response)

@app.route('/get_stop_details')
def get_stop_details():
    
    response = jsonify({
        'stops':util.get_stop_details()
    })
    
    #response.headers.add('Access-Control-Allow-Origin','*')
    
    return response


@app.route('/get_destination_names')
def get_destination_names():
    
    response= jsonify({
        'destinations':util.get_destination_names()
    })
    
    #response.headers.add('Access-Control-Allow-Origin','*')
    return response


@app.route('/predict',methods=['OPTIONS','POST'])
def predict_flight_price():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    elif request.method == 'POST':
        print(request.get_json())
        airline= request.get_json().get('airline')
        source= request.get_json().get('source')
        destination= request.get_json().get('destination')
        departure= request.get_json().get("dep_Time")
        arrival= request.get_json().get("arrival_Time")
        stops= request.get_json().get("stops")

        print(stops)
        response= jsonify({
            'price':util.get_estimated_price(airline,source,destination,departure,arrival,stops)
        })
        
        
        # response = make_response()
        #response.headers.add('Access-Control-Allow-Origin','*')
        return build_actual_response(response)
        

def build_preflight_response():
    print("I am in preflight")
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def build_actual_response(response):
    print("I am in Actual req")
    response.headers.add("Content-Type","application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__=="__main__":
    print("Starting Python Flask Server For PreVel Application...")
    app.run()
