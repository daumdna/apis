# -*- coding: UTF-8 -*-
import oauthmodule
import config
from xml.etree import ElementTree

from datetime import datetime, timedelta

class Calender_api(object):
    def __init__(self,oauth_manager):
        self.load_event_all = []
        self.oauth_manager = oauth_manager;
        
    def create_event(self,request_parameters):           
        resource_url = "https://apis.daum.net/calendar/event/create.xml"
        result = '<p>'
        response_xml = ElementTree.fromstring(self.oauth_manager.access_resource(request_parameters, resource_url) )
        
        if response_xml.tag == 'apierror':
            result = '에러코드 : %s<br>' % response_xml.find('code').text
            result += '에러내용 :  %s'  % response_xml.find('message').text
        else :
            result += '등록되었습니다.'                
        return result  +"</p>"
    def update_event(self,request_parameters,event_id):      
        resource_url = "https://apis.daum.net/calendar/event/update/%s.xml" %event_id
        result = '<p>'
        response_xml = ElementTree.fromstring(self.oauth_manager.access_resource(request_parameters, resource_url) )
        if response_xml.tag == 'apierror':
            result = '에러코드 : %s<br>' % response_xml.find('code').text
            result += '에러내용 :  %s'  % response_xml.find('message').text
        else :
            result += '수정되었습니다.'                
        return result+'</p>'
    
    def load_event_by_all(self,start_date,end_date):           
        resource_url = "https://apis.daum.net/calendar/event/index.xml"
        request_parameters = {'start_at':start_date,'end_at':end_date}         
        response_xml = ElementTree.fromstring(self.oauth_manager.access_resource(request_parameters, resource_url) )
        for events in response_xml:
            event_result = []    
            for event in events:
                if event.tag == 'end_at' or event.tag == 'id' or event.tag == 'start_at' or event.tag == 'title':
                    event_result.append(event.text)
            self.load_event_all.append(event_result)
    
    def select_event_by_date(self,search_date):
        result = []
        for event_list in self.load_event_all:
            if  (datetime.strptime(search_date, '%Y%m%d')-datetime.strptime(event_list[2].split('T')[0].replace('-',''), '%Y%m%d')) >= timedelta(days=0):
                if (datetime.strptime(search_date, '%Y%m%d')-datetime.strptime(event_list[0].split('T')[0].replace('-',''), '%Y%m%d')) <= timedelta(days=0):
                    result.append(event_list)
        return result
            
    def load_event_by_id(self,id,search_date):
        resource_url = "https://apis.daum.net/calendar/event/show/%s.xml" % id
        request_parameters = {'start_at':search_date,'end_at':search_date}    
        response_xml = ElementTree.fromstring(self.oauth_manager.access_resource(request_parameters, resource_url) )
        result =''
        if response_xml.find('code') is not None:            
            result += '에러코드 - %s<br>' % response_xml.find('code').text.encode('utf-8')
            result += '에러내용 - %s' % response_xml.find('message').text.encode('utf-8')
        else:
            result += "%s," % response_xml.find('title').text.encode('utf-8')
            result += "%s," % response_xml.find('description').text.encode('utf-8')
            result += "%s," % response_xml.find('start_at').text
            result += "%s," % response_xml.find('end_at').text
            result += "%s," % id
        return  result
    
    def delete_event_by_id(self,id):
        resource_url = "https://apis.daum.net/calendar/event/delete/%s.xml" % id
        response_xml = ElementTree.fromstring(self.oauth_manager.access_resource('', resource_url) )
        result = '<p>'
        if response_xml.find('code') is not None:            
            result += '에러코드 - %s<br>' % response_xml.find('code').text.encode('utf-8')
            result += '에러내용 - %s' % response_xml.find('message').text.encode('utf-8')
        else:
            result += '삭제되었습니다.'
        return result+'</p>'
