# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect

import config
import oauthmanager
import calenderapi

def index(request):
    oauth_template = file(config.oauth_file).read()
    oauth_manager = oauthmanager.OAuth_manager(request.session)
    #등록된 accessToken이 있는지 판단
    if oauth_manager.check_access_token():
        return HttpResponseRedirect('/tutorial_python/calender/django/calender/main')
    else:
        return HttpResponse(oauth_template)

def request_token(request):
    oauth_manager = oauthmanager.OAuth_manager(request.session)
    return HttpResponseRedirect(oauth_manager.create_reqeust_token())

def callback(request):
    oauth_manager = oauthmanager.OAuth_manager(request.session)
    verifier_code = request.GET['oauth_verifier']
    oauth_manager.create_access_token(verifier_code)
    return HttpResponseRedirect('/tutorial_python/calender/django/oauth/main')

def access_resource(request):
    oauth_manager = oauthmanager.OAuth_manager(request.session)
    calender_api = calenderapi.Calender_api(oauth_manager)
    result = 'Daum Calender API - 일정가져오기<br>'
    for title in calender_api.load_event_by_all('2011-5-1','2011-6-30'):
        result +=  ('일정제목 -> %s<br>' % (title.encode('utf-8')) )
    return HttpResponse(result)


