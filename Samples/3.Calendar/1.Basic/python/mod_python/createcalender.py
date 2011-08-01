# -*- coding: UTF-8 -*
import calendar
#import datetime

#달력 UI 생성
def Create_calender(now_year,now_month, calender_api):
    cal_navi = '<a href="index.html?date=%d-%d">%d-%d</a> | ' % (calculate_month(now_year,now_month,-1)*2) 
    cal_navi += '<span id="now_day">%d-%d</span>' % (now_year,now_month) 
    cal_navi += ' | <a href="index.html?date=%d-%d">%d-%d</a>' % (calculate_month(now_year,now_month,1)*2)    
    
    my_calender = calendar.Calendar( firstweekday=6)
    month = my_calender.monthdayscalendar(now_year,now_month) 
    nweeks = len(month)
    
    maxDay = 0
    for day in xrange(len(month[nweeks-1])-1,-1,-1):           
        if month[nweeks-1][day] <> 0:
            max_day = month[nweeks-1][day]
            break
    calender_api.load_event_by_all("%s-%s-%s" % (now_year,now_month,1),"%s-%s-%s" % (now_year,now_month,max_day))
    cal_result = ''
    for w in range(0,nweeks): 
        week = month[w] 
        cal_result +=  "<ul>\n" 
        for x in xrange(0,7): 
            day = week[x]            
            if x == 0: class_type = 'sunday'
            elif x == 6: class_type = 'saturday' 
            else: class_type = 'day' 
        
            if day == 0: 
                class_type = 'previous' 
                cal_result += '<li id="%s">&nbsp;</li>\n' %(class_type)     
            else: 
                search_date = "%s%s%s" % (now_year,now_month,day)                
                cal_result += '<li><a href="javascript:create_event(\'%s-%s-%s\')"><span id="%s">%s</span></a>' % (now_year,now_month,day ,class_type,day )
                cal_result += '<div id="detail">'
                select_event_result = []
                select_event_result = calender_api.select_event_by_date(search_date)           
                if len(select_event_result)>0:
                    for event in  select_event_result:
                        cal_result += "<span onclick='view_event(\"%s\",\"%s\")'>%s</span><br>" % (event[1], event[0], event[3].encode('utf-8'))
                cal_result += '</div></li>\n' 
        cal_result += '</ul>\n' 
            
    return {'calender':cal_result,'calender_navi':cal_navi}

#이전달, 다음달 계산
def calculate_month(year, mon, flag):
    yr, mo = divmod(mon+flag, 12)
    if mo == 0:
        mo = 12
        yr = -1
    return (year+yr, mo)  

