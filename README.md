# Raspberry-Pi-weather-dashboard
Measure weather data with Python, log it to MySQL, and view it in a dashboard over the local network with by Node.js

This isn't a new concept my any means but it's my first Pi project and I've documented the steps I took to set it up. End to end, here what it does:

- A Python script polls temperature, pressure and humidity every 5 minutes
- Sensor data is written to a MySQL database running on the Pi
- A Node.js server also running on the Pi querys MySQL when data is needed
- Users can view a basic dashboard to view the most recent sensor readings and historical data plots


## Part 1: Measuring weather data

I used the BME280 sensor together with [Adafruit's BME280 Python libray](https://github.com/adafruit/Adafruit_Python_BME280). It is pretty straightforward to use the example script to initialize the sensor and begin reading the data.

## Part 2: Configuring MySQL and writing data to it

I chose to store the sensor data in MySQL for this project, but SQLite 3 seems to be another popular option. I followed [this tutorial](http://raspberrywebserver.com/sql-databases/using-mysql-on-a-raspberry-pi.html) to get started.
Note that we want the MySQL Python library in addition to MySQL itself which is what you get via:

`sudo apt-get install mysql-server python-mysqldb`

After I chose a username + password for the MySQL setup I created` a single database and a single table via:

```
CREATE DATABASE rpi_Database;
USE rpi_database;
CREATE TABLE weather_data (DATETIME dateTime, FLOAT(4,2) temperature, FLOAT(6,2) pressure, FLOAT(5,2) humidity)
```

FLOAT(X,Y) will declare a float with Y digits to the right of the decimal point and X digits total.

Now that the table is set up, the sensor-reading python script needs to be updated to write to it.

-connect to db using credentials and db name
-use INSERT command


<find tutorial>

## Part 3: Scheduling sensor readings

I chose to use crontab to schedule the python script so it runs every 5 minutes. Access the crontab editor via

`crontab -e`

For more details on how crontab works, I suggest [this explanation](http://kvz.io/blog/2007/07/29/schedule-tasks-on-linux-using-crontab/) but to get my script to run every 5 minutes, I used:

`crontab entry`

There are two more minor steps before the script will run automatically. First, add

`shebang` to the _very first_ line of the python script, as that will allow it to be executable. We also need to set executable permissions on the file itself using `sudo chmod +x weather.py`

Now, the python script will run every 5 minutes and log the sensor data to the MySQL table!

## Part 4: Node.js server

I chose to use Node.js and the [Express framework](https://expressjs.com/en/starter/installing.html) to set up a basic webserver that will allow other devices on the local network to access the data in the databaseThe Node.js (server.js) does a few things:

-link it to the database
-choose a port to listen on
-Setup homepage to return index.html
-Setup a data api to handle request for data from index.html 

I also configured the node server to start automatically when the Pi powers up. I attempted to use crontab for this as well but it didn't seem to work properly. I tried a few strategies but was ultimately successful after finding [this forum post](https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=138861)

## Part 5: Making a dashboard

Lastly, I made a very simple dashboard (index.html) that will display the data retrieved from the database. The most recent measurements are showed at the top of the dashboard. Three charts show the 3-day trailing measurements of temperature, humidity and pressure.

-Call the data endpoint and Query string to select amount of data
-experiementing with data decimation to not crowd graphs.
-chart.js  
