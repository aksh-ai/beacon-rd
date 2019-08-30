# using pandas for reading the csv file
import pandas as pd
# using numpy for easier calculations
import numpy as np
# using matplotlib for plotting
import matplotlib.pyplot as plt
# using python firebase for updating value produced by this program in database
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# give firebase json file and credentials to connect and do the update process in database
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
# read data from csv files 
mylist = ["data1.csv","data2.csv","data3.csv"]
varlist = ["temperauture","carbon monoxide","methane"]
for p in range(3):
    changing_data = pd.read_csv(mylist[p])
    # defining x and y
    x = changing_data['experience']
    y = changing_data['salary']

    # plot a normal scatter graph
    plt.scatter(x, y)
    #plt.show()

    def compute_error(b, m, x_points, y_points):
        total_error = 0
        for i in range(0, len(x_points)):
            # get x and y for the point in the graph
            x = x_points[i]
            y = y_points[i]
            # add the current error to the total error using error linear regression
            total_error += (y - (m * x + b)) ** 2
        # divide by the length of the points to get a more accurate value
        return total_error / float(len(x_points)) 

    def step_gradient(b_current, m_current, x_points, y_points, learning_rate):
        # define initial values
        b_gradient = 0
        m_gradient = 0
        # how many elements are in the list
        N = float(len(x_points))
        for i in range(0, len(x_points)):
            # get x and y for the specific point
            x = x_points[i]
            y = y_points[i]
            
            # calculate b and m by using the partial derivative of the linear regression function
            b_gradient += -(2 / N) * (y - (m_current * x + b_current))
            m_gradient += -(2 / N) * x * (y - (m_current * x + b_current))
        # set the new b and m by multiplying the learning rate to the gradient for avoiding overfitting
        # then calculate the difference between the current gradient and new gradient by getting the actual new b and m
        new_b = b_current - learning_rate * b_gradient
        new_m = m_current - learning_rate * m_gradient
        return [new_b, new_m]    

    # define learning rate for not overfitting
    learning_rate = 0.0001
    # epochs - number of iterations for this algorithm to calculate
    epochs = 10000
    # initial values for m and b
    b = 0
    m = 0

    for i in range(epochs):
        b, m = step_gradient(b, m, x, y, learning_rate)

    # plot the linear regression prediction
    plt.scatter(x, y)
    plt.plot(x, m * x + b, color='red')
    #plt.show()

    # y = m * x + b
    if(mylist[p]=='data1.csv'):
       nextTemp = (m * 20 + b)
       datas={
           "nextTemp": nextTemp
       }
       results = db.child("Data").update(datas)
    
    # constant value multiplied with analog value from sensor to get ppm value
    elif(mylist[p]=='data2.csv'):
       nextCO = (m * 20 + b)*0.0017
       datas={
           "nextCO": nextCO
       }
       results = db.child("Data").update(datas)

    # constant value multiplied with analog value from sensor to get ppm value   
    else:
       nextCH4 = (m * 20 + b)*0.00209 
       datas={
           "nextCH4": nextCH4
       }
       results = db.child("Data").update(datas)    

print('Next Temperature is {}'.format(nextTemp))
print('Next Carbon Monoxide value is {}'.format(nextCO))
print('Next Methane is {}'.format(nextCH4))  

