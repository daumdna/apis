# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
    
from ..oauth_.oauthmanager import OAuth_manager

import time
import createcalender
import calenderapi
import config

def index(request,search_date=None):
    oauth_manager = OAuth_manager(request.session)
    calender_api = calenderapi.calender_api(oauth_manager)
    #등록된 accessToken이 있는지 판단
    if oauth_manager.check_access_token():
        if search_date is None:
            search_date = '%d-%d'%(time.localtime().tm_year,time.localtime().tm_mon)
        result = createcalender.create_calender(int(search_date.split('-')[0]),int(search_date.split('-')[1]),calender_api)
        return render(request,config.index_file,result,content_type="text/html")
    else:
        return HttpResponseRedirect('/tutorial_python/calender/django/oauth/main')

@csrf_exempt 
def create_event(request):
    oauth_manager = OAuth_manager(request.session)
    calender_api = calenderapi.calender_api(oauth_manager)

    start_date = request.POST.get('start_date',None)
    end_date = request.POST.get('end_date',None)
    event_title = request.POST.get('event_title',None)
    event_content = request.POST.get('event_content',None)
    event_mode = request.POST.get('event_mode',-1)
    event_id = request.POST.get('event_id',None)

    if event_title and event_content and start_date and end_date:
        event_title = event_title.encode('utf-8')
        event_content = event_content.encode('utf-8')
        #일정 추가
        if event_mode == '0':
            request_parameters = {'title':event_title,'start_at':start_date,'end_at':end_date,'description':event_content}
            return HttpResponse(calender_api.create_event(request_parameters))
        #일정 수정
        elif event_mode == '1':
            request_parameters = {'title':event_title,'start_at':start_date,'end_at':end_date,'description':event_content}
            return HttpResponse(calender_api.update_event(request_parameters,event_id))
    else:
        return HttpResponse('<br>형식에 맞게 입력하세요.')

    return HttpResponse(status=500)

@csrf_exempt
def view_event(request):
    oauth_manager = OAuth_manager(request.session)
    calender_api = calenderapi.calender_api(oauth_manager)
    id = request.POST.get('id',None)
    start_date = request.POST.get('start_date',None)
    if id and start_date:
        return HttpResponse( calender_api.load_event_by_id(id,start_date))
    return HttpResponse(status=500)

@csrf_exempt
def delete_event(request):
    oauth_manager = OAuth_manager(request.session)
    calender_api = calenderapi.calender_api(oauth_manager)
    id = request.POST.get('id',None)
    if id:
        return HttpResponse(calender_api.delete_event_by_id(id))
    return HttpResponse(status=500)
