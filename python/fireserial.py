from serial import SerialException
import pyrebase
import datetime
import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('beacon-dddae-firebase-adminsdk-2qj4p-4ab2ce47dd.json')
firebase_admin.initialize_app(cred)
fb = firestore.client()
config = {
    "apiKey": "AIzaSyD3_MZ_UEnz3G_cwXBAA9Fv1RZlVqxo2s0",
    "authDomain": "beacon-dddae.firebaseapp.com",
    "databaseURL": "https://beacon-dddae.firebaseio.com",
    "projectId": "beacon-dddae",
    "storageBucket": "beacon-dddae.appspot.com",
    "messagingSenderId": "717730730032",
    "appId": "1:717730730032:web:665ff2d3aa744e4c"
  }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
def connect():
    while(True):
        try:
            arduino=serial.Serial('com9',9600)
            performcode(arduino)
        except SerialException:
            continue
    
def performcode(arduino):
    
    while(True):
        arduinoData=arduino.readline()
        arduinoData=arduinoData.decode('utf-8')
        arduinoData=arduinoData.strip("\n")

        arduinoData=arduinoData.strip("\r").rstrip("\x00")
        Data=arduinoData.split(",")
        if(Data[0]!=""):  
            print(Data)
            MQ2=Data[0]
            MQ7=Data[1]
            Temp=Data[2]
            Humid=Data[3]
            aq=Data[4]
            datas={
                "MQ2":MQ2,
                "MQ7":MQ7,
                "Temp":Temp,
                "Humid":Humid,
                "Ackn":aq,
            }
            date=str(datetime.datetime.now())
            results = db.child("Data").update(datas)
            print(results)
            doc_ref = fb.collection(u'data').document(date)
            doc_ref.set({
            u"MQ2":MQ2,
            u"MQ7":MQ7,
            u"Temp":Temp,
            u"Humid":Humid,
            u"Ackn":aq,
        })
        
connect()