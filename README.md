# Smart_IoT_Project

## Introduction 

This Smart_IoT project deals with advanced applications and methods in the Internet of Things. It builds on top of undergrad-level IoT courses where we may have learned many details about underlying protocols, hardware, security and power management. In this project, we want go beyond this point and look into more high-level topics which allows us not only to engineer small-ish IoT solutions, but also aquire a top-down systems engineering perspective for applications like sensor networks and Edge AI.

## Precondition

in order to successfully complete this project, these requirements are necessary.
- intermediate Python
- version control with Git
- beginner's experience with ESP32
- beginner's experience with Raspberry Pi or other IoT stuffs
- used Docker, InfluxDB or Grafana before

## goal of this project

Define and implement a working solution using Python. Every participant in this project has to deliver Python code and, amongst other technology, work with Git version control

## Exercises for this project 
### Exercise 1: REST API
Implement a REST service using Python and FastAPI.
1. Implement a REST service in src/main.py using FastAPI that should provide the following end points:
- "/sensors/1/datapoints": GET endpoint that returns a float list named data that contains the latest sensor data
- "/actuators/1": PUT endpoint that takes a float value and simulates some action that influences the sensor data by doubling the input and adding it to its internal list of sensor data
- "/sensors/1/datapoints": DELETE endpoint that takes no input and clears the list of sensor data

Make sure that your service uses JSON for encoding the data.
2. Test if your service works correctly by running test/test_fastapi.py.
3. Make sure your code is pushed back into your personal namespace. You see if the automatic test ran correctly when a green tickmark appears.


