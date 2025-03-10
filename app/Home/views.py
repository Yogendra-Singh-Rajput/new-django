from django.shortcuts import render,HttpResponse
from datetime import datetime
# Create your views here.
from .map import context
from numerology.views import list_numerology_apps
import re
from .models import contact_form
from .serializers import contact_form_serializer

all_apps_list = list_numerology_apps
def highlighter(string_main,substr):
    flag = True
    start=0
    final_str = ''
    c=0
    while flag:
        c+=1
        x = re.search(substr.lower(),string_main[start:].lower())
        flag = False if x is None else True
        if not flag:
            break
        final_str+=(f"{string_main[start:x.start()+start]}<span class='highlight' id = 'search_highlight'>{string_main[x.start()+start:x.end()+start]}</span>")
        start+=x.end()
    final_str+=string_main[start:]
    return final_str

def search_fn(s):
    s=s.strip()
    if len(s)>=3:
        token_list = re.split(r'[\s!@#$%^&*\(\)/?<>\-+\.]',s)
        token_list = list(set(token_list))
        try:
            token_list.remove('')
        except Exception as e:
            pass
        token_list=[i for i in token_list if len(i)>=2 ]
        final_list = []
        for i in all_apps_list:
            temp=i.copy()
            c=0
            flag=False
            for j in token_list:
                if re.search(j.lower(),temp[0].lower()):
                    flag=True
                    temp[0]=highlighter(temp[0],j)
                    c+=1
            if flag:
                final_list.append((temp[0],c,temp[1]))
        
        final_list = list(sorted(final_list,key=lambda x: x[1], reverse=True))
        final_list = [(i[0],i[2]) for i in final_list]
        return final_list if len(final_list)!=0 else [("No Results Found - Home",'../')] 
    else:
        return [("No Results Found - Home",'../')] 

def home(req,context=context):
    context.update({'services_dict':{'Numerology':'numerology/','Cards':'cards/'}.items()})
    return render(req,'index.html',context=context)

def search(req,context=context):
    searched_item = req.POST['searched_item']
    context.update({'final_list':search_fn(searched_item)})
    return render(req, 'search.html', context=context)

def contact_us(req, context=context):
    context.update({'flag':False})
    if req.method == "POST":
        print(req.POST)
        serializer = contact_form_serializer(data=req.POST)
        if serializer.is_valid():
            serializer.save()
            context['flag']=True
            return render(req,'contact_us.html',context=context)
    return render(req, 'contact_us.html', context=context)