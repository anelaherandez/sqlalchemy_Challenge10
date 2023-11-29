# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
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
Station=Base.classes.station

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

@app.route("/precipitation")
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


@app.route("/stations")
def station():
    # create session
    session=Session(engine)
    """Return a list of all stations"""
    # query all stations
    station_result=session.query(Station.station, Station.name).all()

    session.close()
    All=[]
    for station, name in station_result:
        Dict_stat={}
        Dict_stat['station']=station
        Dict_stat['name']=name
        All.append(Dict_stat)
    
    return jsonify(All)

@app.route("/tobs")
def tobs():
    # create session
    session=Session(engine)

    # Calculate the date one year from the last date in data set.
    yearago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #get most active station
    Mostactive_station=session.query(measurement.station).\
                       group_by(measurement.station).\
                       order_by(func.count(measurement.station).desc()).all()
    
    # Perform a query to retrieve the data and tobs scores
    results=session.query(measurement.date, measurement.tobs).\
            order_by(measurement.date.asc()).\
            filter(measurement.date>= yearago_date).\
            filter(measurement.station.in_(Mostactive_station)).all()
    session.close()

    Most_Active=[]
    for date, tobs in results:
        temp_dict={}
        temp_dict['date']=date
        temp_dict['tobs']=tobs
        Most_Active.append(temp_dict)
    return jsonify(Most_Active)

@app.route("/start")
def start():
    # create session
    session=Session(engine)

    # Calculate the date one year from the last date in data set.
    yearago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_yrago=session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
                        filter(measurement.date >=yearago_date).all()
    session.close()

    tobs_obs={}
    tobs_obs["Min Temp"]=temp_yrago[0][0]
    tobs_obs["Avg Temp"]=temp_yrago[0][1]
    tobs_obs["Max Temp"]=temp_yrago[0][2]
    return jsonify(tobs_obs)

@app.route("/start/end")
def start_end():
     # create session
    session=Session(engine)

    # calculate start and end date
    yearago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    End=session.query(measurement.date).order_by(measurement.date.desc()).first()
    Eresults=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                        filter(measurement.date >=yearago_date). filter(measurement.date <=End).all()
    
    session.close()

    endT_obs={}
    endT_obs["Min Temp"]=Eresults[0][0]
    endT_obs["Avg Temp"]=Eresults[0][1]
    endT_obs["Max Temp"]=Eresults[0][2]
    return jsonify(endT_obs)


if __name__ == "__main__":
    app.run(debug=True)



