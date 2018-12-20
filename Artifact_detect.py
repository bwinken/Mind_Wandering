import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import biosppy.signals.eda as beda
from scipy.spatial import distance
from scipy import signal

#============Load GSR and Label correspond to user_id and data_no============
def load_data(user_id,data_no):
	ID = str(user_id)
	NO = str(data_no)
	
	if user_id <= 9:
		ID = str(0) + ID
	if data_no <= 9:
		NO = str(0) + NO		
		
	mat_filename = "Amigo_Dataset/Data_Original_P" + ID + "/data_" + str(data_no) + "/GSR.mat"
	label_filename = "Amigo_Dataset/Data_Original_P" + ID + "/data_" + str(data_no) + "/user_" + ID + "_data_" + NO + "_NoiseLabels_Binary.csv"
	mat = scipy.io.loadmat(mat_filename)
	label = pd.read_csv(label_filename)
	return mat['GSR'],label['BinaryLabels']

#===========Calculate Derivative==========
def derivative(GSR,Fs):
	return np.gradient(GSR.ravel())*Fs;

#==========Plot GSR with Label============
def plot_GSR_and_label(GSR,label,Fs):
	plt.plot(GSR)
	#print("LEN label:",len(label.ravel()))
	for i in range(len(label.ravel())):
		if label[i] == -1:
			plt.axvspan(i*Fs*5,(i+1)*Fs*5,color='red',alpha=0.5)
		elif label[i] == 0:
			plt.axvspan(i*Fs*5,(i+1)*Fs*5,color='green',alpha=0.5)
	
			
#==========Plot Deri with Label============	
def plot_deri_and_label(deri,label,Fs):
	plt.plot(deri)
	for i in range(len(label.ravel())):
		if label[i] == -1:
			plt.axvspan(i*Fs*5,(i+1)*Fs*5,color='red',alpha=0.5)	
			
	y_min,y_max = y_precentage(deri,10)
	plt.axvspan(xmin=0,xmax=len(label.ravel())*Fs*5,ymin=y_min,ymax=y_max,color='blue',alpha=0.5)	

	#associted with plot deri with label
def y_precentage(deri,th):
	max = np.max(deri)
	min = np.min(deri)
	
	if(max <= th): y_max = 1
	else: y_max = (th-min)/(max-min)
	
	if(min >= -1*th): y_min = 0
	else: y_min = (-1*th-min)/(max-min)
	
	return y_min,y_max

#======Calculate artifacted epoch========
	#====return the percentage
def artifact_percentage_EDAXplorer(user_id,data_no):
	total_epoch = 0
	artifact_epoch = 0
	
	data,label=load_data(user_id,data_no)
	total_epoch = len(label)
	for k in range(len(label)):
		if label[k] == -1 or label[k] == 0: artifact_epoch += 1	
	return artifact_epoch/total_epoch

def artifact_percentage_Simple(user_id,data_no):
	total_epoch = 0
	artifact_epoch = 0
	
	data,q=load_data(user_id,data_no)
	ts, filtered, onsets, peaks, amplitudes = beda.eda(data.ravel(),128,False)
	label = first_layer_artifact(filtered,10,128)
	total_epoch = len(label)
	for k in range(len(label)):
		if label[k] == -1 or label[k] == 0: artifact_epoch += 1		
	return artifact_epoch/total_epoch
	
def artifact_percentage(user_id,data_no):
	total_epoch = 0
	artifact_epoch = 0
	
	data,a =load_data(user_id,data_no)
	label = detect_artifact(data,10,128)
	total_epoch = len(label)
	for k in range(len(label)):
		if label[k] == -1 or label[k] == 0: artifact_epoch += 1		
	return artifact_epoch/total_epoch

#=====save the fig that show the relation between artifact epoch and derivative=====
def save_fig(user_id,data_no):
	ID = str(user_id)
	NO = str(data_no)
	
	if user_id <= 9:
		ID = str(0) + ID
	
	if data_no <= 9:
		NO = str(0) + NO
	content,label = load_data(user_id,data_no)
	deri = derivative(content,128)
		
	plt.subplot(211)
	plt.title("USER_"+ID+"_DATA_"+NO+"_GSR signal")
	plot_GSR_and_label(content,label,128)
	plt.subplot(212)
	plot_deri_and_label(deri,label,128)

	plt.savefig("Amigo_Dataset/Figures/" + "user_" + ID + "/user_" + ID + "_data_" + NO + ".png")
	plt.close()

#=======Detect artifact of GSR signal======	
def detect_artifact(GSR,th,Fs):
	
	ts, filtered, onsets, peaks, amplitudes = beda.eda(GSR.ravel(),Fs,False)
	first_detect = first_layer_artifact(GSR,th,Fs)
	detect = second_layer_artifact_detect(GSR,filtered,first_detect,Fs,5)
	
	return detect
	
def first_layer_artifact(GSR,th,Fs):
	
	deri = derivative(GSR,Fs)
	epoch_no = int(len(GSR)/(5*Fs))
	detect = np.ones((epoch_no,1))
	for i in range(epoch_no):
		for j in range(5*Fs):
			if( GSR[i*5*Fs+j] < 0.05 or GSR[i*5*Fs+j] > 60):
				detect[i] = -1 #irremovable
			elif((deri[i*5*Fs+j] <= -1*th or deri[i*5*Fs+j] >= th) and detect[i] != -1):
				detect[i] = 0 #artifact
	
	return detect
def second_layer_artifact_detect(GSR,filtered,first_layer_label,Fs,th):
	label = np.ones((len(first_layer_label),1))
	for i in range(len(first_layer_label)):
		if(first_layer_label[i] == 1):	continue 
		if(first_layer_label[i] == -1): 
			label[i] = -1
			continue
		s = i*5*Fs
		e = (i+1)*5*Fs
		if distance.euclidean(GSR[s:e],filtered[s:e]) >= th :
			label[i] = -1
		else: label[i] = 1
	return label

def fig_proposed(GSR,sampling_rate):

	ts, filtered, onsets, peaks, amplitudes = beda.eda(GSR.ravel(),sampling_rate,False)
	SR = filtered
	
	predict = detect_artifact(SR,10,sampling_rate)	
	predict_1 = detect_artifact(GSR,10,sampling_rate)	
	predict_2 = second_layer_artifact_detect(GSR,SR,predict_1,sampling_rate,5)
	plot_GSR_and_label(GSR,predict_1,sampling_rate)

	plt.savefig("CHEN DATA")
	plt.close()
	
#===Figure of comparison between EDA Xplorer and Our Criteria===	
def compare_plt(user_id,data_no,th,Fs):
	ID = str(user_id)
	NO = str(data_no)
	
	if user_id <= 9:
		ID = str(0) + ID
	
	if data_no <= 9:
		NO = str(0) + NO
	GSR,label = load_data(user_id,data_no)
	
	if Fs < 128:
		GSR = downsample(GSR,int(128/Fs))
		
	deri = derivative(GSR,Fs)
	
	detect = detect_artifact(GSR,th,Fs)
	
	plt.subplot(211)
	plt.title("EDA Xplorer")
	plot_GSR_and_label(GSR,label,Fs)
	plt.subplot(212)
	plt.title("Our Criteria")
	plot_GSR_and_label(GSR,detect,Fs)
	
	plt.show()

def SMC(total_user,total_data,th,Fs):
	TP 	= 0
	FP 	= 0
	TN 	= 0
	FN 	= 0
	for i in range(total_user):
		for j in range(total_data):
			GSR,label = load_data(i+1,j+1)
			if Fs < 128:#need to downsample
				GSR = downsample(GSR,int(128/Fs))
			predict = detect_artifact(GSR,th,Fs)
			for k in range(len(label)-2):
				if label[k+1] == 1 and predict[k+1] == 1:
					TN += 1
				elif label[k+1] == -1 and predict[k+1] == -1:
					TP += 1
				elif label[k+1] == -1 and predict[k+1] == 1:
					FN += 1
				elif label[k+1] == 1 and predict[k+1] == -1:
					FP += 1
	print("TP is:",TP)
	print("FN is:",FN)
	print("TN is:",TN)
	print("FP is:",FP)
	SMC = (TP+TN)/(TP+FN+TN+FP)
	sensitivity = TP/(TP+FN)
	specificity = TN/(TN+FP)
	return SMC,sensitivity,specificity

def downsample(GSR,ratio):
	return signal.resample(GSR,int(len(GSR)/ratio))

