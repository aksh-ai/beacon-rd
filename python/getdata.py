import firebase_admin
import csv
import time
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('beacon-dddae-firebase-adminsdk-2qj4p-4ab2ce47dd.json')
firebase_admin.initialize_app(cred)

flag=0
    # print(u'{} => {}'.format(doc.id, doc.to_dict()))
while(flag==0):
 db = firestore.client()
 docs = db.collection(u'data').get()
 varlist=["Humid","MQ7","MQ2"]
 with open('data3.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["experience","salary"])
    for doc in docs:
        docid=doc.id
        data=(doc.to_dict())
        for key,value in data.items():
            # print(key)
            if(key=="Temp"):
                for i in range(3):
                    for keys,values in data.items():
                        if(keys=="Humid"):
                            writer.writerow([value, values])
    csv_file.close()                        
 with open('data2.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["experience","salary"])
    for doc in docs:
        docid=doc.id
        data=(doc.to_dict())
        for key,value in data.items():
            # print(key)
            if(key=="Temp"):
                for i in range(3):
                    for keys,values in data.items():
                        if(keys=="MQ2"):
                            writer.writerow([value, values])
    csv_file.close()                        
 with open('data1.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["experience","salary"])
    for doc in docs:
        docid=doc.id
        data=(doc.to_dict())
        for key,value in data.items():
            # print(key)
            if(key=="Temp"):
                for i in range(3):
                    for keys,values in data.items():
                        if(keys=="MQ7"):
                            writer.writerow([value, values])  
    csv_file.close()                         
    print("Waiting for 5 minutes")
    time.sleep(300)                                                                               