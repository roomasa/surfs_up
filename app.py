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