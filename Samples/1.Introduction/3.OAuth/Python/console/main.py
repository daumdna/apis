# -*- coding: UTF-8 -*-
import oauthmodule
import config

if __name__ == '__main__':
    """
    request_token 
    request_authorize_url
    request_access_token
    access_resource(Calender API)
    """
    oauth_module = oauthmodule.OAuth(config.consumer_key,config.consumer_secret,config.api_server,config.api_port) 
    request_token_string = oauth_module.request_token(config.request_token_url,config.callback_url)
    #print "RequestToken --> %s"%request_token_string
    #print "--------------------------------------"
    authorize_url = oauth_module.request_authorize_url(request_token_string, config.authorize_url,config.callback_url)
    print "아래 url을 웹브라우저에서 입력후 인증코드를 입력해주세요."
    print authorize_url
    verifier_code =  raw_input('인증 코드를 입력하세요 :  ')
    access_token_string = oauth_module.request_access_token(request_token_string,config.access_token_url,verifier_code)
    #print "AccessToken --> %s"%access_token_string
    #print "--------------------------------------"
    resource_url = "https://apis.daum.net/calendar/event/index.xml"
    request_parameters = {'start_at':'2011-04-01','end_at':'2011-07-30'}
    api_result = oauth_module.access_resource(access_token_string, request_parameters, resource_url)    
    print api_result
