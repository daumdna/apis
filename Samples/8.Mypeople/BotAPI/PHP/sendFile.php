<?php
sendFile("buddy", $_POST['buddyId'], $_POST['content'], $_FILES['upload']);

function sendFile($target, $targetId, $msg, $file)
{
	
	$API_URL_PREFIX = "https://apis.daum.net";
	$MYPEOPLE_BOT_APIKEY = $_POST['apikey'];
	$API_URL_POSTFIX = "&apikey=" .$MYPEOPLE_BOT_APIKEY;

	//파일 전송 url 지정
	$url =  $API_URL_PREFIX."/mypeople/" .$target. "/send.xml?" .$target."Id=" .$targetId. "&content=attach" .$API_URL_POSTFIX;

	//파일을 일단 서버에 업로드 합니다.
	$uploadfilepath = NULL;
	$uploadfilename = 'attach.png';
	if($file['tmp_name'] != '')
	{
		$uploaddir =  $_SERVER['DOCUMENT_ROOT'] . '/upload/myapi/mypeoplebot/';
		if(is_dir($uploaddir) == false) mkdir($uploaddir, 0700,TRUE);
		$uploadfilename = urlencode($file['name']);
		$uploadfilepath = $uploaddir .$uploadfilename;
		move_uploaded_file($file['tmp_name'], $uploadfilepath);
	}
	else
	{
		$uploadfilepath = $_SERVER['DOCUMENT_ROOT']. '/upload/myapi/mypeoplebot/' .$uploadfilename;
	}

	//파일 타입과 파일 이름을 설정합니다.
	$postData = array();
	$postData['attach']	= '@'.$uploadfilepath.	";type=" .$file['type'].";filename=" .$uploadfilename;

	//cURL을 이용한 POST전송
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, 0);

	$result = curl_exec($ch);
	curl_close($ch);
	var_dump($result);
}
?>