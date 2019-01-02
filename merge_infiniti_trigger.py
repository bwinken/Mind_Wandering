import pandas as pd
import numpy as np
import os
import sys
from scipy.signal import find_peaks

def parse_data(filename):
	data = pd.read_csv(filename,skiprows=6)
	print("Data Shape : ",data.shape)
	#data = data[['E: VI4','F: VI3','G: VI2','H: VI1']].values
	
	return data
	
def find_stimulus(data):
	channel_E = data[['E: VI4']].values
	channel_F = data[['F: VI3']].values
	channel_G = data[['G: VI2']].values
	channel_H = data[['H: VI1']].values
	
	E,_ = find_peaks(channel_E[:,0],height=0.5)
	F,_ = find_peaks(channel_F[:,0],height=0.5)
	G,_ = find_peaks(channel_G[:,0],height=0.5)
	H,_ = find_peaks(channel_H[:,0],height=0.5)
	
	return E,F,G,H

	
	
def merge_trigger(data,trigger_file,filename):
	E,F,G,H = find_stimulus(data)
	
	trigger = pd.read_csv(trigger_file,sep="\t")
	total_trig = trigger.values.shape[0]
	
	E_pointer = 0
	F_pointer = 0
	G_pointer = 0
	H_pointer = 0
	err		= 2
	trig_num = 0
	trig_list = [None]*data.values.shape[0]
	for i in range(len(trig_list)):
		if E_pointer < len(E) and F_pointer < len(F) and G_pointer < len(G) and H_pointer < len(H) :
			if (abs(i-E[E_pointer])<=err) and (abs(i-F[F_pointer])<=err) and (abs(i-G[G_pointer])<=err) and (abs(i-H[H_pointer])<=err):
				trig_list[i] = "probe"
				trig_num += 1
				E_pointer += 1
				F_pointer += 1
				G_pointer += 1
				H_pointer += 1
				continue
		if E_pointer < len(E):
			if i == E[E_pointer]:
				trig_list[i] = "target"
				trig_num += 1
				E_pointer += 1
				continue
		if F_pointer < len(F):
			if i == F[F_pointer]:
				trig_list[i] = "target response"
				trig_num += 1
				F_pointer += 1
				continue
		if G_pointer < len(G):
			if i == G[G_pointer]:
				trig_list[i] = "normal"	
				trig_num += 1
				G_pointer += 1
				continue
		if H_pointer < len(H):		
			if i == H[H_pointer]:
				trig_list[i] = "response"
				trig_num += 1
				H_pointer += 1
				continue

	if(	trig_num != total_trig):
		print("trig num:",trig_num)
		print("Golden_trig_num:",total_trig)
		
	assert(trig_num == total_trig)
	
	trig = {"trigger":trig_list}
	trig_df = pd.DataFrame(trig)
	df = pd.concat([data,trig_df],axis=1)
	df.to_csv(filename)
	print("Merge to ",filename)
	
if __name__ == "__main__":
	data_path = sys.argv[1]
	path = data_path.split('/')
	user_name = path[-2]
	user_id = user_name.split('_')[0]
	
	infiniti_format = "txt"
	trigger_format = "csv"
	output_format = "csv"
	
	#pre
	infiniti_file 			= os.path.join(data_path,user_name+"_infiniti_prerest."+infiniti_format)
	trigger_file 			= os.path.join(data_path,user_name+"_eegtrigger_prerest."+trigger_format)
	infiniti_csv			= os.path.join(data_path,"user"+user_id+"_pre_infiniti."+output_format)
	
	print("Processing Infiniti's Pre")
	data = parse_data(infiniti_file)
	merge_trigger(data,trigger_file,infiniti_csv)
	
	#post
	infiniti_file 			= os.path.join(data_path,user_name+"_infiniti_postrest."+infiniti_format)
	trigger_file 			= os.path.join(data_path,user_name+"_eegtrigger_postrest."+trigger_format)
	infiniti_csv			= os.path.join(data_path,"user"+user_id+"_post_infiniti."+output_format)
	
	print("Processing Infiniti's Post")
	data = parse_data(infiniti_file)
	merge_trigger(data,trigger_file,infiniti_csv)
	
	#main
	infiniti_file 			= os.path.join(data_path,user_name+"_infiniti_main."+infiniti_format)
	trigger_file 			= os.path.join(data_path,user_name+"_eegtrigger_main."+trigger_format)
	infiniti_csv			= os.path.join(data_path,"user"+user_id+"_main_infiniti."+output_format)
	
	print("Processing Infiniti's Main")
	data = parse_data(infiniti_file)
	merge_trigger(data,trigger_file,infiniti_csv)