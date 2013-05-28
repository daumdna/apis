<?php
$API_URL_PREFIX = "https://apis.daum.net";
$MYPEOPLE_BOT_APIKEY = $_POST['apikey'];
$API_URL_POSTFIX = "&apikey=" .$MYPEOPLE_BOT_APIKEY;

$fileId = $_POST['fileId'];
$url =  $API_URL_PREFIX. "/mypeople/file/download.xml?fileId=" .$fileId .$API_URL_POSTFIX;

//헤더정보를 함께 읽어와 파일명과 파일타입을 얻는다
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt ($ch, CURLOPT_HEADER, 1);
$result = curl_exec($ch);
curl_close($ch);

var_dump($result);

if ($result != false) {
	$filename = '';
	$results = split("\n", trim($result));
	foreach($results as $line) {
		if (strtok($line, ':') == 'Content-Disposition') {
			$parts = explode("=", $line);
			$filename = trim($parts[1]);	////헤더 부분에서 파일명 추출
		}
	}
	//파일 부분
	$body = $results[count($results)-1];

	//파일 저장할 폴더 생성
	$downloaddir =  $_SERVER['DOCUMENT_ROOT'] . '/download/';
	if(is_dir($downloaddir) == false) mkdir($downloaddir, 0700,TRUE);
	$downloadfilepath = $downloaddir .$filename;

	//파일로 저장
	saveFile($downloadfilepath, $body);
	
	echo "저장된 이미지";
	echo "<img src=/download/$filename>";
}


function saveFile($filePath, $content)
{
	$fo = fopen($filePath , 'w');
	fwrite($fo, $content);
	fclose($fo);
}
?>