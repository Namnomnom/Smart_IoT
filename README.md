# Smart_IoT_Project

## Table of Contents <!-- omit from toc -->
- [Introduction](#Introduction)
- [Precondition](#Precondition)
- [Goal_of_this_project](#Goal_of_this_project)
- [Exercises_for_this_project](#Exercises_for_this_project)
  - [Exercise_1_REST_API](#Exercise_1_REST_API)
  - [Exercise_2_(Data_Aggregation_and_Visualization)](#Exercise_2_(Data_Aggregation_and_Visualization))
  - [Exercise_3_(IoT_Device_Connectivity,Reporting,Alerting)](#Exercise_3_(IoT_Device_Connectivity,Reporting,Alerting))
  - [Exercise_4_(High-Level_Interfacing)](#Exercise_4_(High-Level_Interfacing))

## Introduction 

This Smart_IoT project deals with advanced applications and methods in the Internet of Things. It builds on top of undergrad-level IoT courses where we may have learned many details about underlying protocols, hardware, security and power management. In this project, we want go beyond this point and look into more high-level topics which allows us not only to engineer small-ish IoT solutions, but also aquire a top-down systems engineering perspective for applications like sensor networks and Edge AI.

## Precondition

in order to successfully complete this project, these requirements are necessary.
- intermediate Python
- version control with Git
- beginner's experience with ESP32
- beginner's experience with Raspberry Pi or other IoT stuffs
- used Docker, InfluxDB or Grafana before

## Goal_of_this_project

Define and implement a working solution using Python. Every participant in this project has to deliver Python code and, amongst other technology, work with Git version control

## Exercises_for_this_project
Note: Each exercise has been uploaded in a folder
### Exercise_1_REST_API
Implement a REST service using Python and FastAPI.
1. Implement a REST service in src/main.py using FastAPI that should provide the following end points:
- "/sensors/1/datapoints": GET endpoint that returns a float list named data that contains the latest sensor data
- "/actuators/1": PUT endpoint that takes a float value and simulates some action that influences the sensor data by doubling the input and adding it to its internal list of sensor data
- "/sensors/1/datapoints": DELETE endpoint that takes no input and clears the list of sensor data

Make sure that your service uses JSON for encoding the data.
- Test if your service works correctly by running test/test_fastapi.py.
- Make sure your code is pushed back into your personal namespace. You see if the automatic test ran correctly when a green tickmark appears.

### Exercise_2_(Data_Aggregation_and_Visualization)
In this exercise, you're going to set up InfluxDB for data aggregation and Grafana for visualization.
1. Install Influx via Docker as described here: https://docs.influxdata.com/influxdb/v2/install/?t=Docker (make sure you run Docker 2.x and not some older version) OR create an Influx cloud account
2. log in on http://localhost:8086 (or the cloud URL), respectively, set your organization name arbitrarily, create a bucket "smart-iot" and an API token

#### Grafana Setup 
set up Grafana like this: https://grafana.com/docs/grafana-cloud/quickstart/ and then connect to Influx like this: https://docs.influxdata.com/influxdb/cloud/tools/grafana. 
Also create a docker-compose configuration for your Influx+Grafana setup: https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/#run-grafana-via-docker-compose

Create then a dashboard that shows the information you are going to provide to the user in your demo scenario. Afterwards, make a screenshot of the dashboard and upload it.

### Exercise_3_(IoT_Device_Connectivity,Reporting,Alerting)
This exercise deals with setting up some piece of IoT hardware and retrieving data from some sensors as well as generating automatic reports and alarms.

Hardware Pick-Up:

We will be using M5Stack as a platform because this works out-of-the-box and needs no extensive cabling, power issues etc. and can be used with a low-code GUI as well as with MicroPython.

M5Stack Setup:
- Connect the M5Stack (we use the Core2 model) and set up M5Burner and UIFlow (https://docs.m5stack.com/en/quick_start/m5core/uiflow).

Visualization:

First, play with UIFlow to find out what this is capable of. Add the MQTT module to publish some of the sensor data. Use the MQTT Broker (credentials below) to forward some data from the connected or built-in sensors. Then subscribe to the data using some MQTT message visualization tool, e.g. http://mqtt-explorer.com/

Data Reading: 

Next, use MicroPython to read some sensor data. Connect some other sensors and play with them, check how you can use the data that comes back.

Alerting: 

Set up alerts for a concrete use case using InfluxDB, Grafana or a custom MicroPython script. This does not need to trigger sophisticated actions, but show up for the user in some way, e.g. via email, push notifications,...
Whenever the user receives the alert, they should be able to quickly understand the problem in an intuitive way.


### Exercise_4_(High-Level_Interfacing)
For your desired architecture, implement any missing REST APIs. At least one reasonable use of a self-implemented REST API needs to be included.
