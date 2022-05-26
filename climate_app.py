#climate_app
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.measurement
Base.classes.station
# #################################################

# # Flask Setup
# #################################################
# app = Flask(__name__)

# #################################################
# # Flask Routes
# #################################################
@app.route("/")
def welcome():
    "Homepage"
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Dates and temperature observations of the most active station: /api/v1.0/tobs<br/>"
        f"Temperature statistics from the start date(yyyy-mm-dd): /api/v1.0/<start><br/>"
        f"Temperature statistics from start to end dates(yyyy-mm-dd): `/api/v1.0/<start>/<end>`"
    )
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all Precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        all()

    session.close()

    # Convert the list to Dictionary
    prcp_list = []
    for date,prcp_list  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp_dict
               
        prcp_list.append(prcp_dict)

    # Return the JSON representation of your dictionary (precipitation).
    return jsonify(prcp_list)
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all Stations
    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    #Return a JSON list of stations from the dataset.
    return jsonify(all_stations)
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all tobs"""
    # Query all tobs

    #Query the dates and temperature observations of the most active station (USC00519281) for the previous year of data.
    results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()
    # Convert the list to Dictionary
    tobs_list = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        tobs_list.append(tobs_dict)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(tobs_list)
#################################################

@app.route("/api/v1.0/<start>")
def Start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start"""
    # Query all tobs

    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates >= to the start date."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()
 # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

#################################################

@app.route("/api/v1.0/<start><end>")
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start-end range"""
    # Query all tobs

    """When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive)."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_range_tobs = []
    for min, avg, max in results:
        start_end_range_tobs_dict = {}
        start_end_range_tobs_dict["min_temp"] = min
        start_end_range_tobs_dict["avg_temp"] = avg
        start_end_range_tobs_dict["max_temp"] = max
        start_end_range_tobs.append(start_end_range_tobs_dict) 
    
    return jsonify(start_end_range_tobs)

if __name__ == "__main__":
    app.run(debug=True)