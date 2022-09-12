import csv
import sys
import os
import copy
import threading
import time
import timeit
import subprocess
import fnmatch
import re

#Column ID for Original File 
TASK_ID = 0
WCET = 1
PERIOD = 2
JITTER = 3
OFFSET = 4

#Column ID for New File
TID = 0
JID = 1
ARR_MIN = 2
ARR_MAX = 3
COST_MIN = 4
COST_MAX = 5
MAX_FIN = 6
PRIORITY = 7

#Global Variable
hyper_period = 0
awindow = 0
tid = 0
jid = 0
arr_min = 0
arr_max = 0
cost_min = 0
cost_max = 0
deadline = 0
job_period = 0
priority = 0

def sortRmin(val): 
    return val[2]

def sort_jobs_wrt_Rmin(jobs):
     jobs.sort(key = sortRmin)

#Find the lcm of two numbers
def find_lcm(num1,num2):
	if(num1 > num2):
		num = num1
		den = num2
	else:
		num = num2
		den = num1
	rem = num % den
	while(rem != 0):
		num = den
		den = rem
		rem = num % den
	gcd = den
	lcm = int(int(num1 * num2)/int(gcd))
	return lcm

#Find the hyperperiod of a list of periods
def find_hyperperiod(l):
	num1 = l[0]
	num2 = l[1]
	lcm = find_lcm(num1,num2)

	for i in range(2,len(l)):
		lcm = find_lcm(lcm,l[i])

	return lcm

def create_jobs(dest_csv,taskid,cst_min,cst_max,per,jit,ofs):
	global priority
	jid = 0
	with open(dest_csv, mode='ab') as des_file:
		# des_writer = csv.writer(des_file, delimiter =',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv.register_dialect('yimi_up', delimiter =',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		des_writer = csv.writer(des_file, dialect='yimi_up')

		while True:
			ert = (int((float(per))*jid)+int(ofs))
			lrt = (int((float(per))*jid)+int(jit+ofs)) 
			max_fin = (int((float(per))*(jid+1))+int(ofs))
			des_writer.writerow([int(taskid),jid,ert,lrt,int(cst_min),int(cst_max),max_fin,int(priority)])
			jid += 1
			priority +=1
			if(max_fin > awindow):
				break

if __name__ == '__main__':

		ustr = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
		tstr = [20]

		for u in ustr:
			for t in tstr:

				source = "tas_test1/tasksets/U"+str(u)+"/T"+str(t)+"/"
				des = "tas_test1/jobsets/U"+str(u)+"/T"+str(t)+"/"

				dirs = os.listdir(source)

				try:
					os.makedirs(des)
				except OSError:
					print("Creation of path failed")
				else:
					print("Created path")

				for file in dirs:
					if fnmatch.fnmatch(file, '*.csv') == True:
						hyper_period = 0
						period = []
						release = []
						offset = []
						priority = 0
						list_tasks = []
					
						source_csv = source + file
						des_csv = des + file
						print(source_csv)

						with open(source_csv) as csv_file:
							csv_reader = csv.reader(csv_file,delimiter=',')
							line_count = 0
							for row in csv_reader:
								if line_count==0:
									line_count+=1
								else:
									period.append(int(float(row[PERIOD])))
									offset.append(int(row[OFFSET]))
									release.append(int(row[JITTER]))
						if len(period) == 0:
							continue
						hyper_period = find_hyperperiod(period)
						# if there are no offsets
						awindow = hyper_period
						# if there are offsets
						# awindow = 2*hyperperiod

						with open(des_csv, mode='wb') as des_file:
							csv.register_dialect('yimi', delimiter =',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
							des_writer = csv.writer(des_file, dialect='yimi')

							# des_writer = csv.writer(des_file, delimiter =',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							des_writer.writerow(["TASK ID","JOB ID","ARRIVAL MIN","ARRIVAL MAX","COST MIN","COST MAX","DEADLINE","PRIORITY"])

						with open(source_csv) as csv_file:
							csv_reader = csv.reader(csv_file,delimiter=',')
							line_count = 0
							for row in csv_reader:
								if line_count == 0:
									line_count +=1
								else:
									task = []
									for item in row:
										task.append(int(item))
									list_tasks.append(task)
							sort_jobs_wrt_Rmin(list_tasks)
							for row in list_tasks:
								tid = row[TASK_ID]
								cost_min = 0
								cost_max = row[WCET]
								job_period = row[PERIOD]
								jit = row[JITTER]
								ofs = row[OFFSET]
								create_jobs(des_csv,tid,cost_min,cost_max,job_period,jit,ofs)
