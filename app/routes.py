from app import db, app, api
import RPi.GPIO as GPIO 
from app.lib_nrf24 import NRF24
from app.models import Person, MoistureRead, UserSignIn, MinValue
import time
import spidev
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from app.routeClasses import getDataFromDB, GetMoistureReading, ChangeAutoValue,\
                            GetAutoValue, dataNameStore, getalAutoValue, TurnOnNOw,\
                            TestConnection, GetTempValue, GetLight
from app.utils import getMinValData, databaseImport, DatabaseStore,\
                    TurnSystemOn, mTranslate, getMoisture, getAutoValue,\
                    setAutoMeasure, DataNameAutoStore
from app.NRF24RadioSetUp import *




try:
    # ALL of the API calls
    api.add_resource(TurnOnNOw,'/ton/') # get a moisture reading
    api.add_resource(GetMoistureReading,'/gmr/<string:message>') # get a moisture reading
    #api.add_resource(GetMoistureReading,'/gmr/<string:user>') # get a moisture reading
    api.add_resource(getDataFromDB,'/gd/<int:num>/<string:name>') # gets mositure data from the data base depending on the USer
    api.add_resource(ChangeAutoValue, '/cav/<int:num>/<string:name>') # changes the auto min value 
    api.add_resource(GetAutoValue, '/gav/<string:name>') # get auto value
    api.add_resource(dataNameStore, '/std/<string:name>') # stores the name of the user 
    api.add_resource(getalAutoValue, '/gaav/<string:name>') # gets all the autovalues for a given user with dates
    api.add_resource(TestConnection, '/TestConnection/<string:message>')
    api.add_resource(GetTempValue, '/GetTempValue/<string:sensor>')
    api.add_resource(GetLight, '/GetLight/<string:message>')
    


except Exception as err:    
        print("Error creating api links")
        print(err)   




############################################
## command to run on command line 
#sudo FLASK_APP=run.py flask run --port=80##
# sudo FLASK_APP=run.py flask run --host=0.0.0.0
#
#
# set the service like this
# to set the systemd (which is the commands needed to run the flask app on boot)
# [Unit]
# Description= FlaskAppStartup

# [Service]
# ExecStart=/usr/bin/python /home/pi/Documents/dataplicityTest/run.py 

# [Install]
# WantedBy=mulit-user.target
#
# save this in /lib/systemd/service. This is saved as systemdTest.service
# Test this command that 
# systemctl status NAME_OF_SERIVCE (in this instance systemdTestService)
# systemctl start NAME_OF_SERIVCE (in this instance systemdTestService) (to start this service)
# systemctl stop NAME_OF_SERIVCE (in this instance systemdTestService) (to stop the service)
# systemctl enable NAME_OF_SERIVCE (in this instance systemdTestService) (to start the flask app at boot time)


#



# ####
#############################################

    
