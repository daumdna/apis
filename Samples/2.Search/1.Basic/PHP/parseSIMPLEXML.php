<?php

// Parsing Daum OpenAPI REST Web Service results using
// SimpleXML extension. PHP5 only.
// Author: Rasmus Lerdorf, Yahoo! Inc.
//         Sang-Kil Park, Daum Communications Corp.

error_reporting(E_ALL);

$request = 'http://apis.daum.net/search/blog?apikey={발급 받은 키를 입력하세요.}&q='.urlencode('다음');

$response = file_get_contents($request);

if ($response === false) {
	die('Request failed');
}

$phpobject = simplexml_load_string($response);

if ($phpobject === false) {
	die('Parsing failed');
}

// Output the data
// SimpleXML returns the data as a SimpleXML object
$channel = $phpobject->channel;

echo "<h1>".$channel->title."</h1><br />";
echo "<h2>검색결과: ".$channel->totalCount."</h2><br />";

foreach($channel->item as $value) {
	echo "제목: ".$value->title."<br />";	
	echo "내용: ".$value->description."<br />";
	echo "<hr />";
}
?>