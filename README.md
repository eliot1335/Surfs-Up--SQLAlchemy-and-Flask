# Surfs Up! -  SQLAlchemy

In this exercise, we will be practicing how to interact with ORM using sqlalchemy and sqlite.
The exercise breaks down to two parts: 
- the climate_starter.ipynb notebook file where we create engine and query the data, then stuff them into pandas dataframe for further analysis and matplotlib plotting.
- the app.py file where we create API site providing json data using flask package.

## Climate Analysis and Exploration

### Precipitation Analysis
In this portion, we are going to use the datasets and collect a year worth of precipitation scores. We will design a query to retrieve the last 12 months of precipitation data and plot them into a bar chart. I approached this part by first inspect the tables using inspector package, have a look at the columns of the table, then design my queries.

I use my query to extract the last date recorded in the meansurement table, then use daytime package to help calculate the date one year prior to the last date.

Given the dates, I would be able to extract the data I want and plot them using pandas and matplotlib, I can also get a summary using .describe method on the pandas df.

### Station Analysis
Then I will design queries to figure out the total number of stations is the dataset, find out the most active station which has the most records, and then extract the tobs (temperature observation data) of last year recorded from the most active station. I will plot the data into a histagram using matplotlib.

## Climate App
### Routes
In this part of the homework, I will create a local API site using flask and display all available routes in homepage. In these routes, jsonifyied data of designed queries will be stored. Routes and queries are:
- Precipitaion: all precipitation values in the dataset
- Stations: informations of all stations
- TOBS: the json list of temperature observations for previous year
- Start: 
- Start/End:
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
