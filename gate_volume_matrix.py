import os
from datetime import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    output=list([])
    for i in range(n):
        v=list([])
        for j in range(l):
            v.append(0)
        output.append(v)
        del(v)
    plt.plot(mat[4])
    plt.show()
    exit(0)
    for i in range(n):
        for j in range(l):
            output[i][j]=mat[i][j]
    f=open('gate_time_vector_vol_1min.csv','w')
    f.write("gate,")
    for i in range(l):
        f.write(times[i]+",")
    f.write("\n")
    for i in range(n):
        f.write(str(i)+",")
        for j in range(l):
            f.write(str(output[i][j])+",")
        f.write("\n")
    f.close()
    
    
