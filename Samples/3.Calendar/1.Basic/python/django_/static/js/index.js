function init(){
    $('#mask').click(function (e) {
        e.preventDefault();
        $(this).hide();
        $('#manage_wrap').hide();
        $("#api_result").hide();
      }); 
    $('#close_modal').click(function (e) {
        //링크 기본동작은 작동하지 않도록 한다.
        e.preventDefault();
        $('#manage_wrap').hide();
        $('#api_result').hide();
        $('#mask').hide();
    }); 
}

function do_modal(div_id){
    //Get the screen height and width
    $("#loading").hide();
    $("#api_result").hide()
    $("#manage_wrap").hide();

    var maskHeight = $(document).height();
    var maskWidth = $(window).width();

    //Set height and width to mask to fill up the whole screen
    $('#mask').css({'width':maskWidth,'height':maskHeight});
    //transition effect     
    $('#mask').fadeTo("slow",0.8);  

    //Get the window height and width
    var winH = $(window).height();
    var winW = $(window).width();

    //Set the popup window to center
    $(div_id).css('top',  winH/2-$(div_id).height()/2);
    $(div_id).css('left', winW/2-$(div_id).width()/2);

    //transition effect
    $(div_id).fadeIn(1000); 
}

function create_event(day){			
    $("#event_submit").val('생성');					
    $('#start_date').val(day);
    $('#end_date').val(day);
    $('#event_title').val('');
    $('#event_content').val('');
    $("#event_mode").val('0');
    $("#event_id").val('');
    $("#btn_delete").hide(); 
    do_modal('#manage_wrap');
}

function create_event_submit(){			
    $("#loading").show();
    $.ajax({
        type : "POST",
        url: '/tutorial_python/calender/django/calender/main/create_event',
        data: $("#create_event").serialize(),			
        success: function(response_text){	
            result(response_text);
        },
        error: function(jqXHR, textStatus, errorThrown){
            result("시스템 장애. 잠시후 다시 이용해주세요.<br>("+errorThrown+")");
        }
    });
    return false;
}

function view_event(id,start_date){
    $("#loading").show();
    $.ajax({
        type : "POST",
        url: '/tutorial_python/calender/django/calender/main/view_event',
        data: 'id='+id+'&start_date='+start_date,
        success: function(response_text){
            split_response = response_text.split(',')
            if (response_text.length <= 2) {
                result(response_text);
            } else {
                $("#event_title").val(split_response[0]);
                $("#event_content").val(split_response[1]);
                $("#start_date").val(split_response[2]);
                $("#end_date").val(split_response[3]);
                $("#event_id").val(split_response[4]);
                $("#event_mode").val('1');
                $("#event_submit").val('수정');           
                $("#api_result").css('display', 'none');
                $("#btn_delete").show();
                do_modal("#manage_wrap");
            }													
        },
        error: function(jqXHR, textStatus, errorThrown){
            result("시스템 장애. 잠시후 다시 이용해주세요.<br>("+errorThrown+")");
        }

    });
    return false;
}

function delete_event(){
    $("#loading").show();
    $.ajax({
        type : "POST",
        url: '/tutorial_python/calender/django/calender/main/delete_event',
        data: 'id=' + $("#event_id").val(),				
        success: function(response_text){				
             result(response_text);
        },
        error: function(jqXHR, textStatus, errorThrown){
            result("시스템 장애. 잠시후 다시 이용해주세요.<br>("+errorThrown+")");
        }
    });
    return false;
}

function result(response_text){
    $("#api_result").html(response_text);
    do_modal("#api_result");
    $(function(){
        slider = setInterval(function(){
            window.location.reload();
        }, 1500);
    });
}
