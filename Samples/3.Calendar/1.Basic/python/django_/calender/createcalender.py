# -*- coding: UTF-8 -*
import calendar

#달력 UI 생성
def create_calender(now_year,now_month, calender_api):
    result = {}
    result['prev_date'] = '%d-%d'%(calculate_month(now_year,now_month,-1)) 
    result['now_date'] = '%d-%d' % (now_year,now_month) 
    result['next_date']= '%d-%d' % (calculate_month(now_year,now_month,1))    
    
    my_calender = calendar.Calendar( firstweekday=6)
    month = my_calender.monthdayscalendar(now_year,now_month) 
    nweeks = len(month)
    
    maxDay = 0
    for day in xrange(len(month[nweeks-1])-1,-1,-1):           
        if month[nweeks-1][day] <> 0:
            max_day = month[nweeks-1][day]
            break
    calender_api.load_event_by_all("%s-%s-%s" % (now_year,now_month,1),"%s-%s-%s" % (now_year,now_month,max_day))
    
    cal_result = []
    for w in range(0,nweeks): 
        week = month[w] 
        for x in xrange(0,7): 
            day = week[x]            
            if x == 0: class_type = 'sunday'
            elif x == 6: class_type = 'saturday' 
            else: class_type = 'day' 
        
            day_result = []
            if day == 0: 
                class_type = 'previous' 
                day_result.append(class_type)     
            else: 
                search_date = "%s-%s-%s" % (now_year,now_month,day)                
                day_result.append(class_type)
                day_result.append(search_date)     
                day_result.append(day)
                select_event_result = []
                select_event_result = calender_api.select_event_by_date(search_date)    
                if len(select_event_result)>0:
                    for event in  select_event_result:
                        day_result.append(select_event_result)
            cal_result.append(day_result)
    result['calender'] = cal_result 
    return result
    #{'calender':cal_result,'calender_navi':cal_navi}

#이전달, 다음달 계산
def calculate_month(year, mon, flag):
    yr, mo = divmod(mon+flag, 12)
    if mo == 0:
        mo = 12
        yr = -1
    return (year+yr, mo)  

