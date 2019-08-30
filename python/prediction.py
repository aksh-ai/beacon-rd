import pandas as pd 
from threading import *
from multiprocessing import Process

mylist = ["data1.csv","data2.csv","data3.csv"]  # add three more csv files

learning_rate = 0.001
epochs = 100

for itr in range(len(mylist)):
	data = pd.read_csv(mylist[itr])
	x = data['temp']
	y = data['humid']
	m = 0
	b = 0

	for epoch in range(epochs):
		b_slope = 0
		m_slope = 0
		n = len(x)
		N = float(len(x))
	        
		for trainable in range(0, n):
			x_train = x[trainable]
			y_train = y[trainable]
			b_slope += -(2 / N) * (y_train - (m * x_train + b))
			m_slope += -(2 / N) * x_train * (y_train - (m * x_train + b))

		new_b = b - learning_rate * b_slope
		new_m = m - learning_rate * m_slope    
		b = new_b
		m = new_m
	    
	if(mylist[itr]=='data3.csv'):
		nextTemp = (m * 20 + b)
		print('Next Temperature value is {}'.format(nextTemp))
    
	elif(mylist[itr]=='data2.csv'):
		nextCO = (m * 20 + b)*0.0017
		print('Next Carbon Monoxide value is {}'.format(nextCO))
	   
	else:
		nextCH4 = (m * 20 + b)*0.00209
		print('Next Methane value is {}'.format(nextCH4))  
