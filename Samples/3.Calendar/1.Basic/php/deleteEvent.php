<?php
require "config.php";
session_start();

if(!$_SESSION['access_token'] ) {
	header("Location: ./index.php");
} else {
	$id = $_GET['id'];

	try {
	    // Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
	    $oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);

	    // $category_id 조회
	    $oauth->fetch($api_url."/calendar/event/delete/".$id.".json");
	    $json = json_decode($oauth->getLastResponse());
	    $event = $json->title."(".$json->id.")";

	    echo "<a href=\"./event.php\">".$event." 일정이 삭제 되었습니다.</a>";
		exit;
	} catch(OAuthException $E) {
	    print_r($E);
	}
}
?>
