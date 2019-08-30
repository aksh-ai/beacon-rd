# using pandas for reading the csv file
import pandas as pd
# using numpy for easier calculations
import numpy as np
# using matplotlib for plotting
import matplotlib.pyplot as plt
from numba import cuda,vectorize, njit, jit, int32, float32, int64, float64

# read data from csv files 
mylist = ["data1.csv","data2.csv","data3.csv"]
varlist = ["temperauture","carbon monoxide","methane"]
for p in range(3):
    changing_data = pd.read_csv(mylist[p])
    # defining x and y
    x = changing_data['temp']
    y = changing_data['humid']
    
    @jit(['float64(float64, float64, int64, int64, float64)'], target='cuda')
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
    learning_rate = 0.001
    # epochs - number of iterations for this algorithm to calculate
    epochs = 1000
    # initial values for m and b
    b = 0
    m = 0

    for i in range(epochs):
        b, m = step_gradient(b, m, x, y, learning_rate)

    # y = m * x + b
    if(mylist[p]=='data3.csv'):
       nextTemp = (m * 20 + b)
    
    # constant value multiplied with analog value from sensor to get ppm value
    elif(mylist[p]=='data2.csv'):
       nextCO = (m * 20 + b)*0.0017

    # constant value multiplied with analog value from sensor to get ppm value   
    else:
       nextCH4 = (m * 20 + b)*0.00209 

print('Next Temperature is {}'.format(nextTemp))
print('Next Carbon Monoxide value is {}'.format(nextCO))
print('Next Methane is {}'.format(nextCH4))