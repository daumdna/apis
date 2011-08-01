<?php

require "config.php";

session_start();

// access_token이 발급된 상태가 아니라면, OAuth 인증 절차 시작
if(!$_SESSION['access_token'] ) {

	try {
		// Request Token 요청
		$request_token_info = $oauth->getRequestToken($request_token_url, $callback_url);

		// 얻어온 Request Token을 이후 Access Token과 교환하기 위해 session에 저장.
		$_SESSION["request_token_secret"] = $request_token_info["oauth_token_secret"];

		// 사용자 인증 URL로 redirect
		header('Location: '.$authorize_url.'?oauth_token='.$request_token_info['oauth_token']);
		exit;
	} catch(OAuthException $E) {
		print_r($E);
		exit;
	}
} else {
// Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
	$oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);
	$oauth->fetch($api_url."/calendar/category/index.xml");
	$xml = simplexml_load_string($oauth->getLastResponse());

}
?>
<!doctype html>
<html>
<head>
<script>
</script>
</head>

<body>
<ul>
<?php
	foreach($xml->category as $category) {
		echo "<li>";
		echo $category->name;
		echo "</li>";
	}
?>
</ul>
</body>
</html>
