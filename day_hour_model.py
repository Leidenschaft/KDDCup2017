import os

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

if __name__ == "__main__":
    f=open('volume(table 6)_training.csv','r')
    lines=f.readlines()
    f.close()
    lines=lines[1:]
    times=list([])
    MON=list(["2016-09-19 ","2016-09-26 ","2016-10-03 ","2016-10-10 ","2016-10-17 "])
    TUE=list(["2016-09-20 ","2016-09-27 ","2016-10-04 ","2016-10-11 "])
    WED=list(["2016-09-21 ","2016-09-28 ","2016-10-05 ","2016-10-12 "])
    THU=list(["2016-09-22 ","2016-09-29 ","2016-10-06 ","2016-10-13 "])
    FRI=list(["2016-09-23 ","2016-09-30 ","2016-10-07 ","2016-10-14 "])
    SAT=list(["2016-09-24 ","2016-10-01 ","2016-10-08 ","2016-10-15 "])
    SUN=list(["2016-09-25 ","2016-10-02 ","2016-10-09 ","2016-10-16 "])
    daylist=[TUE,WED,THU,FRI,SAT,SUN,MON]
    days=SAT
    predlist=["2016-10-18 ","2016-10-19 ","2016-10-20 ","2016-10-21 ","2016-10-22 ","2016-10-23 ","2016-10-24 "]
    hour='17:20:00'
    for line in lines:
        entry=line.split(",")
        time=entry[0]
        time=time[1:]
        time=time[:15]
        time=time+"0:00"
        rtuple=search(times,time)
        if rtuple[1]==-1:
            times.insert(rtuple[0],time)
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
        time=time[:15]
        time=time+"0:00"
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
    hrs=["00","01","02","03","04","05","06","07","08","09","10","11",
            "12","13","14","15","16","17","18","19","20","21","22","23"]
    sections=["00:00","20:00","40:00","00:00"]
    subsections=["10:00","30:00","50:00"]

    f=open('volume.csv','w')
    f.write('tollgate_id,time_window,direction,volume\n')
    for route in range(5):
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
        
        for i in range(7):
            days=daylist[i]
            date=predlist[i]
            for hr in hrs:
                for j in range(3):
                    hour=hr+":"+sections[j]
                    hour2=hr+":"+subsections[j]
                    if j==2:
                        hrnext=str(int(hr)+1)
                        if len(hrnext)<2:
                            hrnext="0"+hrnext
                    else:
                        hrnext=hr
                    hournext=hrnext+":"+sections[j+1]
                    modset=list([])
                    for day in days:
                        curtime=day+hour
                        curtime2=day+hour2
                        p=search(times,curtime)
                        v=0
                        if p[1]>-1:
                            p=p[0]
                            v=mat[route][p]
                        p=search(times,curtime2)
                        if p[1]>-1:
                            p=p[0]
                            v=v+mat[route][p]
                        modset.append(v)
                    if (hr=="08")or(hr=="09")or(hr=="17")or(hr=="18"):
                        f.write(str(tollgate)+',"['+date+hour+','+date+hournext+')",'+str(direction)+','+str(float(modavg(modset))*0.94)+'\n')
                    del(modset)
    f.close()

"""   
    for route in range(5):
        if route==0:
            print("Gate1,in")
        elif route==1:
            print("Gate2,in")
        elif route==2:
            print("Gate3,in")
        elif route==3:
            print("Gate1,out")
        else:
            print("Gate3,out")
        for day in days:
            curtime=day+hour
            j=search(times,curtime)[0]
            print(curtime+"  :  "+str(mat[route][j]))
        print("")
        print("")
"""

    
    
