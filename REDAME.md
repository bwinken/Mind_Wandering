Description of each file:
1.)plot_signal.py
	-plot infiniti data
	-with automatic artifact detection
	
2.)data_process.py
	-experiment use

3.)merge_EEG_trigger.py
	-detect those event from trigger and merge to EEG file
	how to execute
		python merge_EEG_trigger.py $1 $2 $3
			-$1:EEG data
			-$2:trigger data
			-$3:Merged EEG file
		
4.)merge_tobii_trigger.py
	-detect those event from trigger and merge to tobii file
	how to execute
		python merge_tobii_trigger.py
			-$1:tobii data
			-$2:trigger data
			-$3:Merged tobii file