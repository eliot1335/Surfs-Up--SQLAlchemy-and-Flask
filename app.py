import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Setup Flask
app = Flask(__name__)

# ---------------------------------------------------------------------

# Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# ---------------------------------------------------------------------
# Precipitation API page
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and precipitation values
    last_date = session.query(func.max(Measurement.date)).first()[0]

    x = last_date.split("-")
    for i in range(0, len(x)):
        x[i] = int(x[i])

    year_ago_date = (dt.date(x[0], x[1], x[2]) - dt.timedelta(days = 365))
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago_date).all()

    session.close()

    # Convert to list of dictionaries to jsonify
    prcp_data_list = []

    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_date_list.append(prcp_dict)

    return jsonify(prcp_data_list)

# ---------------------------------------------------------------------
# Stations API page
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    stations_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    stations_list = []

    for station, name, lat, lng, elevation in stations_data:
        stations_dict = {}
        stations_dict["Station"] = station
        stations_dict["Name"] = name
        stations_dict["Latitude"] = lat
        stations_dict["Longitude"] = lng
        stations_dict["Elevation"] = elevation
        stations_list.append(stations_dict)

    return jsonify(stations_list)

# ---------------------------------------------------------------------
# Most active station TOBS API page
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data
    last_date = session.query(func.max(Measurement.date)).first()[0]

    x = last_date.split("-")
    for i in range(0, len(x)):
        x[i] = int(x[i])

    year_ago_date = (dt.date(x[0], x[1], x[2]) - dt.timedelta(days = 365))

    station_tobs_counts = session.query(Measurement.station, Station.name, \
        func.count(Measurement.station)).\
            filter(Measurement.station == Station.station).\
                group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).all()

    most_active_station_id = station_tobs_counts[0][0]

    most_active_station_last_yr_data =  session.query(Measurement.date ,Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
            filter(Measurement.date >= year_ago_date).all()
    
    session.close()

    # Convert to list of dictionaries to jsonify
    tobs_list = []

    for date, tobs in most_active_station_last_yr_data:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# ---------------------------------------------------------------------
# Date querying API page, start date only
@app.route("/api/v1.0/<start>")
def tobs_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs_start_list = []

    results =   session.query(Measurement.date,\
        func.min(Measurement.tobs), \
            func.avg(Measurement.tobs), \
                func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()
    
    session.close()    

    for date, min, avg, max in results:
        tobs_start_dict = {}
        tobs_start_dict["Date"] = date
        tobs_start_dict["TMIN"] = min
        tobs_start_dict["TAVG"] = avg
        tobs_start_dict["TMAX"] = max
        tobs_start_list.append(tobs_start_dict)

    return jsonify(tobs_start_list)

# ---------------------------------------------------------------------
# Date querying API page, start and end date
@app.route("/api/v1.0/<start>/<end>")
def tobs_stat_start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs_start_end_list = []

    results =   session.query(Measurement.date,\
        func.min(Measurement.tobs), \
            func.avg(Measurement.tobs), \
                func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start, Measurement.date <= end).\
                        group_by(Measurement.date).all()

    session.close()    

    for date, min, avg, max in results:
        tobs_start_end_dict = {}
        tobs_start_end_dict["Date"] = date
        tobs_start_end_dict["TMIN"] = min
        tobs_start_end_dict["TAVG"] = avg
        tobs_start_end_dict["TMAX"] = max
        tobs_start_end_list.append(tobs_start_end_dict)

    return jsonify(tobs_start_end_list)

# ---------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)



