# -*- coding: UTF-8 -*-
import httplib
import oauth.oauth as oauth

class OAuth(oauth.OAuthClient):
    def __init__(self, consumer_key, consumer_secret, api_server, api_port, session):   
        #클래스 멤버변수를 설정합니다.
        #OAuth인증방식은 HMAC_SHA1을 사용합니다.
        self.session = session
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = ''
        self.set_access_token(self.session.get('access_token',False))
        self.signature_method_Hmac_Sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()        
        self.counsumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
        self.api_connection = httplib.HTTPSConnection("%s:%d" % (api_server, api_port))

    def request_token(self, request_token_Url, callback_url):        
        #OAuth 요청 정보를 생성합니다.
        oAuth_request = oauth.OAuthRequest.from_consumer_and_token(self.counsumer, http_url=request_token_Url, callback=callback_url)
        oAuth_request.sign_request(self.signature_method_Hmac_Sha1, self.counsumer, None)
        #생성한 OAuth 요청 정보를 HTTP(S)통신을 이용하여 호출합니다.
        self.api_connection.request(oAuth_request.http_method, request_token_Url, headers=oAuth_request.to_header())        
        request_token_reponse_body = self.api_connection.getresponse().read()   
	#디버깅용 모드에서만 작동하며 정상적으로 request_token을 받지 못하면 에러가 발생합니다.
        if __debug__:
            assert request_token_reponse_body.find('oauth_token') >= 0, ' %s' % request_token_reponse_body           
        #발급받은 request_token을 OAuthToken객체로 만듭니다.
        return oauth.OAuthToken.from_string(request_token_reponse_body)
        
    def request_authorize_user(self, token, authorizationUrl, callback_url):        
        #사용자 인증에 필요한 Url을 생성합니다.
        return "%s?oauth_token=%s&oauth_callback=%s" % (authorizationUrl, token.key, callback_url)
    
    def request_access_token(self, request_token_string, verifier_code, access_token_url):
        #AccessToken을 요청하기 위해 OAuth 요청 정보를 만듭니다.
        request_token = oauth.OAuthToken.from_string(request_token_string)
        
        oAuth_request = oauth.OAuthRequest.from_consumer_and_token(self.counsumer, token=request_token, http_url=access_token_url, verifier=verifier_code)        
        oAuth_request.sign_request(self.signature_method_Hmac_Sha1, self.counsumer, request_token)                
        #생성한 OAuth 요청 정보를 HTTP(S)통신을 이용하여 호출합니다.
        self.api_connection.request(oAuth_request.http_method, access_token_url, headers=oAuth_request.to_header())
        access_token_response_body = self.api_connection.getresponse().read()
        #디버깅용 모드에서만 작동하며 정상적으로 accessToken을 받지 못하면 에러가 발생합니다.
        if __debug__:
            assert access_token_response_body.find('oauth_token') >= 0, ' %s' % access_token_response_body      
        #발급받은 accessToken을 OAuthToken객체로 변환합니다.
        self.access_token = oauth.OAuthToken.from_string(access_token_response_body)
        #발급받은 OAuthToken을 세션에 저장합니다.
        self.save_access_token_to_session()
    
    def access_resource(self, parameters, resourceUrl):
        #보호된 자원에 접근합니다.
        #resource의 parameters와 resourceUrl을 이용하여 OAuth 요청 정보를 생성합니다.
        #post 방식으로 요청합니다.
        OAuthRequest = oauth.OAuthRequest.from_consumer_and_token(self.counsumer, token=self.access_token, http_method='POST', http_url=resourceUrl, parameters=parameters)       
        OAuthRequest.sign_request(self.signature_method_Hmac_Sha1, self.counsumer, self.access_token)
        headers = {'Content-Type' :'application/x-www-form-urlencoded'}
        print 'AccessResource PostData - %s' % OAuthRequest.to_postdata()
        self.api_connection.request('POST', resourceUrl, body=OAuthRequest.to_postdata(), headers=headers)
	return self.api_connection.getresponse().read()
   
    def set_access_token(self,access_token_string):
        if access_token_string:
            self.access_token = oauth.OAuthToken.from_string(access_token_string)

    def save_access_token_to_session(self):
        self.session['access_token'] = self.access_token.to_string()
        self.session.save()

    def check_access_token(self):
        if self.access_token:
            return True
        return False
