import firebase_admin
import csv
import time
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('beacon-dddae-firebase-adminsdk-2qj4p-4ab2ce47dd.json')
firebase_admin.initialize_app(cred)


db = firestore.client()
docs = db.collection(u'data').get()

csv_list=["data1.csv","data2.csv","data3.csv"]
keys= ["MQ7","MQ2","Temp"]

with open('data3.csv', 'w') as csv_file:
   writer = csv.writer(csv_file)
   writer.writerow(["temp","humid"])
   for doc in docs:
       docid=doc.id
       data=(doc.to_dict())
       for key,value in data.items():
            if(key=="Temp"):
               for keys,values in data.items():
                   if(keys=="Humid"):
                        writer.writerow([value, values])
csv_file.close()

'''with open('data2.csv', 'w') as csv_file:
   writer = csv.writer(csv_file)
   writer.writerow(["temp","humid"])
   for doc in docs:
       docid=doc.id
       data=(doc.to_dict())
       for key,value in data.items():
            if(key=="Temp"):
               for keys,values in data.items():
                   if(keys=="MQ2"):
                        writer.writerow([value, values])
csv_file.close()'''

'''for ctr in range(0,3):
with open(csv_list[], 'w') as csv_file:
   writer = csv.writer(csv_file)
   writer.writerow(["temp","humid"])
   for doc in docs:
       docid=doc.id
       data=(doc.to_dict())
       for key,value in data.items():
            if(key=="Temp"):
               for keys,values in data.items():
                   if(keys=="Humid"):
                        writer.writerow([value, values])
csv_file.close()'''