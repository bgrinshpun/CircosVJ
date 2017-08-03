#!/usr/bin/env python

import sys
import numpy as np

'''
Commandline inputs:

1. Input file containing cassette information and counts. First row is the header.
2. Vcol: column index for V cassettes
3. Jcol: column index for J cassettes
4. ctscol: column index for counts
5. Output file name

Output:

Table of VJ usage, V cassette along columns, J cassette along rows

'''


inputfile=sys.argv[1]
Vcol=int(sys.argv[2])
Jcol=int(sys.argv[3])
ctscol=int(sys.argv[4])
colnames=int(sys.argv[5])

if len(sys.argv)==7:
	output=sys.argv[6]
else:
	output="output.txt"

## Read the input file
f=open(inputfile,'r')

if colnames:
	h=f.readline() 
data=f.readlines()
data=[i.strip().split("\t") for i in data]
data=zip(*data)

## Select cassettes
V=data[Vcol]
V=[i.translate(None, 'TCRB') for i in V]
V=[i.translate(None, 'TCRA') for i in V]

J=data[Jcol]
J=[i.translate(None, 'TCRB') for i in J]
J=[i.translate(None, 'TCRA') for i in J]


cts=map(int,data[ctscol])
uV=list(set(V)) # unique V
uJ=list(set(J)) # unique V

## Generate empty matrix
M=np.zeros((len(uJ),len(uV)),dtype=int) # Create empty matrix
Vd=dict([j,i] for i,j in enumerate(uV)) # index cassettes
Jd=dict([j,i] for i,j in enumerate(uJ))

## Populate matrix with counts using cassette indices
for i in range(len(V)):
		M[Jd[J[i]]][Vd[V[i]]]=M[Jd[J[i]]][Vd[V[i]]]+cts[i]

## Write table to file
out=open(output,'w')
out.write("\t"+"\t".join(uV)+"\n")
for i in range(len(uJ)):
	Jseg=uJ[i]
	m=map(str,M[i,])
	out.write(Jseg+"\t"+"\t".join(m)+"\n")

out.close()
