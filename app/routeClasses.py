
from app.models import *
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

from app.utils import *
###################################### classes #########################################

class TestConnection(Resource):
    def get(self, message):
        data1 = str(message)
        message = list(data1)
        data =GetSensorReading(message)
        print("in class and data is {}".format(data))
        return data


class GetLight(Resource):
    def get(self, message):
        data1 = str(message)
        message = list(data1)
        data =GetSensorReading(message)
        return data

class getDataFromDB(Resource):
    def get(self, num, name):
        user = Person.query.filter_by(name=name).first()
        val = user.id
        list1 = []
        if (num == 255):
            print("WOWOW in if")
            MRead = MoistureRead.query.all()
        else:
            # MRead = MoistureRead.query.limit(num).all()
            MRead = MoistureRead.query.filter_by(person_id=val).order_by(MoistureRead.id.desc()).limit(num).all()
            print("Mread is {}".format(MRead))
        for elements in MRead:
            val = int(elements.MReading)
            list1.append(val)
        if not(num == 255):
            list1.reverse()
        return jsonify(list1)
        

class GetMoistureReading (Resource):
    def get(self, message):
        data = str(message)
        message = list(data)
        result = GetSensorReading(message)
        #sensorReading = getMoisture("moist", 5, user)          
        #return jsonify(Sensor_result =sensorReading,
         #           Recomendation=reading)
        return jsonify(result)

class ChangeAutoValue(Resource):    
    def get(self, num, name):
        num = str(num)
        num = list(num)
        while len(num)<32:
            num.append(0)
        val = setAutoMeasure(num, name)
        return(val)

class GetAutoValue(Resource):
    def get(self, name):
        message = list("two")
        confirmMessge = list("ok")
        while len(message)<32 and len(confirmMessge)<32:
            message.append(0)
            confirmMessge.append(0)
        val = getAutoValue(message, name)
        return (val)

class dataNameStore(Resource):
    def get(self, name):
        result = DatabaseStore(name)
        return (result)
# gets a list of the minimun values set and returns them
class getalAutoValue(Resource):
    def get(self, name):
 
        result = getMinValData(name)
        print("result is {}".format(result))
        return result 

# turns on watering system
class TurnOnNOw(Resource):
    def get(self):
        message = list("ton")
        confirmMessge = list("ok")
        while len(message)<32 and len(confirmMessge)<32:
            message.append(0)
            confirmMessge.append(0)
        result = TurnSystemOn(message)
        
        return result  # result should be "turned on system"
    

#Gets the temperature value
class GetTempValue(Resource):
    def get(self, sensor):
        print("in gettemp and sensor is {} ".format(sensor))
        data = str(sensor)
        message = list(data)
        result = GetSensorReading(message, sensor)
        print("result from GetTempValue is {} ".format(result))
        return result  # result should be "turned on system"
    