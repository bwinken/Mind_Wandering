import numpy as np
import pandas as pd
import sys
import os


def parse_data(tobii_file):
	data = pd.read_csv(tobii_file,sep="\t",encoding='utf-16')
	timestamp 	= data[['Recording timestamp']].values
	event		= data[['Event']].values
	
	return data,timestamp,event

#check the event num
#return True when equal
def first_layer_check(event,trigger_num):
	event_num = (event == "SyncPortInHigh").sum()
	print("Trigger Num is:",event_num)
	print("Goleden Trigger Num is:",trigger_num)
	return (event_num==trigger_num)
	
	
#check the timing alignment
#the time difference between each trigger no more than XXX
def second_layer_check(event,event_time,trigger_latency):
	index,a = np.where(event=="SyncPortInHigh")
	print(index)
	trigger_start_time = trigger_latency[0,0]
	event_start_time = event_time[index[0]]

	#assert(len(index) == trigger_latency.shape[0])
	
	for i in range(len(index)):
		trig_latency = trigger_latency[i,0]-trigger_start_time
		event_latency = event_time[index[i],0]-event_start_time
		if abs(trig_latency-event_latency)>50:#difference bigger than 50 ms
			print(" time is not aligning, please check data")
			return False
			
	return True
	
	
def merge_trigger(tobii,timestamp,event,trigger_csv,filename):
	normal = 36
	response = 68
	target	= 12
	target_res = 20
	trial = 255
	
	trigger = pd.read_csv(trigger_csv,sep="\t")
	trig_type = trigger[['type']].values
	trig_latency = trigger[['latency']].values
	
	trigger_num_equality = first_layer_check(event,trig_latency.shape[0])
	if trigger_num_equality:
		print("First layer check accomplished")
	else:
		print("Event num and trigger num is not equal")
		
	timing_alignment = second_layer_check(event,timestamp,trig_latency)
	if timing_alignment:
		print("Second layer check accomplished")
	else:
		print("Time is not aligned, Please check data ! ")
	
	index,a = np.where(event=="SyncPortInHigh")
	trig_list = [None]*event.shape[0]
	
	for i in range(len(index)):
		if trig_type[i,0] == normal:
			trig_list[index[i]] = "normal"
		elif trig_type[i,0] == response:
			trig_list[index[i]] = "response"
		elif trig_type[i,0] == target:
			trig_list[index[i]] = "target"
		elif trig_type[i,0] == target_res:
			trig_list[index[i]] = "target_response"
		elif trig_type[i,0] == trial:
			trig_list[index[i]] = "probe"
		else:
			print("ERROR OCCURS")
	
	trig = {"trigger":trig_list}
	trig_df = pd.DataFrame(trig)
	df = pd.concat([tobii,trig_df],axis=1)
	df.to_csv(filename)
	
	print("Merge to ",filename)
if __name__ == "__main__":
	data_path = sys.argv[1]
	path = data_path.split('/')
	user_name = path[-2]
	user_id = user_name.split('_')[0]
	
	tobii_format = "tsv"
	trigger_format = "csv"
	output_format = "csv"
	
	#pre
	tobii_file 				= os.path.join(data_path,user_name+"_tobii_prerest."+tobii_format)
	trigger_file 			= os.path.join(data_path,user_name+"_eegtrigger_prerest."+trigger_format)
	processed_tobii_file 	= os.path.join(data_path,"user"+user_id+"_pre_tobii."+output_format)
	
	print("Processing Tobii's Pre")
	tobii,timestamp,event = parse_data(tobii_file)
	merge_trigger(tobii,timestamp,event,trigger_file,processed_tobii_file)

	
	#post
	tobii_file 				= os.path.join(data_path,user_name+"_tobii_postrest."+tobii_format)
	trigger_file 			= os.path.join(data_path,user_name+"_eegtrigger_postrest."+trigger_format)
	processed_tobii_file 	= os.path.join(data_path,"user"+user_id+"_post_tobii."+output_format)
	
	print("Processing Tobii's Post")
	tobii,timestamp,event = parse_data(tobii_file)
	merge_trigger(tobii,timestamp,event,trigger_file,processed_tobii_file)
	
	#main
	tobii_file 				= os.path.join(data_path,user_name+"_tobii_main."+tobii_format)
	trigger_file 			= os.path.join(data_path,user_name+"_eegtrigger_main."+trigger_format)
	processed_tobii_file 	= os.path.join(data_path,"user"+user_id+"_main_tobii."+output_format)
	
	print("Processing Tobii's Main")
	tobii,timestamp,event = parse_data(tobii_file)
	merge_trigger(tobii,timestamp,event,trigger_file,processed_tobii_file)
	
