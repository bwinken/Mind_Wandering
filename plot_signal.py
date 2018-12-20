import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from Artifact_detect import fig_proposed

def parse_data(filename):
	data = pd.read_csv(filename)
	print("Data Shape : ",data.shape)

	data = data[['Temp-Pro/Flex - 1A','SC-Pro/Flex - 1B','C: BVP','D: Resp']].values
	
	return data
	
data_csv = sys.argv[1]

data = parse_data(data_csv)

fig_proposed(data[1::,1],256)

#plt.subplot(4,1,1)
#plt.title("TEMP")
#plt.plot(data[1::,0])
#plt.subplot(4,1,2)
#plt.title("GSR")
#plt.plot(data[1::,1])
#plt.subplot(4,1,3)
#plt.title("BVP")
#plt.plot(data[1::,2])
#plt.subplot(4,1,4)
#plt.title("RESP")
#plt.plot(data[1::,3])
#plt.show()