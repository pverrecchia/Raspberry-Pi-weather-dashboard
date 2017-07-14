#!/usr/bin/env node

//This script sets up a node.js server and connects to the same database that the sensor data is written to

var mysql = require('mysql');
var path = require('path');

const express = require('express')
const app = express()

//Enter MySQL credentials and connect to the database
var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "password",
  database: "database"
});

con.connect(function(err) {
  if (err) throw err;
});


//Using Express framework, chose port to listen on

app.listen(8080)

//Serve index.html to :8080. Here, index.html is locaed in the same directory as our node script

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname + '/index.html'));
}) 

//Query the DB far days passed in query string, return the sensor data to callers of :8080/data?days=n

app.get('/data', function (req, res) {
      var days = req.query.days;
      con.query("SELECT * FROM weather_data WHERE dateTime >= (NOW() - INTERVAL ? DAY);", days, function (err, result, fields) {
        if (err) throw err;
      res.send(result);
    });
})



