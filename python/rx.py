from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import pyrebase
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('beacon-dddae-firebase-adminsdk-2qj4p-bedd444b20.json')
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


BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            #print("Signal Strength: {}".format(rssi_value))
            status = self.get_modem_status()
            sys.stdout.flush()
            

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True) 
        try:
            #print(bytes(payload).decode("utf-8",'ignore'))
            value=bytes(payload).decode("utf-8",'ignore')
            #print(type(value))
           # intval = int(value)
            #print("\nReceived: ")
            Data = []
            value = value.strip("\x00")
            Data = value.split(" ")
            if(Data[0]!=""):  
                print(Data)
                Node=Data[0]
                MQ7=Data[1]
                MQ2=Data[2]
                Temp=Data[3]
                Humid=Data[4]
                Ack=Data[5]
                datas={
                    "MQ2":MQ2,
                    "MQ7":MQ7,
                    "Temp":Temp,
                    "Humid":Humid,
                    "Ackn":Ack,
                }
                date=str(datetime.datetime.now())
                results = db.child("Data").child(Node).set(datas)
                print(results)
                doc_ref = fb.collection(u'data').document(date)
                doc_ref.set({
                u"Node":Node,
                u"MQ2":MQ2,
                u"MQ7":MQ7,
                u"Temp":Temp,
                u"Humid":Humid,
                u"Ackn":Ack,
            })
            rssi_value = self.get_rssi_value()
            print("Signal Strength: {}".format(rssi_value))
            print(Data)
            
        except ValueError:
            pass
            #print("")    
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT) 

lora = LoRaRcvCont(verbose=False)
lora.set_mode(MODE.STDBY)
#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm

#lora.set_pa_config(pa_select=1)
lora.set_pa_config(pa_select=1, max_power=23)
#lora.set_bw(BW.BW125)
#lora.set_coding_rate(CODING_RATE.CR4_8)
#lora.set_spreading_factor(12)
#lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
#lora.set_low_data_rate_optim(True)


try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()