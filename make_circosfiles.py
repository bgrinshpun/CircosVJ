#!/usr/bin/env python

import sys
import numpy as np
import re


# get cassettes and counts matrix
data=open(sys.argv[1],'r')
Vcas=data.readline()[1:].strip().split("\t")
data=data.readlines()
data=[i.strip().split("\t") for i in data]
data=zip(*data)
Jcas=data[0]
data=zip(*data[1:])
data=np.array(data).astype(int)

# Assign a band label index to the V cassettes
Vd=dict([[j,i] for i,j in enumerate(Vcas)])
Jd=dict([[j,i] for i,j in enumerate(Jcas)])

# Sorted counts for V and for J
Vsum=zip(Vcas,np.sum(data,axis=0))
Jsum=zip(Jcas,np.sum(data,axis=1))

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

Vsum=sorted(Vsum,key=lambda x: natural_key(x[0]))
Jsum=sorted(Jsum,key=lambda x: natural_key(x[0]))


# define the circos chromosomes
kfile=sys.argv[2]
fout=open(kfile,'w')

prefix="chr - "
colordict={}

for line in Vsum:
	label=line[0]; end=line[1]
	color=label.lower()
	band="v"+str(Vd[label])
	colordict[band]=color
	fout.write(prefix+"\t"+band+"\t"+label[3:]+"\t0\t"+str(end)+"\t"+label+"\n")

for line in Jsum:
        label=line[0]; end=line[1]
	color=label.lower()
        band="j"+str(Jd[label])
        fout.write(prefix+"\t"+band+"\t"+label[3:]+"\t0\t"+str(end)+"\t"+label+"\n")

# make bands

[Jlen,Vlen]=np.shape(data)

prefix="band"

for i in range(Vlen):
	start=0
	band='v'+str(Vd[Vcas[i]])
	line=data[:,i]
	for j in range(len(line)):
		end=line[j]
		id='v'+str(i)+str(j)
		if end>0:
		   fout.write(prefix+"\t"+band+"\t"+id+"\t"+id+"\t"+str(start)+"\t"+str((start+end))+"\t"+"grey"+"\n")
		   start=start+end
		else:
		   continue;

for i in range(Jlen):
        start=0
        band='j'+str(Jd[Jcas[i]])
        line=data[i,:]
        for j in range(len(line)):
                end=line[j]
                id='j'+str(i)+str(j)
                if end>0:
                   fout.write(prefix+"\t"+band+"\t"+id+"\t"+id+"\t"+str(start)+"\t"+str((start+end))+"\t"+"grey"+"\n")
                   start=start+end
                else:
                   continue;

fout.close()

# make links
fout=open(sys.argv[3],'w')

Vs=sorted(Vcas,reverse=True)
Jpos=np.zeros((Jlen,1),dtype=int)
Jposdict=dict(zip(Jcas,Jpos))

for i in range(Vlen):
	start=0
        id_v='v'+str(Vd[Vs[i]])
        line=data[:,Vd[Vs[i]]]
	Js=zip(Jcas,line)
	Js=sorted(Js,key=lambda x: x[1], reverse=True)
	Js=[p for p in Js if p[1]>0]
	Js=zip(*Js)
	line=Js[1]
	Js=Js[0]
        for j in range(len(line)):		
                end=line[j]
                id_j='j'+str(Jd[Js[j]])
		fout.write(id_v+"\t"+str(start)+"\t"+str(start+end)+"\t"+id_j+"\t"+str(Jposdict[Js[j]][0])+"\t"+str(Jposdict[Js[j]][0]+end)+"\t"+"color="+colordict[id_v]+"\n")

		start=start+end
		Jposdict[Js[j]]=Jposdict[Js[j]]+end

fout.close()



