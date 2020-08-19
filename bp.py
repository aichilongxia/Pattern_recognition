#function: 3 calssfication by zengliang shi bp
import numpy as np
import random
import math
import sys
import os
a = 1
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 335c37d... commit A
=======
>>>>>>> 1f44087... modified

=======
b = 1 
c = 1
<<<<<<< HEAD
>>>>>>> c5399e9... commit C
=======
d = 1
>>>>>>> 958c6b6... commit D
<<<<<<< HEAD
<<<<<<< HEAD

e = 1
f = 1
=======
>>>>>>> 1f44087... modified
=======

e = 1
<<<<<<< HEAD
>>>>>>> 3491053... commit E
=======
f = 1
>>>>>>> 9ef3976... commit F
def logsig(x):
	return  1/(1 + np.exp(-x))

def train(SamSum,InDim,HidDim,OutDim,x):
	ITERS = 2000
	N_1 = 0.1 
	N_2 = 0.1
	Error = 0.002 #erroe for single sample
	class_typenum = []
	class_type = []
	for item in x:
		if item[0] > -1 and item[0] < 1 and item[1] < item[0]+1:
			class_type = [1,0,0]
		elif math.sqrt((item[0] - 1)**2+(item[1] + 1)**2) < 1.0:
			class_type = [0,1,0]
		else:
			class_type = [0,0,1]
		class_typenum.append(class_type)
	#back error 1*11 and 1*3
	backerror1 = [0 for row in range(HidDim+1)]
	backerror2 = [0 for row in range(OutDim)]
	# w  and b 
	w1 = [[random.uniform(-0.1,0.1) for m in range(InDim)] for i in range(HidDim)]
	offset1 = [random.uniform(-0.1,0.1) for m in range(HidDim)]
	w2 = [[random.uniform(-0.1,0.1) for m in range(HidDim)] for i in range(OutDim)]
	offset2 = [random.uniform(-0.1,0.1) for m in range(OutDim)]
	#w 10*2->10*3,3*10->3*11
	for i in range(HidDim):
		w1[i].append(offset1[i])
	for j in range(OutDim):
		w2[j].append(offset2[j])
	w1_mat = np.array(w1)
	w2_mat = np.array(w2)
	x1_offset = [-1 for _ in range(SamSum)]#200*1
	#x:200*2->200*3
	for m in range(SamSum):
		x[m].append(-1)
	x_mat = np.array(x)
	#iter 
	for iter in range(ITERS):
		for num in range(SamSum):
			while(True):
				x1=logsig(np.dot(w1_mat,x_mat.T).T)#output  of hidden
				#hidden 200*10->200*11
				x1_mat=np.column_stack((x1,x1_offset))
				#y  200*3
				y=logsig(np.dot(w2_mat,x1_mat.T).T)
				ER = 0.5*sum([(p - q)**2 for p,q in zip(class_typenum[num],y[num])]) 
				if ER < Error:
					break
				# backerror2 is 1*3, backerror1 is 1*11 
				for m in range(OutDim):
					backerror2[m] = (class_typenum[num][m] - y[num][m])*y[num][m]*(1 - y[num][m])
				for k in range(HidDim+1):
					backerror1[k] = sum([backerror2[l]*w2_mat[l][k]*x1_mat[num][k]*(1-x1_mat[num][k]) for l in range(OutDim)])
				# it is ok  that one of l,k and k,j can be first
				for l in range(OutDim):
					for k in range(HidDim+1):
						w2_mat[l][k] += N_1*backerror2[l]*x1_mat[num][k]
				for k in range(HidDim):
					for j in range(InDim+1):
						w1_mat[k][j] += N_2*backerror1[k]*x_mat[num][j]
		print "This is the %d th trainning Network, Error is %f !" %(iter,ER)
	print "The BP Network train end!"
	return w1_mat,w2_mat

def test(w1_mat,w2_mat,x,SamSum):
	accu = []
	class_typenum = []
	class_type = []
	for item in x:
		if item[0] > -1 and item[0] < 1 and item[1] < item[0]+1:
			class_type = [1,0,0]
		elif math.sqrt((item[0] - 1)**2+(item[1] + 1)**2) < 1.0:
			class_type = [0,1,0]
		else:
			class_type = [0,0,1]
		class_typenum.append(class_type)
	#w1 and w2 dim has been modified
	x1_offset = [-1 for _ in range(SamSum)]#200*1
	#x:200*2->200*3
	for m in range(SamSum):
		x[m].append(-1)
	x_mat = np.array(x)
	for  num in range(SamSum):
		x1=logsig(np.dot(w1_mat,x_mat.T).T)#output  of hidden
		#hidden 200*10->200*11
		x1_mat=np.column_stack((x1,x1_offset))
		#y  200*3
		y=logsig(np.dot(w2_mat,x1_mat.T).T)
		ER = 0.5*sum([(p - q)**2 for p,q in zip(class_typenum[num],y[num])]) 
		if ER<0.002:
			accu.append(1.0)
	return sum(accu) / SamSum


if __name__ == '__main__':
	SamSum = 200
	InDim = 2
	OutDim = 3
	HidDim = 10;
	result = []
	t=0.0
	x=[[random.uniform(-1,1) for m in range(InDim)] for i in range(SamSum)]
	w1,w2 = train(SamSum,InDim,HidDim,OutDim,x)
	for _ in range(100):
		x2=[[random.uniform(-1,1) for m in range(InDim)] for i in range(SamSum)]
		accu = test(w1,w2,x2,SamSum)
		result.append(accu)
	for i in range(len(result)):
		print result[i] #," " if  i%10!=0 else '\n'
		t += result[i]
	print "average =" ,t/len(result)
	print "w1 = ", w1
	print "w2 = ", w2
