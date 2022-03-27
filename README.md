# Tracking the International Space Station

 Given an abundance of positional data, this project is meant to sort through different kinds of information about the sightings of the International Space Station (ISS), such as the ISS position and velocity at given times as well as the cities and countries it can be seen in, and return specific information that a user might be looking for. This repository contains 4 other files: a Dockerfile, a Makefile, a python script called app.py, and a tester script\
 called test_app.py. All of which play a role in achieving this goal.

Before running this application and building the container, you must first download the two data sets used by inputting the following in your terminal:

> wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml

> wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA01.xml


## What Is In This Repository?
This repository contains a flask application app.py that sorts through different types of positional and sighting data for the ISS and returns more specific information. For example, if you want a list of all the countries where the ISS has been spotted in, there is a function for that. Furthermore, if you want a list of all the cities in one of those countries where the ISS has been spotted in, there is also a function for that. 

Additionally, this application has a tester script test_app.py that tests almost all of the functions to make sure it is returning the right type. 

This repository contains a Dockerfile that containerizes the application and data sets and sets a default command to launch the application. 

Lastly, this repository contains a Makefile that actually builds the container and starts the application.

## Building This Application
To build and run the containerized app, you can simply type "make" into the command line. 

If you want to change the name to your own Docker Hub username type:
> NAME= *name goes here* make

Additionally, if you just want to build it you can type the following into your command line:
> docker build -t ${NAME}/isstracker:latest .

To run it:
> docker run -d -p 5022:5000 ${NAME}/flask-isstracker:latest

put your Docker Hub username where it says ${NAME}

To pull a pre-containerized copy of the app from Docker Hub type the following into your command line:
> docker pull niccoleriera/flask-isstracker:latest

## How To Interact With The Application
To see all of the options this application has input the following in the command line:
> curl localhost:5022/

This should return a list of options that says something like this:
```
    ### ISS Tracker ###

    Informational and management routes:

    /                                                    (GET) print this information
    /reset                                               (POST) reset data, load from file

    Routes for querying positional and velocity data:

    /epochs                                              (GET) list all epochs
    /epochs/<epoch>                                      (GET) info on a specific epoch


    Routes for querying sighting data:

    /countries                                           (GET) List of all countries
    /countries/<country>                                 (GET) All data associated with <country>
    /countries/<country>/regions                         (GET) List of all regions ina given country
    /countries/<country>/regions/<region>                (GET) All data associated with <region>
    /countries/<country>/regions/<region>/cities         (GET) List of all cities in a given region
    /countries/<country>/regions/<region>/cities/<city>  (GET) All data associated with <city>
```

What this is saying is for example, if you want a list of all countries where the ISS has been spotted, type:
> curl localhost:5022/countries
into your command line.

Let's say it returns United_States. If you want all of the data associated with where it was spotted in the United_States, you would type
> curl localhost:5022/countries/United_States

This should return dictionaries that all look similar to the following:
```
    {
      "city": "Le_Grand",
      "country": "United_States",
      "duration_minutes": "< 1",
      "enters": "9 above NNE",
      "exits": "10 above NNE",
      "max_elevation": "9",
      "region": "California",
      "sighting_date": "Fri Feb 25/04:15 AM",
      "spacecraft": "ISS",
      "utc_date": "Feb 25, 2022",
      "utc_offset": "-8.0",
      "utc_time": "12:15"
    }
```
This shows the time, date, country, region, etc. where the ISS was spotted.

Before doing any other command other than '/', you must first run 
> curl localhost:5022/reset 
or the functions will not be able to read the data and execute the commands.

If at any time, you decide to make an edit to the application, in order to run the application again, you must input
> curl localhost:5022/reset
to read the data from XML to dictionary again. Otherwise, the other commands will not work.

## Sources
ISS_COORDS_2020-12-02 - Public Distribution File - Welcome ... https://cloud.csiss.gmu.edu/uddi/en_AU/dataset/iss-coords-2020-12-02/resource/e438c779-9b2a-4281-bf7f-3c658b5f8598. 

ISS_COORDS_2020-12-02 - xmlsightingdata_citiesusa01 ... https://cloud.csiss.gmu.edu/uddi/en_AU/dataset/iss-coords-2020-12-02/resource/1414fb5b-2db8-4bf6-a581-aa1dc1895390. 