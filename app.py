from flask import Flask, jsonify
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
#Sept 6-20 Dates to choose
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
print (Base.classes.keys())
# Save references to each table
measure = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)
@app.route("/api/date")
def welcome(date):
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dttimedelta(days=365)
    hawaii_results = session.query(measure.date, measure.prcp).filter(measure.date >= last_year).all()
    hawaii_trip = pd.DataFrame(hawaii_results, columns = ['date', 'prcp'])
    sum_of_rain = []
    for result in rain:
        row = {}
        row ["date"] = rain[0]
        row["prcp"] = rain[1]
        sum_of_rain.append(row)
    return jsonify(hawaii_results)

@app.route("/api/v1.0/stations")
def station():
    station_list = session.query(measure.station).order_by(func.count(measure.station).desc()).all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session_results = session.query(measure.tobs).filter(measure.station=='USC00519281').filter(measure.date >=last_year).all()
    return jsonify(session_results)

@app.route('/api/v1.0/<start>') 
#Sept 6-20 Dates to choose landing in Hi on my Birfday~~~~~
def start(start=None):
    tobs_start = (session.query(measure.tobs).filter(measure.date.between(start, '2017-09-06')).all())
    return jsonify(tobs_start)

@app.route('/api/v1.0/<start>/<end>') 
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    start_end = session.query(func.min(measure.tobs), func.avg(measure.tobs), func.max(measure.tobs)).\
        filter(measure.date >= start_date).filter(measure.date <= end_date).all()

    return jsonify(start_end)
if __name__ == '__main__':
    app.run(debug=True)