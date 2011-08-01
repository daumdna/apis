# -*- coding: UTF-8 -*-
from mod_python import apache
from mod_python import util
from mod_python import Session
import calenderapi
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
    #URL에서 파일명 추출
    real_file_name = req.filename[ req.filename.rfind('/')+1:]
    if real_file_name == 'index.html':
        #등록된 accessToken이 있는지 판단
        if oauth_manager.check_access_token():
            util.redirect(req,'access_resource.py');	    
        else:
        #등록된 accessToken이 없다면 인증페이지로
            util.redirect(req,'oauth.py');	    
    elif real_file_name == 'oauth.py':
        oauth_template = file(config.oauth_file).read()
        req.write (oauth_template) 
    elif real_file_name == 'request_token.py':
        #request_token 생성 및 사용자 인증 URL redirect
        util.redirect(req,oauth_manager.create_reqeust_token())
    elif real_file_name == 'callback.py':
        #callback_url 처리
	oauth_manager.create_access_token(req)
        util.redirect(req,'index.html')
    elif real_file_name == 'access_resource.py':
        for title in calender_api.load_event_by_all('2011-5-1','2011-5-31'):
            req.write ( '일정 제목 -> %s<br>' % (title.encode('utf-8')) )

    return apache.OK  

def session_init(session):
    if session.is_new():
	session['request_token'] = None
	session['access_token'] = None
    session.save()
    return session

