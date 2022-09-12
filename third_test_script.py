import csv
import sys
import os
import copy
import subprocess
import fnmatch
import re
from os.path import exists

#Path to original code
og_path = "CE/np-schedulability-analysis/build/nptest"

# Path for publsihing results
result_path = "tas_test1/results"

if __name__ == '__main__':


	util = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	tstr = [20]


	for u in util:
		for t in tstr:

			des = "tas_test1/jobsets/U"+str(u)+"/T"+ str(t)+"/"
					
			result_csv = "third run result_U"+str(u)+"_T"+ str(t) +".csv"
			
			result_final = result_path+"/"+result_csv

			with open(result_final, 'w') as csvfile:
				resultwriter = csv.writer(csvfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
				resultwriter.writerow(['Filename','Schedulability','Num_jobs', 'Num_states', 'Num_edges', 'Max_width', 'Cpu_time', 'Mem_used', 'Timeout' ]) 

			dirs = os.listdir(des)

			for file in dirs:
				if fnmatch.fnmatch(file, '*.rj.pop.csv') == True:	

					des_csv = des + file
					tarName = file.replace('.pop', '')

					des_rj_csv = des + tarName

					tas_analysis = [og_path, des_rj_csv, '-b', des_csv]
					tas_analysis_run = subprocess.Popen(tas_analysis, stdout = subprocess.PIPE)
					tas_analysis_out = tas_analysis_run.stdout.read()
					tas_analysis_out_str = str(tas_analysis_out)
					tas_analysis_out_str_split = tas_analysis_out_str.split(', ')[1:-1]


					with open(result_final, 'a') as csvfile:
						# resultwriter = csv.writer(csvfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
						csv.register_dialect('yimi_up', delimiter =',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
						des_writer = csv.writer(csvfile, dialect='yimi_up')
						# resultwriter.writerow([file, int(tas_analysis_out_str_split[1].replace(",","")), float(tas_analysis_out_str_split[2].replace(",","")), float(tas_analysis_out_str_split[3].replace(",","")), float(tas_analysis_out_str_split[4].replace(",","")), float(tas_analysis_out_str_split[5].replace(",","")), float(tas_analysis_out_str_split[6].replace(",","")), float(tas_analysis_out_str_split[7].replace(",","")), int(tas_analysis_out_str_split[8].replace(",","")), int(tas_analysis_out_str_split[9].replace(",","")) ]) 
						try:
							des_writer.writerow([file, int(tas_analysis_out_str_split[0]), int(tas_analysis_out_str_split[1]), int(tas_analysis_out_str_split[2]), int(tas_analysis_out_str_split[3]), int(tas_analysis_out_str_split[4]), float(tas_analysis_out_str_split[5]), float(tas_analysis_out_str_split[6]), int(tas_analysis_out_str_split[7]) ]) 
						except:
							des_writer.writerow([int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(0) ]) 

						


