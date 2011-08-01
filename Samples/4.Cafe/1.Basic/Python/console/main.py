# -*- coding: UTF-8 -*-
import oauthmodule
import config

"""
    print문으로 각 단계를 구분하였습니다. 한 단계씩 테스트 해보세요.
    request_token 
    request_authorize_url
    request_access_token
    access_resource(Calender API)
"""
if __name__ == '__main__':    
    oauth_module = oauthmodule.OAuth(config.consumer_key,config.consumer_secret,config.api_server,config.api_port) 
    request_token_string = oauth_module.request_token(config.request_token_url,config.callback_url)
    print "RequestToken --> %s"%request_token_string
    print "--------------------------------------"
    authorize_url = oauth_module.request_authorize_url(request_token_string, config.authorize_url,config.callback_url)
    print "아래 url을 웹브라우저에서 입력후 인증코드를 입력해주세요."
    print authorize_url
    verifier_code =  raw_input('인증 코드를 입력하세요 :  ')
    access_token_string = oauth_module.request_access_token(request_token_string,config.access_token_url,verifier_code)
    print "AccessToken --> %s"%access_token_string
    print "--------------------------------------"
    resource_url = "http://apis.daum.net/cafe/write_article/{cafeCode}/{boardId}.xml"
    request_parameters = {'content':'여기는 메모를 삽입합니다.','hideyn':'N'}
    api_result = oauth_module.access_resource(access_token_string, request_parameters, resource_url)    
    print api_result
