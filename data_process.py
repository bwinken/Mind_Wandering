import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import find_peaks


def parse_data(filename):
	data = pd.read_csv(filename,skiprows=6)
	print("Data Shape : ",data.shape)
	print(data)
	#time = data[['Time']].values
	data = data[['E: VI4','F: VI3','G: VI2','H: VI1']].values
	
	return data#,time

def parse_data_eprime(filename):
	data = pd.read_csv(filename)
	data = data[['Trialtime']].values
	return data

def trigger_interval_eprime(array):
	dump = str(array[0,0]).split()
	p_time = dump[1]
	
	interval = np.zeros((array.shape[0]-1,1))
	for i in range(1,len(array)):
		dump = str(array[i,0]).split()
		c_time = dump[1]
		interval[i-1] = time_dif(p_time,c_time)
		p_time = c_time
	return interval
		
def time_dif(pre_time,time):
	cur    = str(time).split(':')
	c_hour = float(cur[0])
	c_min  = float(cur[1])
	c_sec  = float(cur[2])
	c_m_sec= float(cur[3])
	
	pre    = str(pre_time).split(':')
	p_hour = float(pre[0])
	p_min  = float(pre[1])
	p_sec  = float(pre[2])
	p_m_sec= float(pre[3]) 
	
	dif = 3600*(c_hour-p_hour)+60*(c_min-p_min)+(c_sec-p_sec)+0.001*(c_m_sec-p_m_sec)
	
	return dif
	
def find_stimulus(array,upper,lower):
	if upper >= 0:
		indices,_ = find_peaks(array,height=(lower,upper))
	elif upper < 0:
		indices,_ = find_peaks(array,height=(-1*upper,-1*lower))
	print("INDICES SHAPE :",len(indices))

	return indices
	
def trigger_interval(time_array,indices):
	array = np.zeros((len(indices)-1,1))
	start = float(time_array[indices[0]])
	for i in range(1,len(indices)):
		array[i-1] = float(time_array[indices[i]])-start
		start = float(time_array[indices[i]])
	return array

def plot_EFGH(data,start,end):
	plt.subplot(4,1,1)
	plt.title("E : VI4")
	plt.plot(data[start:end,0])
	plt.subplot(4,1,2)
	plt.title("F : VI3")
	plt.plot(data[start:end,1])
	plt.subplot(4,1,3)
	plt.title("G : VI2")
	plt.plot(data[start:end,2])
	plt.subplot(4,1,4)
	plt.title("H : VI1")
	plt.plot(data[start:end,3])
	plt.show()

def plot_compare_interval(data,time_eprime):
	indices = find_stimulus(-1*data[1::,1],-0.2,-0.4)
	interval_array = trigger_interval(time[1::],indices)
	print("INFINITY : ",np.sum(interval_array))
	
	interval_eprime = trigger_interval_eprime(time_eprime)
	print("EPRIME :",np.sum(interval_eprime))
	
	#plot the data with peak
	dd = data[1::,1]
	plt.plot(dd)
	plt.plot(indices,dd[indices],"x")
	plt.show()
	
	#plot the time interval
	plt.subplot(2,1,1)
	plt.title("INFINITI")
	plt.plot(interval_array)
	plt.subplot(2,1,2)
	plt.title("EPRIME")
	plt.plot(interval_eprime,'r')
	plt.show()
	
train_csv = sys.argv[1]
eprime_csv = sys.argv[2]

data= parse_data(train_csv)
#time_eprime = parse_data_eprime(eprime_csv)

start = 350000
end   = 450000
#print("RMSE:",np.sqrt(np.mean((interval_eprime-interval_array)**2)))


plot_EFGH(data,start,end)
#plot_compare_interval(data,time_eprime)




plt.show()