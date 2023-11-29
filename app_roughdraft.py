# Import the dependencies. 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session link from python to DB
    session=Session(engine)
    """Return a list of precipitation and date for one year"""
    # Calculate the date one year from the last date in data set.
    yearago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # print(yearago_date)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(measurement.date, measurement.prcp).order_by(measurement.date.asc()).filter(measurement.date>=yearago_date).all()
    session.close()

    # Convert list of tuples into dictionary
    precipitation=[]
    for date,prcp in results:
        precipitation_dict={}
        precipitation_dict['date']=date
        precipitation_dict['prcp']=prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def station():
    # create session
    session=Session(engine)
    """Return a list of all stations"""
    # query all stations
    station_result=session.query(station.station,station.name).all()

    session.close()

    # Convert list of tuples into normal list
    Stations=list(np.ravel(station_result))
    return jsonify(Stations)

if __name__ == "__main__":
    app.run(debug=True)