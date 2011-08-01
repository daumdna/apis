# -*- coding: UTF-8 -*-
from mod_python import apache
from mod_python import util
from mod_python import Session
import time
import calenderapi
import createcalender
import oauthmanager
import config

def handler(req):
    req.send_http_header()
    req.content_type = 'text/html;charset=UTF-8'
    session = Session.Session(req,timeout=3600)
    session.load()
    session = session_init(session) 
    oauth_manager = oauthmanager.OAuth_manager(session)
    calender_api = calenderapi.Calender_api(oauth_manager)
    #request parameter 
    formValueList = util.FieldStorage(req)
    #URL에서 파일명 추출
    real_file_name = req.filename[ req.filename.rfind('/')+1:]
    if real_file_name == 'index.html':
        #등록된 accessToken이 있는지 판단
        if oauth_manager.check_access_token():
            template = file(config.index_file).read()
            search_date = formValueList.get('date', '%s-%s'%(time.localtime().tm_year,time.localtime().tm_mon))
            try:
               content = createcalender.Create_calender(int(search_date.split('-')[0]), int(search_date.split('-')[1]), calender_api)
            except ValueError, error:
            #data 형식이 잘못 되었을 경우
               req.write ("ValueError -> %s" % error)
            else:
               req.write (template % content)
        else:
        #등록된 accessToken이 없다면 인증페이지로
            util.redirect(req,'oauth.py');	    
    elif real_file_name == 'oauth.py':
        oauth_template = file(config.oauth_file).read()
        req.write (oauth_template) 
    elif real_file_name == 'request_token.py':
        #request_token 생성 및 사용자 인증 URL redirect
        util.redirect(req,oauth_manager.create_reqeust_token())
    #callback_url 처리
    elif real_file_name == 'callback.py':
    	oauth_manager.create_access_token(req)
        util.redirect(req,'index.html')
   #createevent.py        
    elif real_file_name == 'createevent.py':
        start_date = formValueList.get('start_date',None)
        end_date = formValueList.get('end_date',None)
        event_title = formValueList.get('event_title',None)
        event_content = formValueList.get('event_content',None)
        event_mode = formValueList.get('event_mode',-1)
        event_id = formValueList.get('event_id',None)
        #일정 추가
        if event_mode == '0':
            request_parameters = {'title':event_title,'start_at':start_date,'end_at':end_date,'description':event_content}
            req.write ( calender_api.create_event(request_parameters) )
        #일정 수정
        elif event_mode == '1':
            request_parameters = {'title':event_title,'start_at':start_date,'end_at':end_date,'description':event_content}
            req.write ( calender_api.update_event(request_parameters,event_id) )
    #viewevent.py 
    elif real_file_name == 'viewevent.py':
        id = formValueList.get('id',None)
        start_date = formValueList.get('start_date',None)
        req.write ( calender_api.load_event_by_id(id,start_date) )
    #deleteevent.py
    elif real_file_name == 'deleteevent.py':
        id = formValueList.get('id',None)
        req.write( calender_api.delete_event_by_id(id) )

    return apache.OK  

def session_init(session):
    if session.is_new():
	session['request_token'] = None
	session['access_token'] = None
    session.save()
    return session

