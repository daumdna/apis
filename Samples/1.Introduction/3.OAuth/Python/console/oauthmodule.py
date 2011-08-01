# -*- coding: UTF-8 -*-
import httplib
import oauth.oauth as oauth

class OAuth(oauth.OAuthClient):
    def __init__(self, consumer_key, consumer_secret, api_server, api_port):   
        """
        클래스 멤버변수를 설정합니다.
        OAuth인증방식은 HMAC_SHA1을 사용합니다.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()    
        self.counsumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
        self.connection = httplib.HTTPSConnection("%s:%d" % (api_server, api_port))
    def request_token(self, url, callback_url):        
        """
        OAuth 요청 정보를 생성합니다.
        생성한 OAuth 요청 정보를 HTTP(S)통신을 이용하여 호출합니다.
        request_token을 return합니다.
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.counsumer, http_url=url, callback=callback_url)
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.counsumer, None)
        self.connection.request(oauth_request.http_method, url, headers=oauth_request.to_header())        
        return self.connection.getresponse().read()           
    def request_authorize_url(self, token, url, callback_url):        
        """
        사용자 인증에 필요한 url을 생성 및 return 합니다.
        """
        oauth_request_token = oauth.OAuthToken.from_string(token)
        return "%s?oauth_token=%s&oauth_callback=%s" % (url, oauth_request_token.key, callback_url)
    def request_access_token(self, token, url, verifier):        
        """
        AccessToken을 요청하기 위해 OAuth 요청 정보를 만듭니다.
        생성한 OAuth 요청 정보를 HTTP(S)통신을 이용하여 호출합니다.
        access_token을 return합니다.
        """
        oauth_request_token = oauth.OAuthToken.from_string(token)        
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.counsumer, token=oauth_request_token, http_url=url, verifier=verifier)        
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.counsumer, oauth_request_token)                
        self.connection.request(oauth_request.http_method, url, headers=oauth_request.to_header())
        return self.connection.getresponse().read()
    def access_resource(self, token, parameters, url):
        """
        보호된 자원에 접근합니다.
        resource의 parameters와 resource_url을 이용하여 oauth 요청 정보를 생성합니다.
        post 방식으로 요청합니다.
        """
        oauth_access_token = oauth.OAuthToken.from_string(token)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.counsumer, token=oauth_access_token, http_method='POST', http_url=url, parameters=parameters)       
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.counsumer, oauth_access_token)
        headers = {'Content-Type' :'application/x-www-form-urlencoded'}
        self.connection.request('POST', url, body=oauth_request.to_postdata(), headers=headers)
        return self.connection.getresponse().read()   
