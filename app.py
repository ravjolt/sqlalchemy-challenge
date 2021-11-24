#import dependencies
import os
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from dateutil.relativedelta import relativedelta

#import flask
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#set up app and flask
climateApp = Flask(__name__)

#create database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database and tables
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# create reference to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session and like python to database
session = Session(engine)



#flask routes
@climateApp.route("/")
def Welcome():
    return (
        f"Available Routes:<br/>"

        f"/api/v1.0/precipitation"

        f"/api/v1.0/stations"

        f"/api/v1.0/tobs"

        f"/api/v1.0/<start>"
        
        f"/api/v1.0/<start>/<end>"
    )

@climateApp.route("/api/v1.0/precipitation")
def precipitation():

    prcp_data = session.query(Measurement.date, Measurement.prcp).all()

    # convert list of tuples into normal list
    prcp_list = list(np.ravel(prcp_data))

    # Create a dictionary from the row data and append to a list 
    dates = prcp_list[0::2]
    prcp = prcp_list[1::2]   
    prcp_dict = dict(zip(dates, prcp))

    return jsonify(prcp_dict)

@climateApp.route("/api/v1.0/stations")
def stations():
   
    # query all precipitation
    station_data = session.query(Station.name).all()

    # convert list of tuples into normal list
    station_list = list(np.ravel(station_data))

    return jsonify(station_list)

@climateApp.route("/api/v1.0/tobs")
def tobs():
   
    # query all tobs 
    tobs_data = session.query(Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    # convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_data))

    return jsonify(tobs_list)


@climateApp.route("/api/v1.0/<start>")
def tobs_start(start):


    # query the database to get the maximum date
    max_date_query = session.query(func.max(Measurement.date)).scalar()

    # convert max_date to proper date format
    max_date = dt.datetime.strptime(max_date_query, '%Y-%m-%d').date()

    # query all tobs greater than and equal to start date
    min_ave_max_tobs =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= max_date).all()

    # convert list of tuples into normal list
    min_ave_max_tobs_list = list(np.ravel(min_ave_max_tobs))
    
    tmin = min_ave_max_tobs_list[0]
    tave = min_ave_max_tobs_list[1]
    tmax = min_ave_max_tobs_list[2]

    return jsonify(tmin, tave, tmax)

@climateApp.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start, end):
 

    # query all tobs between start date and end date inclusive
    min_ave_max_tobs_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # convert list of tuples into normal list
    min_ave_max_tobs_end_list = list(np.ravel(min_ave_max_tobs_end))

    tmin = min_ave_max_tobs_end_list[0]
    tave = min_ave_max_tobs_end_list[1]
    tmax = min_ave_max_tobs_end_list[2]

    return jsonify(tmin, tave, tmax)

if __name__ == '__main__':
    climateApp.run(debug=True)

