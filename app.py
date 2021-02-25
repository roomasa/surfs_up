from flask import Flask
import datetime as dt
import numpy as np
import pandas as pd
#dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#import dependencies for Flask
from flask import Flask, jsonify
#create the database engine
engine = create_engine("sqlite:///hawaii.sqlite")
#reflect the database into our classes.
Base = automap_base()
#Add the following code to reflect the database
Base.prepare(engine, reflect=True)
#save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#create a session link from Python to our database with the following code
session = Session(engine)
#define our Flask app, add the following line of code. This will create a Flask application called "app."
app = Flask(__name__)
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#route for precipitation analysis    
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
#route for station analysis, We want to start by unraveling our results into a one-dimensional array. To do this, we want to use thefunction np.ravel(), with results as our parameter.
#Next, we will convert our unraveled results into a list. To convert the results to a list, 
# we will need to use the list function, which is list(), and then convert that array into a list. 
# Then we'll jsonify the list and return it as JSON. Let's add that functionality to our code:
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
#for this route, the goal is to return the temperature observations for the previous year. 
#As with the previous routes, begin by defining the route with this code
#unravel the results into a one-dimensional array and convert that array into a list. 
# Then jsonify the list and return our results, like this
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps=list(np.ravel(results))
    return (jsonify(temps=temps))
#note to transfer this output ot the flask web app, go to command line, navigate to your folder that 
#has this file and press control+c if the prev rout has not been quit yet and then type flask run
#next route is for the statistical analysis
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#create a function called stats to put our code in
#We need to add parameters to our stats()function: a start parameter and an end parameter
#With the function declared, we can now create a query to select the minimum, average, and 
# maximum temperatures from our SQLite database. We'll start by just creating a list called sel, with the following code
#Since we need to determine the starting and ending date, add an if-not statement to our code. 
# This will help us accomplish a few things. We'll need to query our database using the list that we just made. 
# Then, we'll unravel the results into a one-dimensional array and convert them to a list. Finally, we will jsonify our results 
# and return them.
# asterik next to sel denotes that we will have multiple results for our query: min, avg and max 
##Now we need to calculate the temperature minimum, average, and maximum with the start and end dates. 
#We'll use the sel list, which is simply the data points we need to collect. Let's create our next query, which will get our statistics data.
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
   