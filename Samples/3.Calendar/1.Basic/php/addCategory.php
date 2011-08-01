<?php
require "config.php";
session_start();

if(!$_SESSION['access_token'] ) {
	header("Location: ./index.php");
} else {
	$name = $_POST['name'];
	$color = $_POST['color'];
	$description = $_POST['description'];

	try {
		// Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
		$oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);

		$parameters = array("name" => $name, "color" => $color, "description" => $description);
		$oauth->fetch($api_url."/calendar/category/create.json", $parameters, "POST");

		$json = $oauth->getLastResponse();
	
		echo "<a href=\"./index.php\">카테고리 [".$name."] 추가되었습니다.</a>";
	} catch(OAuthException $E) {
		print_r($E);
	}
}
?>
