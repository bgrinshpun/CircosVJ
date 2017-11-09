#!/usr/bin/env python

import sys
import re

# define colors
inputfile=sys.argv[1]
Vcol=int(sys.argv[2])
Jcol=int(sys.argv[3])

f=open(inputfile,'r')
h=f.readline()
data=f.readlines()
data=[i.strip().split("\t") for i in data]
data=zip(*data)

allV=list(set(data[Vcol]))
allV=[i.translate(None, 'TCRA') for i in allV]
allV=[i.translate(None, 'TCRB') for i in allV]
allV=[c.lower() for c in allV]
allJ=list(set(data[Jcol]))
allJ=[i.translate(None, 'TCRA') for i in allJ]
allJ=[i.translate(None, 'TCRB') for i in allJ]
allJ=[c.lower() for c in allJ]

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

allV=sorted(allV,key=lambda x: natural_key(x))
allJ=sorted(allJ,key=lambda x: natural_key(x))

# V colors
r = 125;
g = 0;
b= 0;
totdist=(255-125)*2+(2*255)
stepsize=totdist/len(allV)

colors=[(r,g,b)]

while(r<255):
	tmp=255-r;
	r+=stepsize;
	if(r>255):
		r=255;
		g=g+(stepsize-tmp-1);
	colors.append((r,g,b))


while(g < 255):
	tmp=255-g;
	g += stepsize;
	if(g > 255): 	
		g = 255;
		r=r-(stepsize-tmp-1);
	colors.append((r, g, b));

while(r > 0):
	tmp=r
	r -= stepsize;
	if(r<0):
		r=0;
		g=g-tmp-1;
	colors.append((r, g, b)); 

while(g>125):
	g-=stepsize;
	colors.append((r,g,b))

colors=colors[0:len(allV)]
Vcolors=zip(allV,colors)
Vcolors


# J colors
r = 128;
g = 0;
b = 128
totdist=(255-128)+255+128
stepsize=totdist/len(allJ)

colors=[((r,g,b))]
while(b < 255):
	tmp=255-b
        b += stepsize;
        if(b > 255):
                b = 255;
		g=g+(stepsize-tmp-1);
        colors.append((r, g, b));

while(g < 255):
	tmp=255-g;
        g += stepsize;
        if(g > 255):
                g = 255;
		r = r-(stepsize-tmp-1);
        colors.append((r, g, b));

while(r > 0):
	r -= stepsize;
	colors.append((r,g,b))

colors=colors[0:len(allJ)]
Jcolors=zip(allJ,colors)

RGBlist=Vcolors+Jcolors

invrange=range(1,11)
invrange=[i/10. for i in invrange]
invrange=map(str,invrange)

subscripts=['_a1','_a2','_a3','_a4','_a5','_a6','_a7','_a8','_a9','_a10','_a11','_a12','_a13','_a14','_a15','_a16','_a17']

for line in RGBlist:
        print line[0]+ "  =  " + str(line[1])[1:-1]
        for i in xrange(len(invrange)):
                print line[0] + subscripts[i] + "  =  " + str(line[1])[1:-1] + "," + invrange[i] 



