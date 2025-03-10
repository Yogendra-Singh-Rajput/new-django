from django.shortcuts import render, HttpResponse
from datetime import datetime as dt, timedelta
import math
import re
# Create your views here.
from Home.map import context

def fn(name,dob):
    variable = f'Hi, {name} your Date of Birth is {dt.strptime(dob,"%Y-%m-%d").strftime("%A, %dth of %B, %Y")}'
    variable1 = '...Thank You for Visiting...'
    return variable,variable1

def mul(n):
            x = str(n)
            while(len(x)!=1):
                sumx = 0
                for _ in x:
                    sumx = sumx + int(_)
                x = str(sumx)
            return int(x)

def home(req,context=context):
    context.update({
        'apps':[
            ('Soulmate Date of Birth Finder - Loshu Cube','app1/'),
            ('Loshu Cube - Compatibility Checker','app2/'),
            ('Loshu Cube Generator','app3/')
            ]
    })
    return render(req,'numerology_home.html',context=context)

# Soulmate Date of Birth Finder - Loshu Cube
def app1(req,context=context):
    def app1_fn(dob,r1=5,r2=5,comp=100):
        dob = dt.strptime(dob,"%Y-%m-%d")
        dob_str=dob.strftime('%Y%M%d')
        dob_list=[i for i in dob_str]
        my_mulank = mul(dob.day)
        my_bhagyank = mul(dob.day+dob.year+dob.month)
        dob_list.append(my_mulank)
        dob_list.append(my_bhagyank)
        l = list(range(1,10))
        for i in dob_list:
            if int(i) in l:
                l.remove(int(i))
        if r1 == 0:
            end = dt.strptime(dob.strftime('%Y-12-31'),'%Y-%m-%d')
        else:
            end  = dob + timedelta(days=365*r1)
        if r2 == 0:
            start = dt.strptime(dob.strftime('%Y-01-01'),'%Y-%m-%d')
        else:
            start = dob - timedelta(days=365*r2)

        def test(dx):
            c = 0
            strx = dx.strftime('%d%m%Y')
            lx = list(strx)
            lx.append(str(mul(dx.day)))
            lx.append(str(mul(strx)))
            #l = [3,8,5,7,6]  # Extra Numbers Required in loshu cube
            for _ in l:
                if str(_) in lx:
                    c+=1
            real_comp=int((c/len(l))*100)
            if c >= int(len(l)*(comp/100)):
                return (True,real_comp)
            else:
                return (False,real_comp)
        final_list=[]
        while(start<=end):
            test_start,test_comp=test(start)
            if test_start:
                final_list.append(f"--MATCHED--  {start.strftime('%d-%b-%Y')}  --MATCHED--  Compatibility - {test_comp}%")
            start+=timedelta(days=1)
        final_list = final_list if len(final_list)!=0 else ["No Matching Dates Found...."]
        if final_list[0] != "No Matching Dates Found....":
            final_list = list(sorted(final_list,key= lambda x : int(re.search('([^- ]*)%',x).group()[:-1]),reverse=True))
        return final_list, len(final_list)

    if req.method=="POST":
        name=req.POST['name']
        dob=req.POST['dob']
        r1=int(req.POST['r1'])
        r2=int(req.POST['r2'])
        compatibility=int(req.POST['r3'])
        variable, variable1 = fn(name,dob)
        final_list,n=app1_fn(dob,r1=r1,r2=r2,comp=compatibility)
        
        context.update({
            'variable':variable,
            'variable1':variable1,
            'final_list':final_list,
            'n':n,
            'final_list_0':final_list[0],
            'r1':r1,
            'r2':r2,
            'compatibility':compatibility
            })
        return render(req,'app1_results.html',context=context)
    return render(req,'app1.html',context=context)
    #return HttpResponse(f'<h1>Welecome to Numerology App 1 Page</h1>')

# Loshu Cube - Compatibility Checker
def app2(req,context=context):
    def app2_fn(dob1,dob2):
        dob1_day=dt.strptime(dob1,'%Y-%m-%d').day
        dob2_day=dt.strptime(dob2,'%Y-%m-%d').day
        dob1=dob1.replace('-','').replace('0','')
        dob2=dob2.replace('-','').replace('0','')
        dob1=[int(i) for i in dob1]
        dob2=[int(i) for i in dob2]
        dob1.append(mul(sum(dob1)))
        dob1.append(mul(dob1_day))
        dob2.append(mul(sum(dob2))) 
        dob2.append(mul(dob2_day))
        dob=list(set(dob1+dob2))
        comp=(len(dob)/9)*100
        ideal_list = [4,9,2,3,5,7,8,1,6]
        for i in range(len(ideal_list)):
            if ideal_list[i] in dob:
                context.update({f'num{i+1}':f'{ideal_list[i]}'})
            else:
                context.update({f'num{i+1}':"-"})
        return round(comp,2)
    if req.method=="POST":
        dob1=req.POST['dob1']
        dob2=req.POST['dob2']
        comp = app2_fn(dob1,dob2)
        context.update({'comp':f"Compatibility Score - {comp}%"})
        return render(req,'app2_results.html',context=context)
    return render(req,'app2.html',context=context)

# Loshu Cube - Generator
def app3(req,context=context):
    def app3_fn(dob1):
        dob1_day=dt.strptime(dob1,'%Y-%m-%d').day
        
        dob1=dob1.replace('-','').replace('0','')
        dob1=[int(i) for i in dob1]
        dob1.append(mul(sum(dob1)))
        dob1.append(mul(dob1_day))
        dob=list(set(dob1))
        comp=(len(dob)/9)*100
        ideal_list = [4,9,2,3,5,7,8,1,6]
        for i in range(len(ideal_list)):
            if ideal_list[i] in dob:
                context.update({f'num{i+1}':f'{ideal_list[i]}'})
            else:
                context.update({f'num{i+1}':"-"})
    if req.method=="POST":
        dob1=req.POST['dob1']
        comp = app3_fn(dob1)
        return render(req,'app3_results.html',context=context)
    return render(req,'app3.html',context=context)



list_numerology_apps = [
    ['Soulmate Date of Birth Finder - Loshu Cube','../numerology/app1'],
    ['Loshu Cube - Compatibility Checker','../numerology/app2'],
    ['Loshu Cube Generator','../numerology/app3']
]