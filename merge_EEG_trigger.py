import pandas as pd
import numpy as np
import sys
import os 

def parse_data(EEG_txt):
	COL = ['FP1','FP2','F7','F3','FZ','F4','F8','FT7','FC3','FCZ','FC4','FT8','T7','C3','CZ','C4','T8','M2','TP7','CP3','CPZ','CP4','TP8','P7','P3','PZ','P4','P8','O1','OZ','O2','HEO','VEO']	
	EEG = pd.read_csv(EEG_txt,sep='\t')
	EEG = EEG[COL].values
	print(EEG.shape)
	return EEG

def merge_trigger(EEG,trigger_csv,EEG_csv):
	normal = 36
	response = 68
	target	= 12
	target_res = 20
	trial = 255
	COL = ['FP1','FP2','F7','F3','FZ','F4','F8','FT7','FC3','FCZ','FC4','FT8','T7','C3','CZ','C4','T8','M2','TP7','CP3','CPZ','CP4','TP8','P7','P3','PZ','P4','P8','O1','OZ','O2','HEO','VEO','trigger']
	
	trigger = pd.read_csv(trigger_csv,sep="\t")
	trig_type = trigger[['type']].values
	trig_latency = trigger[['latency']].values

	#initiate an empty list
	trig_list = [None]*EEG.shape[0]
		
	for i in range(trig_type.shape[0]):
		if trig_type[i,0] == normal:
			trig_list[int(trig_latency[i,0])] = "normal"
		elif trig_type[i,0] == response:
			trig_list[int(trig_latency[i,0])] = "response"
		elif trig_type[i,0] == target:
			trig_list[int(trig_latency[i,0])] = "target"
		elif trig_type[i,0] == target_res:
			trig_list[int(trig_latency[i,0])] = "target_response"
		elif trig_type[i,0] == trial:
			trig_list[int(trig_latency[i,0])] = "probe"
		else:
			print("ERROR OCCURS")
			
	trig = np.asarray(trig_list)
	trig = np.reshape(trig,(trig.shape[0],1))
	
	new_EEG = np.hstack((EEG,trig))
	df = pd.DataFrame(new_EEG,columns=COL)
	df.to_csv(EEG_csv)
	print("Merge to ",EEG_csv)
	
if __name__ == "__main__":
	data_path = sys.argv[1]
	path = data_path.split('/')
	user_name = path[-2]
	user_id = user_name.split('_')[0]
	
	EEG_format = "txt"
	trigger_format = "csv"
	output_format = "csv"
	
	#pre
	EEG_txt 				= os.path.join(data_path,user_name+"_eegoutput_prerest."+EEG_format)
	trigger_csv 			= os.path.join(data_path,user_name+"_eegtrigger_prerest."+trigger_format)
	EEG_csv				 	= os.path.join(data_path,"user"+user_id+"_pre_EEG."+output_format)
	
	print("Processing EEG's Pre")
	EEG = parse_data(EEG_txt)
	merge_trigger(EEG,trigger_csv,EEG_csv)
	
	
	#post
	EEG_txt 				= os.path.join(data_path,user_name+"_eegoutput_postrest."+EEG_format)
	trigger_csv 			= os.path.join(data_path,user_name+"_eegtrigger_postrest."+trigger_format)
	EEG_csv		 			= os.path.join(data_path,"user"+user_id+"_post_EEG."+output_format)
	
	print("Processing EEG's Post")
	EEG = parse_data(EEG_txt)
	merge_trigger(EEG,trigger_csv,EEG_csv)
	
	#main
	EEG_txt 				= os.path.join(data_path,user_name+"_eegoutput_main."+EEG_format)
	trigger_csv 			= os.path.join(data_path,user_name+"_eegtrigger_main."+trigger_format)
	EEG_csv					= os.path.join(data_path,"user"+user_id+"_main_EEG."+output_format)
	
	print("Processing EEG's Main")
	EEG = parse_data(EEG_txt)
	merge_trigger(EEG,trigger_csv,EEG_csv)
	