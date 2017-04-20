import os
from datetime import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import math

def search(a,m):  
    low = 0   
    high = len(a) - 1   
    while(low <= high):  
        mid = int((low + high)/2)  
        midval = a[mid]  
      
        if midval < m:  
            low = mid + 1   
        elif midval > m:  
            high = mid - 1   
        else:    
            return (mid,0)   
    return (low,-1)  

def modavg(a):
    n=len(a)
    avgdist=list([])
    for i in range(n):
        avgtemp=float(0)
        for j in range(n):
            if not j==i:
                avgtemp=avgtemp+float(a[j])
        avgtemp=float(avgtemp)/float(n-1)
        avgtemp=avgtemp-float(a[i])
        if avgtemp<0:
            avgtemp=float(0)-float(avgtemp)
        avgdist.append(avgtemp)
    maxdist=float(0)
    p=0
    for i in range(n):
        if avgdist[i]>maxdist:
            p=i
            maxdist=avgdist[i]
    avgtemp=float(0)
    for i in range(n):
        if not p==i:
            avgtemp=float(avgtemp)+float(a[i])
    return float(avgtemp)/float(n-1)

def poisson(r):
    p=random.random()
    n=0
    b=math.exp(0-float(r))
    while p>b:
        n=n+1
        b=b+(float(r)**n)/float(math.factorial(n))*math.exp(0-float(r))
    return n

if __name__ == "__main__":
    f=open('volume(table 6)_training.csv','r')
    lines=f.readlines()
    f.close()
    lines=lines[1:]
    times=list([])
    starttime=datetime(2016,9,19,0,0,0)
    delta=timedelta(minutes=1)
    curtime=starttime
    endtime=datetime(2016,10,18,0,0,0)
    while curtime<endtime:
        times.append(curtime.strftime('%Y-%m-%d %H:%M:%S'))        
        curtime=curtime+delta 
    l=len(times)
    ld=int(l/29)
    n=5
    i=0
    mat=list([])
    for i in range(n):
        tp=0
        vec=list([])
        for j in range(l):
            vec.append(tp)
        mat.append(vec)
        del(vec)
    for line in lines:
        trajectory=line.split(",")
        time=trajectory[0][1:]
        time=time[:16]
        time=time+":00"
        gate_id=int(trajectory[1].replace('"',''))
        direction=int(trajectory[2].replace('"',''))
        model=int(trajectory[3].replace('"',''))
        etc=int(trajectory[4].replace('"',''))
        vtype=trajectory[5].replace('"','')
        row=gate_id-1
        if direction>0:
            if gate_id==1:
                row=3
            elif gate_id==3:
                row=4
            else:
                row=1
        col=search(times,time)[0]
        car=mat[row][col]
        mat[row][col]=car+1

    predlist=["2016-10-18 ","2016-10-19 ","2016-10-20 ","2016-10-21 ","2016-10-22 ","2016-10-23 ","2016-10-24 "]
    hrs=["00","01","02","03","04","05","06","07","08","09","10","11",
            "12","13","14","15","16","17","18","19","20","21","22","23"]
    sections=["00:00","20:00","40:00","00:00"]
    subsections=["10:00","30:00","50:00"]
    nowtime=datetime.now()
    nowstr=nowtime.strftime('%m%d%H%M%S')
    f=open('volume_poisson_'+nowstr+'.csv','w')
    f.write('tollgate_id,time_window,direction,volume\n')
    for route in range(5):
        oriseq=mat[route]
        curpointer=0
        slicedseq=list([])
    
        while curpointer<len(times):
            slicedseq.extend(oriseq[curpointer:curpointer+480])
            piece=oriseq[curpointer+480:curpointer+600]
            fftpiece=np.fft.fft(piece)
            for i in range(int(0.1*len(fftpiece)),len(fftpiece)):
                fftpiece[i]=0
            piecetrunc=np.fft.ifft(fftpiece)
            slicedseq.extend(piecetrunc)
            slicedseq.extend(oriseq[curpointer+600:curpointer+1020])
            piece=oriseq[curpointer+1020:curpointer+1140]
            fftpiece=np.fft.fft(piece)
            for i in range(int(1*len(fftpiece)),len(fftpiece)):
                fftpiece[i]=0
            piecetrunc=np.fft.ifft(fftpiece)
            slicedseq.extend(piecetrunc)
            slicedseq.extend(oriseq[curpointer+1140:curpointer+1440])
            curpointer=curpointer+1440
    
        newslot=list([])
        for i in range(7*1440):
            j=i+l-1440*7
            avgbag=list([])
            while j>=0:
                avgbag.append(slicedseq[j])
                j=j-1440*7
            newslot.append(modavg(avgbag))
            del(avgbag)

        predslot=list([])
        for i in range(len(newslot)):
            predslot.append(poisson(newslot[i]))

        output=list([])
        for i in range(int(len(predslot)/20)):
            temp=0
            for j in range(20):
                temp=temp+predslot[i*20+j]
            output.append(temp)

        if route==0:
            tollgate=1
            direction=0
        elif route==1:
            tollgate=2
            direction=0
        elif route==2:
            tollgate=3
            direction=0
        elif route==3:
            tollgate=1
            direction=1
        else:
            tollgate=3
            direction=1

        outputpos=0
        for i in range(7):
            date=predlist[i]
            for hr in hrs:
                for j in range(3):
                    hour=hr+":"+sections[j]
                    if j==2:
                        hrnext=str(int(hr)+1)
                        if len(hrnext)<2:
                            hrnext="0"+hrnext
                    else:
                        hrnext=hr
                    hournext=hrnext+":"+sections[j+1]
                    if (hr=="08")or(hr=="09")or(hr=="17")or(hr=="18"):
                        f.write(str(tollgate)+',"['+date+hour+','+date+hournext+')",'+str(direction)+','+str(output[outputpos])+'\n')
                    outputpos=outputpos+1
        del(output)
    f.close()
