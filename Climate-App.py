import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<a href='/api/v1.0/2017-01-01'>/api/v1.0/2017-01-01</a><br></p>"
        f"<a href='/api/v1.0/2017-01-01/2017-01-07'>/api/v1.0/2017-01-01/2017-01-07</a></p>"
    
    )

@app.route("/api/v1.0/precipitation")
def PRCP():
    """Return a list of all station and its precipitation"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).\
        group_by(Measurement.date).order_by(func.sum(Measurement.prcp).desc()).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    PRCP = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        PRCP.append(prcp_dict)

    return jsonify(PRCP)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of Stations"""
    # Query all Stations
    stations = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)   

@app.route("/api/v1.0/tobs")
def TOBS():
    """Return a list of dates and TOBS"""
    # Query all passengers

    TOBS = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= '2010-08-23').all()

    # Convert list of tuples into normal list
    all_TOBS = list(np.ravel(TOBS))

    return jsonify(all_TOBS)

@app.route("/api/v1.0/<start>")
def DTOBS(start):
    """Return a list of dates and TOBS"""
    # Query all passengers
    
    DTBOS = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all() 

    # Convert list of tuples into normal list
    all_DTOBS = list(np.ravel(DTBOS))

    return jsonify(all_DTOBS)

@app.route("/api/v1.0/<start>/<end>")
def SETOBS(start, end):
    """Return a list of dates and TOBS"""
    # Query all passengers

    SETBOS = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all() 

    # Convert list of tuples into normal list
    all_SETOBS = list(np.ravel(SETBOS))

    return jsonify(all_SETOBS)

if __name__ == '__main__':
    app.run(debug=True)