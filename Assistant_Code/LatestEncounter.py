import pandas as pd
from pandas import DataFrame
import numpy as np
import datetime as dt

PATH = '/home/vinodrao/Spring2017/MATH497/project/DataAnalysis/'

droppedIndex = [ ]

dfs = pd.read_pickle(PATH + 'all_encounter_data.pickle')
def TakeAverage(list1, list2):
	#BMI,BP,Glucose,A1C
	l = [ ]
	l.append(list1[0])
	l.append(list1[1])
	bmi = list1[2]
	bp = list1[3]
	glu = list1[4]
	a1c = list1[5]

	if(list2[0] > 1):
		bmi = float(list1[2]) / int(list2[0])
	if(list2[1] > 1):
		s = bp.split("/")
		if(len(s) == 2):
			bp = str(float(s[0])/list2[1]) + '/' + str(float(s[1])/list2[1])
		else:
			bp = str(float(bp/list2[1]))
	if(list2[2] > 1):
		g = glu.split("/")
		if(len(g) == 2):
			glu = str(float(g[0])/list2[2]) + '/' + str(float(g[1])/list2[2])
		else:
			glu = str(float(glu)/list2[2])
	if(list2[3] > 1):
			a1c = str(float(a1c)/list2[3])

	l.append(bmi)
	l.append(bp)
	l.append(glu)
	l.append(a1c)

	return l

def TokenizeAndAdd(str1,str2):
	addedStr = ""
	sS = str1.split("/")
	uU = str2.split("/")

	s = [ ]
	for i in (sS):
		tmp = i.strip()
		if(len(tmp) > 0):
			s.append(tmp)

	u = [ ]
	for i in (uU):
		tmp = i.strip()
		if(len(tmp) > 0):
			u.append(tmp)

	if(len(s) == 2 and len(u) == 2):
		v = int(s[0]) + int(u[0])
		w = int(s[1]) + int(u[1])
		addedStr = str(v) + '/' + str(w)
	elif(len(s) == 1 and len(u) == 1):
		v = int(s[0]) + int(u[0])
		addedStr = str(v)
	elif(len(s) == 2 and len(u) == 1):
		v = int(s[0]) + int(s[0])
		addedStr = str(v) + '/' + str(float(u[0]) * 2)
	else:
		v = int(u[0]) + int(u[0])
		addedStr = str(float(s[0]) * 2) + '/' + str(v)

	return addedStr

h = dict()
num = 0
for val in dfs.itertuples():
	num = val.Index
	_date = pd.to_datetime(val.Enc_Date).date()
	if(h.get(val.Person_Nbr)):
		value = h.get(val.Person_Nbr)
		if(value[0] < _date):
			value.pop(0)
			for i in (value):
				droppedIndex.append(i)
			h[val.Person_Nbr] = [_date, num] 
		elif(value[0] == _date):
			h[val.Person_Nbr].append(num)
	else:
		h[val.Person_Nbr] = [_date, num] 

for key,val in h.items():
	PPLocked = False
	SSLocked = False
	lastIndex = val[len(val)-1]
	val.pop(0)
 	
	primeParam = ['NaN'] * 6
	primeParamFreq = [0] * 4

	if(len(val) > 1):
		for ind in reversed(val):
		
			if(pd.isnull(dfs.ix[ind].Primary_Payer) == False and PPLocked == False):
				primeParam[0] = dfs.ix[ind].Primary_Payer
				PPLocked = True
			if(pd.isnull(dfs.ix[ind].Smoking_Status) == False and SSLocked == False):
				primeParam[1] = dfs.ix[ind].Smoking_Status
				SSLocked = True
			if(pd.isnull(dfs.ix[ind].BMI) == False):
				if(primeParamFreq[0] == 0):
					primeParam[2] = (dfs.ix[ind].BMI).strip()
					primeParamFreq[0] = 1
				else:
					primeParam[2] = float(primeParam[2]) + float((dfs.ix[ind].BMI).strip())
					primeParamFreq[0] = primeParamFreq[0] + 1
			if(pd.isnull(dfs.ix[ind].BP) == False):
				if(primeParamFreq[1] == 0):
					primeParam[3] = (dfs.ix[ind].BP).strip()
					primeParamFreq[1] = 1
				else:
					primeParam[3] = TokenizeAndAdd(primeParam[3] , (dfs.ix[ind].BP).strip())
					primeParamFreq[1] = primeParamFreq[1] + 1
			if(pd.isnull(dfs.ix[ind].Glucose) == False):
				if(primeParamFreq[2] == 0):
					primeParam[4] = str(dfs.ix[ind].Glucose).strip()
					primeParamFreq[2] = 1
				else:
					primeParam[4] = TokenizeAndAdd(primeParam[4] , str(dfs.ix[ind].Glucose).strip())
					primeParamFreq[2] = primeParamFreq[2] + 1
			if(pd.isnull(dfs.ix[ind].A1C) == False):
				if(primeParamFreq[3] == 0):
					primeParam[5] = str(dfs.ix[ind].A1C).strip()
					primeParamFreq[3] = 1
				else:
					primeParam[5] = float(primeParam[5])+ float(str(dfs.ix[ind].A1C).strip())
					primeParamFreq[3] = primeParamFreq[3] + 1
	
		primeParam = TakeAverage(primeParam,primeParamFreq)

		dfs.set_value(lastIndex, 'Primary_Payer', primeParam[0])
		dfs.set_value(lastIndex, 'Smoking_Status' , primeParam[1])
		dfs.set_value(lastIndex, 'BMI' ,primeParam[2])
		dfs.set_value(lastIndex, 'BP' , primeParam[3]) 
		dfs.set_value(lastIndex, 'Glucose' , primeParam[4])
		dfs.set_value(lastIndex, 'A1C' , primeParam[5])

		val.pop()
		for i in (val):
			droppedIndex.append(i)

dfs.drop(droppedIndex, inplace=True)
dfs.to_csv("LatestEncounter.csv", sep=',')
dfs.to_pickle("LatestEncounter.pickle")
