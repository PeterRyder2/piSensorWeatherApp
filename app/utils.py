
from flask import jsonify
from app.models import *
import datetime
from datetime import datetime
import time
from app.NRF24RadioSetUp import *
import numpy as np



message2 = list("two")
while len(message2)<32:
    message2.append(0)


# adds the moisture reading to the database
def getMinValData(name):
    user = Person.query.filter_by(name=name).first()
    dateList = []
    valueList = []
    print("user is {}".format(user))
    val = user.id
    print("val is {}".format(val))
    dResult = MinValue.query.filter_by(person_id = val).order_by(MinValue.dateOfChange.desc()).all()
    for elements in dResult:
        print("elements.data is {}".format(elements.dateOfChange))
        dateList.append(elements.dateOfChange)
        valueList.append(elements.changeTo) 
    return(dateList, valueList)

def databaseImport(moistureValue, user):
    #if type(moistureValue) is not int: 
     #   raise ValueError("mositureValue is not an int")
    if moistureValue < 0: 
        raise ValueError("mositureValue cannot be negative")
    #if type(user) is not str: 
     #   raise ValueError("user is not an string")
    try:
        print("in databaseImport")
        user = Person.query.filter_by(name=user).first()
        M1 = MoistureRead(MReading= moistureValue, person=user)
        db.session.add(M1)
        db.session.commit()
        return "Successfully added reading"
    except Exception as err:    
        print("error accessing database")
        print(err)   

# stores a name in the database
def DatabaseStore(name):
    if type(name) is int:
        raise ValueError("name is of type integer")
    try:
        print("in DataName Store")
        users = Person.query.all()
        print("Users are {}".format(users))

        for p in users:
            if p.name == name:
                return "user Already exists"
        else:
            N1 = Person(name =name)
            db.session.add(N1)
            db.session.commit()
            return "New User added"
    except Exception as err:    
        print("error accessing database")
        print(err)   

# turn on the watering system now
def TurnSystemOn(message):
    for i in range(50):
        start = time.time()
        radio.write(message)
        print("sent the message:{}".format(message))
        #radio.startListening()
        print(i)
    return "turned on system"






# function translates received message into unicode characters
def mTranslate(newMessage):
    print("Translating our received message to Unicode characters...")
    string = ""
    print("new message is {}".format(newMessage))
    for n in newMessage:
        if (n>=32 and n<= 126):
            print("in if    ")
            string +=chr(n)
    print("String is  {}".format(string))
    return string

# function talk to the arduino. it is called in the if else statments
# depending on the option given by the user
def getMoisture(option, recurseNum, user):
    print("in getMoisture")
    message = list(option)
    arrayMoist = []
    print(message)
    # appends zeros to end of message
    while len(message)<32:
        message.append(0)

    for i in range(2):
        start = time.time()
        radio.write(message)
        print("sent the message:{}".format(message))
        radio.startListening()

        while not radio.available(0):
            time.sleep(1/100) 
            if time.time() - start > 2:
                print("Timed out")
                break
        
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("received: {}".format(receivedMessage))
        # if no value then break from the loop
        if not(receivedMessage):
            if recurseNum != 5:
                recurseNum += 1
                #user1 = user
                return getMoisture("one", recurseNum, user)
            else:
                print("error reading message")
                raise ConnectionError("failed to connect to Arduino")
                
        # translate the returned message into unicode characters
        transMessage = mTranslate(receivedMessage)
        print("transMessage = {}" .format(transMessage))

        radio.stopListening()
        value = receivedMessage
        arrayMoist.append(value)
        print(arrayMoist)
    #avg = random.randint(1,101)
    avg = np.mean(arrayMoist)
    for e in arrayMoist: print(e)
    # print ("AVG is {} ").format(avg)
    # print("in flask")
    val = databaseImport(avg, user)
    return(transMessage)



def getAutoValue(message, name):
    for i in range(2):
        print("here")
        start = time.time()
        for j in range(5):
            print("and now here")
            radio.write(message)
        
            print("sent the message:{}".format(message))
            time.sleep(0.25)
            radio.startListening()

            while not radio.available(0):        
                time.sleep(1/100)
                if time.time() - start > 2:
                    print("Timed out")
                    break
                
        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print(receivedMessage)
        while receivedMessage[0] != 0:
            return(receivedMessage[0])
    return"Failed to comminucate with the Arduino"
             



# sets the auto value in the arduino    
def setAutoMeasure(num, name):
    if (num == "none"):
        return jsonify("Ok")
    for i in range(3):
        start = time.time()
        print("num is + {0}".format(num))
        for j in range(10):
            print("Writing message")
            radio.write(num)
            time.sleep(0.25)
        print("sent the message:{}".format(num))
        
        time.sleep(1)
    for i in range(5):
        val = getAutoValue(message2, name)
        time.sleep(0.25)

    r = DataNameAutoStore(val,name)
    print(r)
    print(" in Set auto measure....Returning val which is ".format(val))
    return (val)
# end optionTwo
# stores the auto value in database with user and date  
def DataNameAutoStore(val,name):
    #if type(val) is not int: 
     #   raise ValueError("val is not an int")
    #if val < 0: 
     #   raise ValueError("val cannot be negative")
    #if type(name) is not str: 
    #    raise ValueError("name is not an string")
    try:
        user = Person.query.filter_by(name=name).first()
        print("user is {}".format(user))
        userID = user.id
        print("val is {}".format(val))
        dataStore = MinValue(changeTo= val,person_id= userID)
        db.session.add(dataStore)
        db.session.commit()
        return "Successfully added reading"
    except Exception as err:    
        print("error accessing database for MinValue")
        print(err)   


def GetSensorReading(message, sensor=None, dataEntry=None):
    try:
        #message = list("one")
        rawMessageVal = ''.join(str(e) for e in message if e != 0)
        print(rawMessageVal)
        while len(message)<32:
            message.append(0)

        for i in range (5):
            print (i)
            start = time.time()
            radio.write(message)
            print("sent the message:{}".format(message))
            radio.startListening()

            while not radio.available(0):
                time.sleep(1/100) 
                if time.time() - start > 2:
                    print("Timed out")
                    break
            
            receivedMessage = []
            radio.read(receivedMessage, radio.getDynamicPayloadSize())
            print("received: {}".format(receivedMessage))

            string = mTranslate (receivedMessage)
            # used in TestConnection conditional if a connected just return it
            if rawMessageVal == "connect" and string == "Connected":
                print("string is {} and message is {} ".format(string,rawMessageVal))
                radio.stopListening()
                return string 
            elif i==4 and rawMessageVal == 'connect':
                string = "No Connection"
                radio.stopListening()
                return string


            radio.stopListening()
            time.sleep(1)
        else:
            return float(string)
    except:
        raise ValueError("Error in GetSensorReading")