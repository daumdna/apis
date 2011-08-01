<?php
require "config.php";
session_start();

if(!$_SESSION['access_token'] ) {
	header("Location: ./index.php");
} else {
	$category_id = $_POST['category_id'];
	$title = $_POST['title'];
	$start_at = $_POST['start_at'];
	$end_at = $_POST['end_at'];


	try {
		// Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
		$oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);

		$parameters = array("category_id" => $category_id, "title" => $title, "start_at" => $start_at, "end_at" => $end_at);
		$oauth->fetch($api_url."/calendar/event/create.json", $parameters, "POST");

		$json = $oauth->getLastResponse();

		print_r($json);
	
		echo "<a href=\"./event.php\">".$title."(".$start_at."~".$end_at.") 일정이 추가되었습니다.</a>"; 
	} catch(OAuthException $E) {
		print_r($E);
	}
}
?>
