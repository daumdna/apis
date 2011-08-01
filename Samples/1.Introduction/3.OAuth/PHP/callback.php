<?php
require "config.php";

session_start();
if($_GET['oauth_verifier'] ) {
	try {
		// Request Token과 verifier로 Access Token 얻기
		$oauth->setToken($_GET['oauth_token'],$_SESSION["request_token_secret"]);
		$access_token_info = $oauth->getAccessToken($access_token_url, null, $_GET['oauth_verifier']);

		// Access Token으로 교환 되었으므로 Request Token 삭제.
		unset($_SESSION["request_token_secret"]);
		
		// Access Token을 세션에 저장
		$_SESSION['access_token'] = $access_token_info['oauth_token'];
		$_SESSION['access_token_secret'] = $access_token_info['oauth_token_secret'];
	} catch(OAuthException $E) {
		print_r($E);
		exit;
	}
}
// protected resource가 있는 페이지로
header("Location: ./index.php");
?>
