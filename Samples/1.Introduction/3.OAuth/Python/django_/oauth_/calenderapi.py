# -*- coding: UTF-8 -*-
import config
import oauthmodule
from xml.etree import ElementTree

class Calender_api(object):
    def __init__(self,oauth_manager):                
        self.oauth_manager = oauth_manager;
        
    def load_event_by_all(self,start_date,end_date):           
        resource_url = "https://apis.daum.net/calendar/event/index.xml"
        request_parameters = {'start_at':start_date,'end_at':end_date}         
        response_xml = ElementTree.fromstring(self.oauth_manager.access_resource(request_parameters, resource_url) )
        load_event_all = []
        for events in response_xml:
            for event in events:
                if event.tag == 'title':
                    load_event_all.append(event.text )
	
        return load_event_all
